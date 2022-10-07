class FaceBlurringError(Exception):
    """Base exception for captioning errors."""


class DownloadError(FaceBlurringError):
    """Error downloading video."""
