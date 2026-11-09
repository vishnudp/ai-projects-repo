from pathlib import Path

from moviepy import VideoFileClip
from moviepy import ImageClip

import tempfile

COURSE_VIDEO_DIR = Path(
    "courses/developed_india_2047/videos"
)

TARGET_W = 1080

# top video area
VIDEO_AREA_HEIGHT = 700


def create_course_clip(
    scene,
    duration
):

    video_name = scene.get(
        "matched_video"
    )

    if not video_name:
        return None

    video_path = (
        COURSE_VIDEO_DIR /
        video_name
    )

    if not video_path.exists():
        return None

    try:

        clip = VideoFileClip(
            str(video_path)
        )

        start = float(
            scene.get(
                "video_start",
                0
            )
        )

        if start >= clip.duration:

            start = max(
                0,
                clip.duration - duration
            )

        end = min(
            start + duration,
            clip.duration
        )

        # ----------------------------------
        # REAL VIDEO CHUNK
        # ----------------------------------

        chunk = clip.subclipped(
            start,
            end
        )

        # ----------------------------------
        # FIT INSIDE TOP AREA
        # ----------------------------------

        scale = min(
            TARGET_W / chunk.w,
            VIDEO_AREA_HEIGHT / chunk.h
        )

        chunk = chunk.resized(scale)

        # ----------------------------------
        # CENTER HORIZONTALLY
        # TOP ALIGN VERTICALLY
        # ----------------------------------

        chunk = chunk.with_position(
            (
                (TARGET_W - chunk.w) / 2,
                0
            )
        )

        return chunk.with_duration(
            duration
        )

    except Exception as e:

        print(
            "Video chunk failed:",
            e
        )

        try:

            clip = VideoFileClip(
                str(video_path)
            )

            frame_file = tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False
            )

            clip.save_frame(
                frame_file.name,
                t=min(
                    start,
                    clip.duration - 1
                )
            )

            img = ImageClip(
                frame_file.name
            ).with_duration(
                duration
            )

            scale = min(
                TARGET_W / img.w,
                VIDEO_AREA_HEIGHT / img.h
            )

            img = img.resized(scale)

            img = img.with_position(
                (
                    (TARGET_W - img.w) / 2,
                    0
                )
            )

            return img

        except Exception as e2:

            print(
                "Frame fallback failed:",
                e2
            )

            return None