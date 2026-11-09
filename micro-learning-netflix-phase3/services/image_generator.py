from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

IMAGE_DIR = Path(
    "generated/images"
)

IMAGE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def download_placeholder(
    scene_no,
    output_path
):

    try:

        url = (
            f"https://picsum.photos/1080/1920?random={scene_no}"
        )

        print(
            f"Downloading image for scene {scene_no}"
        )

        response = requests.get(
            url,
            timeout=15
        )

        response.raise_for_status()

        with open(
            output_path,
            "wb"
        ) as f:

            f.write(
                response.content
            )

        print(
            f"Image saved: {output_path}"
        )

        return str(
            output_path
        )

    except Exception as e:

        print(
            f"Image generation failed for scene "
            f"{scene_no}: {e}"
        )

        return None


def generate_scene_images(
    scenes
):

    def process(scene):

        output_path = (
            IMAGE_DIR
            /
            f"scene_{scene['scene_no']}.jpg"
        )

        image_path = download_placeholder(
            scene["scene_no"],
            output_path
        )

        if image_path:

            scene["image_path"] = image_path

        else:

            scene["image_path"] = None

        return scene

    generated_scenes = []

    with ThreadPoolExecutor(
        max_workers=4
    ) as executor:

        futures = [

            executor.submit(
                process,
                scene
            )

            for scene in scenes
        ]

        for future in as_completed(
            futures
        ):

            try:

                generated_scenes.append(
                    future.result(
                        timeout=20
                    )
                )

            except Exception as e:

                print(
                    f"Scene image timeout: {e}"
                )

    generated_scenes = sorted(
        generated_scenes,
        key=lambda x: x["scene_no"]
    )

    print(
        f"Generated Images: "
        f"{len(generated_scenes)}"
    )

    return generated_scenes