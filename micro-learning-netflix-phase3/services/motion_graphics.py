from moviepy import *
import numpy as np


def create_progress_bar(duration):

    def make_frame(t):

        frame = np.zeros(
            (12, 1080, 3),
            dtype=np.uint8
        )

        width = int(
            (t / duration) * 1080
        )

        frame[:, :width] = [229, 9, 20]

        return frame

    return (
        VideoClip(
            frame_function=make_frame,
            duration=duration
        )
        .with_position(
            ("left", 1908)
        )
    )

def create_kinetic_title(
    text,
    duration
):

    title_clip = TextClip(
        text=text.upper(),
        font_size=60,
        color="#E50914",
        stroke_color="black",
        stroke_width=5,
        method="caption",
        size=(820, 700),
        text_align="center"
    )

    title_clip = (
        title_clip
        .with_duration(duration)
        .with_position(
            ("center", 120)
        )
    )

    return title_clip