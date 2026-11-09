from moviepy import *
from services.ui.card_helper import create_card
def create_outcome_card(
    text,
    duration
):

    # bg = (

    #     ColorClip(
    #         (1000,180),
    #         color=(0,0,0)
    #     )

    #     .with_opacity(1)

    #     .with_duration(duration)

    # )

    bg = create_card(
        width=1000,
        height=180,
        color=(0,0,0),
        radius=16,
        duration=duration,
        border_color="#00FF7F",
        border_width=1
    ).with_opacity(1)

    icon = (
        ImageClip(
            "generated/assets/icons/outcome.png"
        )
        .resized(height=80)
        .with_duration(duration)
        .with_position((20,30))
    )

    title = TextClip(
        text="LEARNING OUTCOME",
        font="generated/assets/fonts/BebasNeue-Regular.ttf",
        font_size=60,
        color="#00FF7F",
        size=(550,60)
    ).with_duration(duration)

    body = (
        TextClip(
            text=text,
            font_size=30,
            color="white",
            size=(900,150),
            method="caption"
        )
        .with_duration(duration)
    )

    return (
        CompositeVideoClip(
            [
                bg,
                icon,
                title.with_position((30,15)),
                body.with_position((40,40))
            ],
            size=(1000,210)
        )
        .with_duration(duration)
        .with_position((40,1500))
    )