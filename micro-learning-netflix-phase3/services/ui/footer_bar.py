from moviepy import *

def create_footer_bar(
    keywords,
    duration
):

    tags = " • ".join(
        keywords[:4]
    )

    bg = (

        ColorClip(
            size=(1080,120),
            color=(0,0,0)
        )

        .with_opacity(1)

        .with_duration(duration)
    )

    txt = (

        TextClip(
            text=tags,
            font_size=28,
            color="white",
            method="caption",
            size=(900,60)
        )

        .with_duration(duration)

        .with_position(
            (40,15)
        )
    )

    return (

        CompositeVideoClip(
            [
                bg,
                txt
            ],
            size=(1080,120)
        )

        .with_duration(duration)

        .with_position(
            (0,"bottom")
        )

    )