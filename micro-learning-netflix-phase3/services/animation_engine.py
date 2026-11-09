from moviepy import TextClip


def create_title_clip(
    text,
    duration
):

    return (
        TextClip(
            text,
            font_size=90,
            method="caption",
            size=(900, None)
        )
        .with_duration(duration)
    )