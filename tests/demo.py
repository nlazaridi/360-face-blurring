import httpx

VIDEO_URL = "https://fs.mever.gr/media-annotation/short_video.mp4"


def demo_url():
    resp = httpx.get(
        "http://localhost:8080/video_face_blurring",
        params={"url": VIDEO_URL},
        timeout=300,
    )
    assert resp.status_code == 200
    with open("blurred_short_video.mp4", "wb") as f:
        f.write(resp.content)


def demo_bytes():
    resp = httpx.get(VIDEO_URL, timeout=300)
    assert resp.status_code == 200
    resp = httpx.post(
        "http://localhost:8080/video_face_blurring",
        data=resp.content,
        timeout=300,
    )
    assert resp.status_code == 200
    with open("blurred_short_video.mp4", "wb") as f:
        f.write(resp.content)


if __name__ == "__main__":
    demo_bytes()
