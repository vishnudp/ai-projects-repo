from moviepy import *
from services.ui.card_helper import create_card

def create_purpose_block(purpose,duration):

    # bg = (
    #     ColorClip(
    #         (980,140),
    #         color=(0,0,0)
    #     )
    #     .with_opacity(0.65)
    #     .with_duration(duration)
    # )

    bg = create_card(
        width=980,
        height=140,
        color=(0,0,0),
        radius=16,
        duration=duration,
        border_color=(0,0,0,255),
        border_width=3
    ).with_opacity(0.65)

    icon = (
        ImageClip(
            "generated/assets/icons/purpose.png"
        )
        .resized(height=80)
        .with_duration(duration)
        .with_position((20,30))
    )

    title = (
        TextClip(
            text="PURPOSE",
            font_size=40,
            color="#FFD700",
            size=(170,60)
        )
        .with_duration(duration)
        .with_position((120,30))
    )

    txt = (
        TextClip(
            text=purpose,
            font_size=34,
            color="white",
            method="caption",
            size=(680,90),
            text_align="left"
        )
        .with_duration(duration)
        .with_position((300,15))
    )
        

    return (
        CompositeVideoClip(
            [bg,icon,title,txt],
            size=(980,140)
        )
        .with_duration(duration)
        .with_position((50,550))
    )