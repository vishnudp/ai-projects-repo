from moviepy import *


def create_social_overlay(duration):

    icons = []

    positions = [

        ("follow.png",600),
        ("comment.png",700),
        ("share.png",800),
        ("save.png",900)

    ]

    for file,y in positions:

        icons.append(

            ImageClip(
                f"generated/assets/icons/{file}"
            )

            .resized(width=80)

            .with_duration(duration)

            .with_position((970,y))

        )

    return CompositeVideoClip(
        icons,
        size=(1080,1920)
    )