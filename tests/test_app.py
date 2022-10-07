import pytest
from fastapi.testclient import TestClient

from face_blurring.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


def test_short_video(client):
    response = client.get(
        "/video_face_blurring",
        params={"url": "https://fs.mever.gr/media-annotation/short_video.mp4"},
    )
    assert response.status_code == 200
