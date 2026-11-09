from services.video_retriever import (
    retrieve_best_segment
)


def map_scene_to_video(scene):

    search_text = " ".join([

        scene.get(
            "title",
            ""
        ),

        scene.get(
            "purpose",
            ""
        ),

        scene.get(
            "voiceover",
            ""
        )

    ])

    match = retrieve_best_segment(
        search_text
    )

    scene["matched_video"] = (
        match["video"]
    )

    scene["video_start"] = (
        match["start"]
    )

    scene["video_end"] = (
        match["end"]
    )

    return scene