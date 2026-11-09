from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class JobStage(str, Enum):
    INITIALIZING = "initializing"
    COLLECTING = "collecting"
    PROCESSING = "processing"
    EMBEDDING = "embedding"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ProgressState:
    stage: JobStage = JobStage.INITIALIZING
    progress: float = 0.0
    message: str = "Initializing"
    started_at: str | None = None
    updated_at: str | None = None

    def update(
        self,
        stage: JobStage,
        progress: float,
        message: str,
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()

        if not self.started_at:
            self.started_at = now

        self.updated_at = now
        self.stage = stage
        self.progress = max(
            0.0,
            min(100.0, progress),
        )
        self.message = message

    def snapshot(self) -> dict:
        return {
            "stage": self.stage.value,
            "progress": self.progress,
            "message": self.message,
            "started_at": self.started_at,
            "updated_at": self.updated_at,
        }


progress_state = ProgressState()