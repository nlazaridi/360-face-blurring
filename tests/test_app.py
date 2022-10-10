import pytest
import requests
from fastapi.testclient import TestClient

from face_blurring.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


def test_short_video_url(client):
    response = client.get(
        "/video_face_blurring",
        params={"url": "https://fs.mever.gr/media-annotation/short_video.mp4"},
    )
    assert response.status_code == 200


def test_short_video_bytes(client):
    response = requests.get("https://fs.mever.gr/media-annotation/short_video.mp4")
    assert response.status_code == 200

    response = client.post("/video_face_blurring", data=response.content)
    assert response.status_code == 200
