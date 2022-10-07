from .models import ProblemJsonResponse


class FaceBlurringError(Exception):
    """Base exception for captioning errors."""

    def __init__(self, problemJSON: ProblemJsonResponse):
        super().__init__(problemJSON.detail)
        self.problemJSON = problemJSON


class DownloadError(FaceBlurringError):
    """Error downloading video."""
