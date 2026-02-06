import sys
import typer
import tempfile
from gtts.lang import tts_langs
from gtts import gTTS
from typing_extensions import Annotated
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
from pycaps import TemplateLoader
from pathlib import Path
import questionary


def tts(text, lang, out):
    """Converts text to speech using google translate API. Output file is saved to the path out"""

    tts = gTTS(text, lang=lang)
    tts.save(str(out))


def combine(audio, video, out):
    """Combines audio and video files, making video loop"""

    # loop video
    loops_required = int(audio.duration // video.duration) + 1
    video_clips = [video] * loops_required
    looped_video = concatenate_videoclips(video_clips)

    clip = looped_video.subclipped(0, audio.duration).with_audio(audio)
    clip.write_videofile(out, codec="libx264", audio_codec="aac")


def generate(
    recording: Annotated[
        Path,
        typer.Argument(
            exists=True, file_okay=True, dir_okay=False, readable=True, help="Path to the background video for the reel"
        ),
    ],
    lang: Annotated[
        str, typer.Option(help="Language to use for text-to-speech, otherwise selected interactively")
    ] = None,
    outfile: Annotated[Path, typer.Option(help="Name of reel to be generated.")] = Path("output.mp4"),
    script: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Path to script for the reel, otherwise taken from stdin",
        ),
    ] = None,
    captions_template: Annotated[str, typer.Option(help="Name of pycaps template to use.")] = "hype",
):
    # outfile
    if outfile.exists():
        if questionary.confirm(f"File '{str(outfile)} already exists, remove it?'").ask():
            outfile.unlink()
        else:
            raise typer.Exit(1)

    # tts language
    languages = tts_langs()
    if lang is None:
        # Interactive selection
        choice = questionary.select(
            "Select language:",
            choices=[
                questionary.Choice(
                    title=f"{code} — {name}",
                    value=code,
                )
                for code, name in sorted(languages.items())
            ],
        ).ask()

        if choice is None:
            raise typer.Exit(1)
        lang = choice
    elif lang not in languages:
        raise typer.BadParameter(f"Unsupported language '{lang}'.")

    # script
    if script is None:
        if sys.stdin.isatty():
            typer.echo("Reading script from stdin (Ctrl-D to finish):", err=True)

        script = sys.stdin.read()
    else:
        script = script.read_text(encoding="utf-8")

    typer.echo("Generating reel...")
    with tempfile.TemporaryDirectory() as outdir:
        outdir = Path(outdir)
        audio_file = outdir / "audio.mp3"

        tts(script, lang, audio_file)
        audio = AudioFileClip(audio_file)
        video = VideoFileClip(recording)

        combined = outdir / "combined.mp4"

        combine(audio, video, combined)

        TemplateLoader(captions_template).with_input_video(combined).with_output_video(outfile).load().run()
