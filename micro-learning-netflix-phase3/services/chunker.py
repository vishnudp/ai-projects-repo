from datetime import timedelta


def to_seconds(timestamp):

    h, m, s = timestamp.split(":")

    return int(h) * 3600 + int(m) * 60 + float(s)


def create_chunks(
    transcript,
    chunk_size=600
):

    chunks = []

    current = []

    start_time = 0

    for item in transcript:

        sec = to_seconds(item["start"])

        if sec > start_time + chunk_size:

            chunks.append(current)

            current = []

            start_time = sec

        current.append(item)

    if current:

        chunks.append(current)

    return chunks