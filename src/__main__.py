from moviepy import VideoFileClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips
from gtts import gTTS
import requests
import pathlib
from pycaps import TemplateLoader


# todo: actually scrape some social media site with an api
def scrape():
    url = "https://automatetheboringstuff.com/files/rj.txt"
    response = requests.get(url)

    return response.text[3720:6000]


def tts(text, out=pathlib.Path("out.mp3")):
    """Converts text to speech using google translate API. Output file is saved to the path out"""

    tts = gTTS(text)
    tts.save(str(out))


def combine(audio, video, out=pathlib.Path("out.mp4")):
    """Combines audio and video files, making video loop"""

    # loop video
    loops_required = int(audio.duration // video.duration) + 1
    video_clips = [video] * loops_required
    looped_video = concatenate_videoclips(video_clips)

    clip = looped_video.subclipped(0, audio.duration).with_audio(audio)
    clip.write_videofile(out, codec="libx264", audio_codec="aac")


print("Generating reel...")
outdir = pathlib.Path("build")
outdir.mkdir(parents=True, exist_ok=True)

text = scrape()

audio_file = outdir / "audio.mp3"
tts(text, out=audio_file)
audio = AudioFileClip(audio_file)

input_file = pathlib.Path("recording.mp4")
video = VideoFileClip(input_file)

combined_file = outdir / "combined.mp4"

combine(audio, video, combined_file)

output_file = outdir / "output.mp4"
TemplateLoader("hype").with_input_video(combined_file).with_output_video(output_file).load().run()
