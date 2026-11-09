def rank_reel(reel_json):

    score = 50

    hook = str(
        reel_json.get(
            "hook",
            ""
        )
    )

    insight = reel_json.get(
        "insight"
    )

    storyboard = reel_json.get(
        "storyboard"
    )

    thumbnail = reel_json.get(
        "thumbnail_prompt"
    )

    # Hook quality

    if len(hook) > 20:
        score += 15

    # Insight present

    if insight:
        score += 15

    # Storyboard quality

    scenes = []

    if isinstance(
        storyboard,
        dict
    ):
        scenes = storyboard.get(
            "scenes",
            []
        )

    if len(scenes) >= 6:
        score += 20

    # Thumbnail

    if thumbnail:
        score += 10

    # Bonus

    if len(hook) > 50:
        score += 5

    score = min(
        score,
        100
    )

    grade = "C"

    if score >= 90:
        grade = "A+"

    elif score >= 80:
        grade = "A"

    elif score >= 70:
        grade = "B"

    return {
        "score": score,
        "grade": grade
    }