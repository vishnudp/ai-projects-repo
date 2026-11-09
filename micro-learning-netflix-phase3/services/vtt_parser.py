# services/vtt_parser.py

import re
import webvtt


class VTTParser:

    @staticmethod
    def timestamp_to_seconds(timestamp: str) -> float:
        """
        00:10:15.500 -> seconds
        """

        parts = timestamp.split(":")

        hours = int(parts[0])
        minutes = int(parts[1])

        seconds = float(parts[2])

        return (
            hours * 3600
            + minutes * 60
            + seconds
        )

    @staticmethod
    def clean_text(text: str) -> str:

        text = text.replace("\n", " ")

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def parse(self, vtt_path: str):

        transcript = []

        for caption in webvtt.read(vtt_path):

            transcript.append({

                "start": caption.start,

                "end": caption.end,

                "start_seconds":
                    self.timestamp_to_seconds(
                        caption.start
                    ),

                "end_seconds":
                    self.timestamp_to_seconds(
                        caption.end
                    ),

                "duration":
                    self.timestamp_to_seconds(
                        caption.end
                    )
                    -
                    self.timestamp_to_seconds(
                        caption.start
                    ),

                "text":
                    self.clean_text(
                        caption.text
                    )
            })

        return transcript