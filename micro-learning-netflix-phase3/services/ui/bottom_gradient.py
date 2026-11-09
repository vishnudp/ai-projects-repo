from moviepy import *

def create_bottom_gradient(duration):

    return (
        ColorClip(
            size=(1080,1000),
            color=(0,0,0)
        )
        .with_opacity(0.55)
        .with_duration(duration)
        .with_position((0,920))
    )