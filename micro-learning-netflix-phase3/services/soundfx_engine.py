from moviepy import AudioFileClip


def load_transition_sfx():

    return (
        AudioFileClip(
            "generated/assets/sfx/whoosh.mp3"
        )
        .with_volume_scaled(
            0.25
        )
    )