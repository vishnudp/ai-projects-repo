from moviepy import *

def create_dark_gradient(duration):

    return (
        ColorClip(
            (1080,1920),
            color=(0,0,0)
        )
        .with_opacity(0.35)
        .with_duration(duration)
    )