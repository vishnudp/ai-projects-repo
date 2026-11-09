from moviepy import *


def create_light_sweep(duration):

    sweep = (

        ColorClip(
            size=(220, 1920),
            color=(255, 255, 255)
        )

        .with_duration(duration)

        .with_opacity(0.10)

    )

    sweep = sweep.with_position(

        lambda t:

        (
            -300 +
            (
                1700 *
                (t / duration)
            ),

            0
        )

    )

    return sweep