from PIL import Image
from PIL import ImageDraw

import tempfile

from moviepy import ImageClip


def create_card(
    width,
    height,
    color,
    radius,
    duration,
    border_color=None,
    border_width=0
):

    img = Image.new(
        "RGBA",
        (width, height),
        (0,0,0,0)
    )

    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle(
        (
            border_width,
            border_width,
            width-border_width,
            height-border_width
        ),
        radius=radius,
        fill=color,
        outline=border_color,
        width=border_width
    )

    tmp = tempfile.NamedTemporaryFile(
        suffix=".png",
        delete=False
    )

    img.save(tmp.name)

    return (
        ImageClip(tmp.name)
        .with_duration(duration)
    )