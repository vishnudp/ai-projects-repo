from moviepy import *
from moviepy.video.fx.FadeOut import FadeOut
def create_title_block(
    title,
    duration
):

    title = title.upper()

    return (

        TextClip(
            text=title.upper(),
            font_size=135,
            color="#FF0000",
            font="generated/assets/fonts/BebasNeue-Regular.ttf",
            stroke_color="#000000",
            stroke_width=1,
            method="caption",
            text_align="center",
            size=(920,450)
        ).with_position(
            ("center", 80)
        )
        .with_duration(
            min(duration, 2.5)
        )

        .with_effects([
            FadeOut(0.8)
        ])


    )