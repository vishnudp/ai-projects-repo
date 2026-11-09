def build_word_subtitles(
    text,
    duration
):

    words = text.split()

    if not words:
        return []

    per_word = duration / len(words)

    subtitles = []

    for idx, word in enumerate(words):

        subtitles.append({

            "text":
                word.upper(),

            "start":
                idx * per_word,

            "end":
                (idx + 1) * per_word
        })

    return subtitles


# backward compatibility
def build_subtitles(
    scenes
):
    return scenes