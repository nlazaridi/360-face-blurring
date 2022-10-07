from uvicorn.workers import UvicornWorker

from config import settings


class CustomUvicornWorker(UvicornWorker):
    """Wrapper of UvicornWorker class that custom config options.

    When application is executed under gunicorn, this worker class should be
    provided instead of uvicorn.workers.UvicornWorker.
    """

    CONFIG_KWARGS = {
        "timeout_keep_alive": settings.uvicorn.timeout_keep_alive,
    }
