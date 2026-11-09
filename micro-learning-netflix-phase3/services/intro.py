from moviepy import *

from pathlib import Path

from services.light_sweep import (
    create_light_sweep
)

from moviepy.video.fx.Resize import Resize


def create_intro():

    duration = 2.8

    # ----------------------------------
    # Background
    # ----------------------------------

    bg = (
        ColorClip(
            size=(1080, 1920),
            color=(0, 0, 0)
        )
        .with_duration(duration)
    )

    # ----------------------------------
    # Logo Scale Animation
    # ----------------------------------

    def scale(t):

        if t < 1.0:

            return 0.15 + (
                0.85 * (t / 1.0)
            )

        elif t < 1.4:

            return 1.10

        elif t < 2.2:

            return 1.00

        else:

            return 1.00 + (
                0.05 *
                ((t - 2.2) / 0.6)
            )

    # ----------------------------------
    # Main Logo
    # ----------------------------------

    logo = (

        ImageClip(
            "generated/assets/logo.png"
        )

        .with_duration(duration)

        .with_position("center")

        .with_opacity(1)

    )

    logo = logo.with_effects([
        Resize(
            lambda t: (
                0.15 + (0.85 * (t / 1.0))
                if t < 1.0
                else 1.10
                if t < 1.4
                else 1.00
                if t < 2.2
                else 1.00 + (0.05 * ((t - 2.2) / 0.6))
            )
        )
    ])

    # ----------------------------------
    # Glow Behind Logo
    # ----------------------------------

    glow = (

        ImageClip(
            "generated/assets/logo.png"
        )

        .with_duration(duration)

        .with_position("center")

        .with_opacity(0.20)

    )

    glow = glow.with_effects([
        Resize(
            lambda t: (
                (
                    0.15 + (0.85 * (t / 1.0))
                )
                if t < 1.0
                else 1.10
                if t < 1.4
                else 1.00
                if t < 2.2
                else 1.00 + (0.05 * ((t - 2.2) / 0.6))
            ) * 1.2
        )
    ])

    # ----------------------------------
    # Light Sweep
    # ----------------------------------

    light = ColorClip(
        size=(1, 1),
        color=(0, 0, 0)
    ).with_duration(duration).with_opacity(0)

    # ----------------------------------
    # Intro Composite
    # ----------------------------------

    intro = CompositeVideoClip(

        [
            bg,
            glow,
            light,
            logo
        ],

        size=(1080, 1920)

    )

    # ----------------------------------
    # Audio
    # ----------------------------------

    whoosh = Path(
        "generated/assets/audio/sfx/whoosh.mp3"
    )

    if whoosh.exists():

        intro = intro.with_audio(

            AudioFileClip(
                str(whoosh)
            ).subclipped(
                0,
                duration
            )

        )

    return intro