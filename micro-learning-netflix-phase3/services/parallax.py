from moviepy import *

def create_parallax(
    bg,
    duration
):

    layer1 = (
        bg
        .resized(1.15)
        .with_position(
            lambda t:
            (
                -100*(t/duration),
                0
            )
        )
    )

    layer2 = (
        bg
        .resized(1.05)
        .with_position(
            lambda t:
            (
                40*(t/duration),
                0
            )
        )
        .with_opacity(0.35)
    )

    return CompositeVideoClip(
        [
            layer1,
            layer2
        ]
    )