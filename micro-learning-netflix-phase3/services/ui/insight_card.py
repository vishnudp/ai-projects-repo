from moviepy import *
from services.ui.card_helper import create_card
def create_insight_card(
    text,
    duration
):

    # bg = (
    #     ColorClip(
    #         (1000,220),
    #         color=(0,30,80)
    #     )
    #     .with_opacity(0.85)
    #     .with_duration(duration)
    # )

    bg = create_card(
        width=1000,
        height=180,
        color=(0,30,80),
        radius=16,
        duration=duration,
        border_color="#00BFFF",
        border_width=1
    ).with_opacity(0.85)

    icon = (
        ImageClip(
            "generated/assets/icons/insight.png"
        )
        .resized(height=80)
        .with_duration(duration)
        .with_position((20,30))
    )

    title = (
        TextClip(
            text="KEY INSIGHT",
            font_size=60,
            font="generated/assets/fonts/BebasNeue-Regular.ttf",
            color="#00BFFF",
            size=(390, 60),
        )
        .with_duration(duration)
    )

    body = (
        TextClip(
            text=text,
            font_size=32,
            color="white",
            size=(940,100),
            method="caption"
        )
        .with_duration(duration)
    )

    icon_right = (
        ImageClip(
            "generated/assets/icons/insight_right.png"
        )
        .resized(height=110)
        .with_duration(duration)
        
    )

    icon_right = icon_right.with_position(
        (1080 - icon_right.w - 90, 20)
    )
    return (
        CompositeVideoClip(
            [
                bg,
                icon,

                # NEW TITLE
                title.with_position((30,15)),

                # BODY BELOW TITLE
                body.with_position((30,65)),
                icon_right
            ],
            size=(1000,200)
        )
        .with_duration(duration)
        .with_position((40,1070))
    )