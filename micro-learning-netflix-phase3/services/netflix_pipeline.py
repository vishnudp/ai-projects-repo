import json
from pathlib import Path

from services.hook_generator import generate_hook
from services.insight_generator import generate_insight
from services.cta_generator import create_cta_clip

from services.thumbnail_generator import (
    generate_thumbnail
)

from services.broll_generator import (
    generate_broll
)

from services.storyboard_generator import (
    generate_storyboard
)

from services.visual_planner import (
    generate_visual_plan
)

from services.reel_ranker import (
    rank_reel
)

from services.netflix_cache import (
    load_netflix,
    save_netflix
)

from services.parallel_executor import (
    run_parallel
)

OUTPUT_DIR = Path(
    "generated/netflix"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def run_netflix_pipeline(
    reel_file
):
    print("RUNNING NETFLIX PIPELINE")

    reel_data = json.loads(
        Path(reel_file).read_text()
    )

    chunk_no = reel_data[
        "chunk_number"
    ]

    # -------------------------
    # CACHE CHECK
    # -------------------------

    cached = load_netflix(
        chunk_no
    )

    cached = None

    if cached:

        print(
            f"NETFLIX CACHE HIT: {chunk_no}"
        )

        return cached

    print(
        f"NETFLIX CACHE MISS: {chunk_no}"
    )

    summary = reel_data[
        "summary"
    ]

    # -------------------------
    # PARALLEL GENERATION
    # -------------------------

    summary_text = json.dumps({
        "title": summary.get("title"),
        "key_insights": summary.get("key_insights"),
        "important_numbers": summary.get("important_numbers")
    })

    print(
        f"SUMMARY TEXT: {summary_text}"
    )

    tasks = {

        "hook":
            lambda:
                generate_hook(
                    summary_text
                ),

        "insight":
            lambda:
                generate_insight(
                    summary
                ),

        "cta":
            lambda:
                create_cta_clip(
                    summary
                ),

        "thumbnail":
            lambda:
                generate_thumbnail(
                    summary
                ),

        "broll":
            lambda:
                generate_broll(
                    summary
                )
    }

    results, total_time = (
        run_parallel(
            tasks
        )
    )

    print(
        f"Parallel Assets Generated "
        f"in {total_time:.2f}s"
    )

    hook = results[
        "hook"
    ]["output"]

    insight = results[
        "insight"
    ]["output"]

    cta = results[
        "cta"
    ]["output"]

    thumbnail = results[
        "thumbnail"
    ]["output"]

    broll = results[
        "broll"
    ]["output"]

    # -------------------------
    # STORYBOARD
    # -------------------------

    storyboard_input = {
        "hook": hook.get("hook", ""),
        "insight": insight.get("insight", ""),
        "cta": cta.get("cta", "")
    }

    storyboard = (
        generate_storyboard(
            json.dumps(
                storyboard_input,
                indent=2,
                ensure_ascii=False
            )
        )
    )

    # -------------------------
    # VISUAL PLAN
    # -------------------------

    visual_plan = (
        generate_visual_plan(
            storyboard
        )
    )

    # -------------------------
    # REEL SCORE
    # -------------------------

    score = rank_reel(
        {
            "hook":
                hook,

            "insight":
                insight,

            "cta":
                cta,

            "storyboard":
                storyboard,

            "thumbnail_prompt":
                thumbnail
        }
    )

    # -------------------------
    # OUTPUT
    # -------------------------

    netflix_output = {

        "chunk_number":
            chunk_no,

        "hook":
            hook,

        "insight":
            insight,

        "cta":
            cta,

        "thumbnail":
            thumbnail,

        "broll":
            broll,

        "storyboard":
            storyboard,

        "visual_plan":
            visual_plan,

        "reel_score":
            score
    }

    # -------------------------
    # SAVE GENERATED FILE
    # -------------------------

    output_file = (
        OUTPUT_DIR
        /
        f"reel_{chunk_no}_netflix.json"
    )

    with open(
        output_file,
        "w"
    ) as f:

        json.dump(
            netflix_output,
            f,
            indent=2,
            ensure_ascii=False
        )

    # -------------------------
    # SAVE CACHE
    # -------------------------

    save_netflix(
        chunk_no,
        netflix_output
    )

    print(
        f"NETFLIX SAVED: "
        f"{output_file}"
    )

    return netflix_output