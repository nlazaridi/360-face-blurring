import io
import logging
import tempfile

import cv2
import numpy as np
from fastapi import Depends, Request
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter
from PIL import Image, ImageDraw, ImageFilter

from .download import download_video
from .errors import FaceBlurringError

augmented_logger = logging.getLogger("augmented")

router = APIRouter()


async def get_body(request: Request):
    return await request.body()


@router.get("/video_face_blurring")
def get_video_face_blurring(request: Request, url: str):
    augmented_logger.debug(f"Dowloading video from {url}")
    video = download_video(url)
    augmented_logger.debug(f"Downloaded {len(video)} bytes from {url}")
    with tempfile.NamedTemporaryFile() as temp:
        augmented_logger.debug(f"Saving video to {temp.name}")
        temp.write(video)
        temp.seek(0)
        augmented_logger.debug("Blurring video")
        try:
            blurred_video = blur_video(request.app.state.model, temp.name)
        except Exception as e:
            raise FaceBlurringError("An error occured while blurring the video") from e
        augmented_logger.debug("Finished blurring video")

    return StreamingResponse(io.BytesIO(blurred_video), media_type="video/mp4")


@router.post("/video_face_blurring")
def post_video_face_blurring(request: Request, video: bytes = Depends(get_body)):
    with tempfile.NamedTemporaryFile() as temp:
        augmented_logger.debug(f"Saving video to {temp.name}")
        temp.write(video)
        temp.seek(0)
        augmented_logger.debug("Blurring video")
        try:
            blurred_video = blur_video(request.app.state.model, temp.name)
        except Exception as e:
            raise FaceBlurringError("An error occured while blurring the video") from e
        augmented_logger.debug("Finished blurring video")

    return StreamingResponse(io.BytesIO(blurred_video), media_type="video/mp4")


def blur_video(model, video_path) -> bytes:
    videocap = cv2.VideoCapture(video_path)
    fps = videocap.get(cv2.CAP_PROP_FPS)

    success, image = videocap.read()

    count = 0
    i = 0
    bboxes = {}
    with tempfile.NamedTemporaryFile(suffix=".mp4") as temp:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_tracked = cv2.VideoWriter(
            temp.name, fourcc, fps, (image.shape[1], image.shape[0])
        )
        while success:
            count = count + 1
            frame = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            img = np.array(frame)

            faces = model_inf(model, img)

            boxes = []
            for f in range(len(faces)):
                boxes.append(faces[f].tolist())

            # append the dictionary with the bboxes
            i = i + 1
            bboxes["frame_" + str(i + 1)] = boxes

            # Draw faces
            frame_draw = frame.copy()

            mask = Image.new("L", frame_draw.size, 0)
            draw = ImageDraw.Draw(mask)

            if boxes is not None:
                for box in boxes:
                    draw.ellipse(box, fill=255)

            blurred = frame_draw.filter(ImageFilter.GaussianBlur(52))
            frame_draw.paste(blurred, mask=mask)

            video_tracked.write(cv2.cvtColor(np.array(frame_draw), cv2.COLOR_RGB2BGR))

            success, image = videocap.read()

        video_tracked.release()

        temp.seek(0)
        return temp.read()


def model_inf(model, img):
    bboxes, _ = model.detect(img, max_num=0, metric="default")
    if bboxes.shape[0] == 0:
        return []
    ret = []
    for i in range(bboxes.shape[0]):
        bbox = bboxes[i, 0:4]
        ret.append(bbox)

    return ret
