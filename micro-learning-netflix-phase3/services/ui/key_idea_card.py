from moviepy import *
from services.ui.card_helper import create_card

def create_key_idea_card(
    text,
    duration
):

    # bg = (
    #     ColorClip(
    #         (550,330),
    #         color=(20,20,20)
    #     )
    #     .with_opacity(0.8)
    #     .with_duration(duration)
    # )

    bg = create_card(
        width=430,
        height=330,
        color=(20,20,20),
        radius=16,
        duration=duration,
        border_color="#cccccc",
        border_width=1
    ).with_opacity(0.8)

    icon = (
        ImageClip(
            "generated/assets/icons/idea.png"
        )
        .resized(height=80)
        .with_duration(duration)
        .with_position((20,30))
    )

    title = (
        TextClip(
            text="KEY IDEA",
            font="generated/assets/fonts/BebasNeue-Regular.ttf",
            font_size=60,
            color="#FFD700",
            size=(330, 80),
        )
        .with_duration(duration)
        
    )

    body = (
        TextClip(
            text=text,
            font_size=32,
            color="white",
            size=(350,220),
            method="caption"
        )
        .with_duration(duration)
        .with_position((300,15))
    )


    return (
        CompositeVideoClip(
            [
                bg,
                icon,
                title.with_position((25,20)),
                body.with_position((40,50))
            ],
            size=(450,350)
        )
        .with_duration(duration)
        .with_position((40,720))
    )