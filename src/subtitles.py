import re
import pathlib
from datetime import timedelta
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy import TextClip


def srt_time(td: timedelta) -> str:
    total_ms = int(td.total_seconds() * 1000)
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_m = total_s // 60
    m = total_m % 60
    h = total_m // 60
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def sub(text, full_dursec, size, out=pathlib.Path("subtitles.srt")):
    lines = re.split("\n{2,}", text)

    num = len(lines)
    dursec = full_dursec / num

    start = timedelta(hours=0, seconds=-dursec)
    duration = timedelta(seconds=dursec)

    # list of timedetlas
    tdlist = []
    for i in range(num + 1):
        start = start + duration
        tdlist.append(start)

    srt = []
    for i in range(num):
        srt.append(f"{i + 1}\n{srt_time(tdlist[i])} --> {srt_time(tdlist[i + 1])}\n{lines[i]}\n")

    srt = "\n".join(srt)

    with open(out, "w") as f:
        f.write(srt)

    generator = lambda text: TextClip(
        text=text,
        font_size=24,
        color="black",
        stroke_color="#000000",
        stroke_width=1,
        text_align="center",
        horizontal_align="center",
        vertical_align="bottom",
        size=size,
    )
    return SubtitlesClip(
        out,
        make_textclip=generator,
        encoding="utf-8",
    )
