from moviepy import *
def create_purpose_block(text,duration):

    bg = (
        ColorClip(
            (980,110),
            color=(0,0,0)
        )
        .with_opacity(0.65)
        .with_duration(duration)
    )

    icon = (
        ImageClip(
            "generated/assets/icons/purpose.png"
        )
        .resized(height=40)
        .with_duration(duration)
        .with_position((20,30))
    )

    title = (
        TextClip(
            text="PURPOSE",
            font_size=30,
            color="#FFD700"
        )
        .with_duration(duration)
        .with_position((80,28))
    )

    body = (
        TextClip(
            text=text,
            font_size=28,
            color="white",
            size=(700,None),
            method="caption"
        )
        .with_duration(duration)
        .with_position((260,25))
    )

    return CompositeVideoClip(
        [
            bg,
            icon,
            title,
            body
        ],
        size=(980,110)
    )