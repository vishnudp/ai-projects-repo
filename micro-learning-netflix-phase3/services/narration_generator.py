import asyncio
from pathlib import Path

import edge_tts

from moviepy import AudioFileClip


AUDIO_DIR = Path("generated/audio")
AUDIO_DIR.mkdir(
    parents=True,
    exist_ok=True
)


async def generate_voice(
    text,
    output_file
):
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-IN-NeerjaNeural"
    )

    await communicate.save(
        output_file
    )


def generate_scene_audio(
    scenes
):

    for scene in scenes:

        try:

            voiceover = scene.get(
                "voiceover",
                ""
            )

            if not voiceover:

                print(
                    f"Scene {scene['scene_no']} "
                    "has no voiceover"
                )

                continue

            output_file = (
                AUDIO_DIR
                /
                f"scene_{scene['scene_no']}.mp3"
            )

            print(
                f"Generating audio "
                f"for Scene "
                f"{scene['scene_no']}"
            )

            asyncio.run(
                generate_voice(
                    voiceover,
                    str(output_file)
                )
            )

            if not output_file.exists():

                print(
                    f"Audio not created "
                    f"for Scene "
                    f"{scene['scene_no']}"
                )

                continue

            audio = AudioFileClip(
                str(output_file)
            )

            scene["audio_path"] = str(
                output_file
            )

            scene["audio_duration"] = (
                audio.duration
            )

            audio.close()

            print(
                f"Audio OK "
                f"Scene {scene['scene_no']}"
            )

        except Exception as e:

            print(
                f"Audio failed "
                f"Scene {scene['scene_no']}"
            )

            print(e)

    return scenes