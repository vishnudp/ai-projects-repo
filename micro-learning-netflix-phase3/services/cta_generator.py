from pathlib import Path
from moviepy import *


def create_cta_clip():

    duration = 3

    assets = Path(
        "generated/assets/icons"
    )

    # ----------------------------------
    # BACKGROUND
    # ----------------------------------

    bg = (
        ColorClip(
            size=(1080, 1920),
            color=(0, 0, 0)
        )
        .with_duration(duration)
    )

    # ----------------------------------
    # CENTER RED GLOW
    # ----------------------------------

    center_glow = (

        ColorClip(
            size=(1080, 1920),
            color=(229, 9, 20)
        )

        .with_opacity(0.08)

        # .with_position(
        #     ("center", 150)
        # )

        .with_duration(duration)

    )

    red_overlay = ColorClip(
        size=(1080,1920),
        color=(229,9,20)
    ).with_opacity(0.04).with_duration(duration)

    # ----------------------------------
    # TITLE
    # ----------------------------------

    title = (

        TextClip(
            text="FOLLOW FOR MORE",
            font_size=95,
            color="#E50914",
            stroke_color="white",
            stroke_width=1,
            method="caption",
            size=(950,150),
            text_align="center"
        )

        .with_position(
            ("center",180)
        )

    )

    subtitle = (

        TextClip(
            text="Daily AI - Business - Tech Reels",
            font_size=40,
            color="white"
        )

        .with_position(
            ("center",350)
        )

    )

    # ----------------------------------
    # CARD
    # ----------------------------------

    def card(y):

        return (

            ColorClip(
                size=(700,140),
                color=(20,20,20)
            )

            .with_opacity(0.85)

            .with_position(
                ("center", y)
            )

            .with_duration(duration)

        )

    card1 = card(650)
    card2 = card(840)
    card3 = card(1030)
    card4 = card(1220)

    # ----------------------------------
    # ICONS
    # ----------------------------------

    icon_x = 280
    text_x = 410

    follow_icon = (
        ImageClip(str(assets/"follow.png"))
        .resized(height=75)
        .with_position((icon_x,685))
    )

    comment_icon = (
        ImageClip(str(assets/"comment.png"))
        .resized(height=75)
        .with_position((icon_x,875))
    )

    share_icon = (
        ImageClip(str(assets/"share.png"))
        .resized(height=75)
        .with_position((icon_x,1065))
    )

    save_icon = (
        ImageClip(str(assets/"save.png"))
        .resized(height=75)
        .with_position((icon_x,1255))
    )

    # ----------------------------------
    # TEXT
    # ----------------------------------

    def main_text(text, y):

        return (

            TextClip(
                text=text,
                font_size=48,
                color="white",
                method="caption",
                size=(350, 60),     # important
            )

            .with_position(
                (text_x, y)
            )

        )

    def sub_text(text, y):

        return (

            TextClip(
                text=text,
                font_size=26,
                color="#aaaaaa",
                method="caption",
                size=(350, 40),     # important
            )

            .with_position(
                (text_x, y)
            )

        )

    follow_txt = main_text(
        "FOLLOW",
        690
    )

    comment_txt = main_text(
        "COMMENT",
        880
    )

    share_txt = main_text(
        "SHARE",
        1070
    )

    save_txt = main_text(
        "SAVE",
        1260
    )

    follow_sub = sub_text(
        "Stay updated",
        745
    )

    comment_sub = sub_text(
        "Share thoughts",
        935
    )

    share_sub = sub_text(
        "Spread content",
        1125
    )

    save_sub = sub_text(
        "Watch later",
        1315
    )

    # ----------------------------------
    # CTA
    # ----------------------------------

    return CompositeVideoClip(

        [
            bg,
            red_overlay,
            center_glow,

            title,
            subtitle,

            card1,
            card2,
            card3,
            card4,

            follow_icon,
            comment_icon,
            share_icon,
            save_icon,

            follow_txt,
            comment_txt,
            share_txt,
            save_txt,

            follow_sub,
            comment_sub,
            share_sub,
            save_sub
        ],

        size=(1080,1920)

    ).with_duration(duration)