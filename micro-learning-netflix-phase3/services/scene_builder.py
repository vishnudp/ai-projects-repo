from services.image_generator import (
    generate_scene_images
)

from services.narration_generator import (
    generate_scene_audio
)

from services.timestamp_mapper import (
    map_scene_to_video
)


def build_scenes(
    netflix_json
):
    insight = netflix_json.get(
    "insight",
        {}
    )

    reel_score = netflix_json.get(
        "reel_score",
        {}
    )

    broll_root = netflix_json.get(
        "broll",
        {}
    )

    broll_items = broll_root.get(
        "broll",
        []
    )
    storyboard = netflix_json.get(
        "storyboard",
        {}
    )

    scenes_data = (
        storyboard.get("scenes")
        or storyboard.get("storyboard")
        or []
    )

    scenes = []

    

    for idx, scene in enumerate(
        scenes_data
    ):

        # broll_data = {}

        # if idx < len(broll_items):

        #     broll_data = broll_items[idx]

        # print(
        #     broll_data
        # )

        voiceover = scene.get(
            "voiceover",
            ""
        )

        duration = max(
            len(
                voiceover.split()
            ) / 2.5,
            3
        )

        scene_obj = {

            "scene_no": idx + 1,

            # -------------------------
            # Scene data
            # -------------------------

           "title": scene.get("title", ""),

           "purpose": scene.get("purpose", ""),


            "key_ideas": scene.get("key_idea", ""),

            "key_insights": scene.get("key_insight", ""),

            "important_numbers": scene.get(
                "important_number",
                ""
            ),

            "important_quotes": scene.get(
                "important_quote",
                ""
            ),

            "learning_outcome": scene.get(
                "learning_outcome",
                ""
            ),

            "search_keywords": scene.get(
                "search_keywords",
                []
            ),

            "voiceover":
                voiceover,

            "duration":
                duration,

            # -------------------------
            # Reel score
            # -------------------------

            "rating":
                reel_score.get(
                    "score",
                    "9.4"
                ),

            "reel_score":
                reel_score.get(
                    "grade",
                    "A+"
                )
        }

        scene_obj = map_scene_to_video(
            scene_obj
        )

        scenes.append(
            scene_obj
        )
    print(
        f"Scenes Parsed: {len(scenes)}"
    )

    # -------------------------
    # Generate Images
    # -------------------------

    scenes = generate_scene_images(
        scenes
    )

    # print(
    #     "Image Generation Complete"
    # )

    # -------------------------
    # Generate Narration
    # -------------------------

    scenes = generate_scene_audio(
        scenes
    )

    print(
        "Narration Generation Complete"
    )

    # -------------------------
    # Valid Scenes Only
    # -------------------------

    valid_scenes = []

    for scene in scenes:

        if (
            scene.get("image_path")
            and
            scene.get("audio_path")
        ):

            valid_scenes.append(
                scene
            )

        else:

            print(
                f"Skipping Scene "
                f"{scene['scene_no']}"
            )

    print(
        f"Valid Scenes: "
        f"{len(valid_scenes)}"
    )

    print("\n========== VALID SCENES ==========\n")

    for scene in valid_scenes:

        print(
            "\n--------------------------------"
        )

        print(
            "Scene:",
            scene.get("scene_no")
        )

        print(
            "Title:",
            scene.get("title")
        )

        print(
            "Purpose:",
            scene.get("purpose")
        )

        print(
            "Key Ideas:",
            scene.get("key_ideas")
        )

        print(
            "Important Numbers:",
            scene.get("important_numbers")
        )

        print(
            "Key Insights:",
            scene.get("key_insights")
        )

        print(
            "Quotes:",
            scene.get("important_quotes")
        )

        print(
            "Learning Outcome:",
            scene.get("learning_outcome")
        )

        print(
            "Matched Video:",
            scene.get("matched_video")
        )

        print(
            "Video Start:",
            scene.get("video_start")
        )

        print(
            "Video End:",
            scene.get("video_end")
        )

        print(
            "Voiceover:",
            scene.get("voiceover")
        )

    return valid_scenes