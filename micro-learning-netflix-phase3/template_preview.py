from moviepy import *
from pathlib import Path

from services.ui.title_block import *
from services.ui.purpose_block import *
from services.ui.key_idea_card import *
from services.ui.number_card import *
from services.ui.insight_card import *
from services.ui.quote_card import *
from services.ui.outcome_card import *
from services.ui.footer_bar import *
from services.ui.bottom_gradient import *
from services.ui.card_helper import create_card

WIDTH = 1080
HEIGHT = 1920

def create_rating_overlay(score, duration):

    assets = Path(
        "generated/assets/icons"
    )

    # badge_bg = (

    #     ColorClip(
    #         size=(180,100),
    #         color=(15,15,15)
    #     )

    #     .with_opacity(0.8)

    #     .with_duration(duration)

    #     .with_position((20,30))

    # )

    badge_bg = create_card(
        width=180,
        height=100,
        color=(15,15,15),
        radius=25,
        duration=duration,
        border_color=(0,0,0,255),
        border_width=3
    ).with_opacity(0.8).with_position((20,30))

    star = (

        ImageClip(
            str(assets / "star.png")
        )

        .resized(height=45)

        .with_duration(duration)

        .with_position((40,60))

    )

    score_txt = (

        TextClip(
            text=str(score),
            font_size=48,
            color="white",
            stroke_color="black",
            stroke_width=2,
            size=(90, 60),     # important
        )

        .with_duration(duration)

        .with_position((90,40))

    )

    return [

        badge_bg,

        star,

        score_txt

    ]


def build_preview():

    duration = 5

    # -------------------------
    # BACKGROUND
    # -------------------------

    bg_path = "sample.jpg"

    background = (
        ImageClip(bg_path)
        .with_duration(duration)
    )

    scale = max(
        WIDTH / background.w,
        HEIGHT / background.h
    )

    background = background.resized(scale)

    crop_x = (background.w - WIDTH) / 2
    crop_y = (background.h - HEIGHT) / 2

    background = background.cropped(
        x1=crop_x,
        y1=crop_y,
        x2=crop_x + WIDTH,
        y2=crop_y + HEIGHT
    )

    # -------------------------
    # OVERLAYS
    # -------------------------

    dark_overlay = (
        ColorClip(
            (WIDTH, HEIGHT),
            color=(0,0,0)
        )
        .with_opacity(0.25)
        .with_duration(duration)
    )

    bottom_gradient = create_bottom_gradient(
        duration
    )

    # -------------------------
    # SAMPLE CONTENT
    # -------------------------

    title = create_title_block(
        "DEVELOPED INDIA 2047 DEVELOPED INDIA 2047 ",
        duration
    )

    purpose = create_purpose_block(
        "Understand India's roadmap to become a developed nation.",
        duration
    )

    idea = create_key_idea_card(
        "Digital transformation is a core pillar of growth.",
        duration
    )

    number = create_number_card(
        "2047",
        duration
    )

    insight = create_insight_card(
        "Infrastructure expansion accelerated national growth.",
        duration
    )

    quote = create_quote_card(
        "The next 25 years will define India's future.",
        duration
    )

    outcome = create_outcome_card(
        "Learn how infrastructure and technology drive national development.",
        duration
    )

    footer = create_footer_bar(
        [
            "Digital India",
            "Infrastructure",
            "Growth",
            "2047"
        ],
        duration
    )

    rating_overlay = create_rating_overlay(
            100,
            duration
    )

    # -------------------------
    # COMPOSE
    # -------------------------

    preview = CompositeVideoClip(
        [
            background,
            dark_overlay,
            *rating_overlay,   
            title,
            purpose,
            idea,
            number,
            insight,
            quote,
            outcome,
            footer
        ],
        size=(WIDTH, HEIGHT)
    )

    preview.save_frame(
        "ui_preview.png",
        t=0
    )

    print(
        "Preview generated -> ui_preview.png"
    )


if __name__ == "__main__":
    build_preview()