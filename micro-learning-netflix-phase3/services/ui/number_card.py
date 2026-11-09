from moviepy import *
from services.ui.card_helper import create_card
def create_number_card(
    number,
    duration
):

    # bg = (
    #     ColorClip(
    #         (550,330),
    #         color=(180,25,25)
    #     )
    #     .with_opacity(0.92)
    #     .with_duration(duration)
    # )

    bg = create_card(
        width=500,
        height=330,
        color=(180,25,25),
        radius=16,
        duration=duration,
        border_color="#000000",
        border_width=1
    ).with_opacity(0.92)

    icon = (
        ImageClip(
            "generated/assets/icons/calendar.png"
        )
        .resized(height=55)
        .with_duration(duration)
        .with_position((20,30))
    )

    title = TextClip(
        text="IMPORTANT NUMBER",
        font="generated/assets/fonts/BebasNeue-Regular.ttf",
        font_size=60,
        color="white",
        size=(500, 60),

    ).with_duration(duration)

    num = TextClip(
        text=number,
        font_size=95,
        font="generated/assets/fonts/BebasNeue-Regular.ttf",
        color="#FFC72C",
        size=(470, 160),
    ).with_duration(duration).with_position(("center",110))
    

    return (
        CompositeVideoClip(
            [
                bg,
                icon,
                title.with_position((25,20)),
                num.with_position(("center",75))
            ],
            size=(550,330)
        )
        .with_duration(duration)
        .with_position((500,720))
    )