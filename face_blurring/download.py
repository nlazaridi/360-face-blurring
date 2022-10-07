import httpx

from .errors import DownloadError


def download_video(url) -> bytes:
    try:
        resp = httpx.get(url)
    except httpx.RequestError as e:
        raise DownloadError(f"Failed to download {url}") from e
    if not resp.is_success:
        raise DownloadError(f"Failed to download {url}")
    return resp.content
