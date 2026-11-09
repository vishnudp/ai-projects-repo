from pathlib import Path

from moviepy import *

from moviepy.video.fx.Resize import Resize


BROLL_DIR = Path(
    "generated/broll"
)


def get_broll_for_scene(scene):

    keyword = (
        scene.get("broll")
        or scene.get("title", "")
    ).lower()

    mapping = {

        "ai": "ai.mp4",
        "india": "india.mp4",
        "startup": "startup.mp4",
        "economy": "economy.mp4",
        "city": "city.mp4"

    }

    
    for key, file in mapping.items():

        if key in keyword:

            return str(
                BROLL_DIR / file
            )

    return None


def create_broll_clip(
    scene,
    duration
):

    video_path = get_broll_for_scene(
        scene
    )

    if not video_path:

        return None

    clip = VideoFileClip(
        video_path
    )

    clip = (
        clip
        .subclipped(
            0,
            min(
                duration,
                clip.duration
            )
        )
        .resized(height=1920)
    )

    # -------------------
    # Center crop
    # -------------------

    if clip.w > 1080:

        x1 = (
            clip.w - 1080
        ) / 2

        clip = clip.cropped(
            x1=x1,
            y1=0,
            x2=x1 + 1080,
            y2=1920
        )

    # -------------------
    # Ken Burns Zoom
    # -------------------

    clip = clip.with_effects([

        Resize(

            lambda t:

            1.0 +

            (

                0.12 *

                (
                    t /
                    duration
                )

            )

        )

    ])

    return clip.with_duration(
        duration
    )