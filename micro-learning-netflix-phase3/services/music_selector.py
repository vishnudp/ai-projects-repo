from moviepy import AudioFileClip


def load_background_music():

    return (
        AudioFileClip(
            "generated/assets/music/netflix_documentary.mp3"
        )
        .with_volume_scaled(
            0.15
        )
    )