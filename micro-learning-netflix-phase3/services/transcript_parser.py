import re


def time_to_seconds(t):

    h, m, s = t.split(":")

    return (
        int(h) * 3600
        + int(m) * 60
        + float(s)
    )


def parse_vtt(content):

    segments = []

    lines = content.splitlines()

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        # skip WEBVTT
        if line.startswith("WEBVTT"):

            i += 1
            continue

        # skip cue numbers
        if line.isdigit():

            i += 1
            continue

        # timestamp line
        if "-->" in line:

            start, end = line.split("-->")

            start = time_to_seconds(
                start.strip()
            )

            end = time_to_seconds(
                end.strip()
            )

            i += 1

            text_lines = []

            while (
                i < len(lines)
                and lines[i].strip()
            ):

                text_lines.append(
                    lines[i].strip()
                )

                i += 1

            text = " ".join(text_lines)

            segments.append({

                "start": start,
                "end": end,
                "text": text

            })

        i += 1

    return segments