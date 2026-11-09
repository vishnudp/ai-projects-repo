from moviepy import *
from pathlib import Path


def create_cover_clip(title):


    font_size = 60

    if len(title) > 50:
        font_size = 70

    if len(title) > 70:
        font_size = 60

    bg = ColorClip(
        size=(1080, 1920),
        color=(10, 10, 10)
    ).with_duration(2)

    # ----------------------------------
    # HOOK
    # ----------------------------------

    hook = TextClip(
        text="WAIT... THIS CHANGES\nEVERYTHING",
        font_size=62,
        color="#E50914",
        method="caption",
        size=(950, 220),
        text_align="center"
    ).with_position(
        ("center", 160)
    )

    # ----------------------------------
    # TITLE
    # ----------------------------------

    title_clip = TextClip(
        text=title.upper(),
        font_size=font_size,
        color="white",
        method="caption",
        size=(820, 650),
        text_align="center"
    ).with_position(
        ("center", 430)
    )

    print(font_size)

    # ----------------------------------
    # ICONS
    # ----------------------------------

    assets = Path(
        "generated/assets/icons"
    )

    follow_icon = (
        ImageClip(
            str(assets / "follow.png")
        )
        .resized(height=70)
        .with_position((250, 1380))
    )

    comment_icon = (
        ImageClip(
            str(assets / "comment.png")
        )
        .resized(height=70)
        .with_position((560, 1380))
    )

    share_icon = (
        ImageClip(
            str(assets / "share.png")
        )
        .resized(height=70)
        .with_position((250, 1520))
    )

    save_icon = (
        ImageClip(
            str(assets / "save.png")
        )
        .resized(height=70)
        .with_position((560, 1520))
    )

    # ----------------------------------
    # LABELS
    # ----------------------------------

    follow_txt = (
        TextClip(
            text="FOLLOW",
            font_size=45,
            color="white",
            size=(200, 60)
        )
        .with_position((330, 1390))
    )

    comment_txt = (
        TextClip(
            text="COMMENT",
            font_size=45,
            color="white",
            size=(280, 60)
        )
        .with_position((650, 1390))
    )

    share_txt = (
        TextClip(
            text="SHARE",
            font_size=45,
            color="white",
            size=(200, 60)
        )
        .with_position((330, 1530))
    )

    save_txt = (
        TextClip(
            text="SAVE",
            font_size=45,
            color="white",
            size=(200, 60)
        )
        .with_position((640, 1530))
    )

    print(save_txt.w, save_txt.h)

    return CompositeVideoClip(
        [
            bg,
            hook,
            title_clip,

            follow_icon,
            comment_icon,
            share_icon,
            save_icon,

            follow_txt,
            comment_txt,
            share_txt,
            save_txt
        ],
        size=(1080, 1920)
    ).with_duration(2)