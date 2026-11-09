from moviepy import *
from services.ui.card_helper import create_card

def create_quote_card(
    text,
    duration
):

    # bg = (

    #     ColorClip(
    #         (1000,180),
    #         color=(15,15,15)
    #     )

    #     .with_opacity(1)

    #     .with_duration(duration)

    # )

    bg = create_card(
        width=1000,
        height=180,
        color=(15,15,15),
        radius=16,
        duration=duration,
        border_color="#FFD700",
        border_width=1
    ).with_opacity(1)

    icon = (
        ImageClip(
            "generated/assets/icons/quote.png"
        )
        .resized(height =120)
        .with_duration(duration)
        .with_position((20,30))
    )

    title = TextClip(
        text="IMPORTANT QUOTE",
        font_size=60,
        color="#FFD700",
        font="generated/assets/fonts/BebasNeue-Regular.ttf",
        size=(600, 65),
    ).with_duration(duration)

    quote = (
        TextClip(
            text=f'"{text}"',
            font_size=34,
            color="#FFFFFF",
            size=(880,70),
            method="caption"
        )
        .with_duration(duration)
    )

    return (
        CompositeVideoClip(
            [
                bg,
                icon,
                title.with_position((30,10)),
                quote.with_position((60,70))
            ],
            size=(1000,180)
        )
        .with_duration(duration)
        .with_position((40,1280))
    )