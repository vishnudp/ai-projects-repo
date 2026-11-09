from datetime import datetime


class StageTracker:

    def __init__(self):

        self.pipeline_start = datetime.now()

    def start(self, stage):

        self.stage = stage

        self.start_time = datetime.now()

        return self.start_time

    def end(self):

        end_time = datetime.now()

        duration = (
            end_time - self.start_time
        ).total_seconds()

        return {
            "stage": self.stage,
            "start": self.start_time,
            "end": end_time,
            "duration": duration
        }