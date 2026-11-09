from moviepy import *


def create_subtitle(
    text,
    start,
    end
):

    duration = end - start

    bg = (
        ColorClip(
            size=(980, 110),
            color=(0, 0, 0)
        )
        .with_opacity(0.55)
        .with_duration(duration)
    )

    caption = (
        TextClip(
            text=text,
            font="generated/assets/fonts/Montserrat-ExtraBold.ttf",
            font_size=36,
            color="white",
            size=(900, 110),
            method="caption"
        )
        .with_duration(duration)
    )

    return (
        CompositeVideoClip(
            [
                bg,
                caption.with_position(
                    ("center", "center")
                )
            ],
            size=(980, 110)
        )
        .with_start(start)
        .with_end(end)
        .with_position(
            ("center", 1720)
        )
    )