import logging
import time

import onnxruntime
import uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from config import settings

from .custom_logging import RequestInfo, ctx_request, setup_logging
from .errors import DownloadError
from .models import ProblemJsonResponse
from .SCRFD import SCRFD
from .video_face_blurring import router as video_face_blurring_router

DETECTION_SIZE = settings.model.detection_size
DETECTION_THRESHOLD = settings.model.detection_threshold
GPU = settings.model.gpu
MODEL_FILE = settings.model.file

augmented_logger = logging.getLogger("augmented")
simple_logger = logging.getLogger(__name__)
setup_logging()

app = FastAPI(
    version="0.1.0",
    title="Face Blurring API",
    contact={"name": "Panagiotis Galopoulos", "email": "gpan@iti.gr"},
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.monotonic()

    peer = ""
    if request.client:
        peer = f"{request.client.host}:{request.client.port}"
    ctx_request.set(
        RequestInfo(
            path=request.url.path,
            query=request.url.query,
            peer=peer,
        )
    )

    augmented_logger.info("Received request")
    response = await call_next(request)
    process_time = time.monotonic() - start_time
    augmented_logger.info(f"Request took {process_time} seconds")

    return response


@app.on_event("startup")
def initialize_model():
    simple_logger.info("Initializing model")
    onnxruntime.set_default_logger_severity(3)
    if GPU:
        onnx_providers = ["CUDAExecutionProvider"]
    else:
        onnx_providers = ["CPUExecutionProvider"]
    onnx_session = onnxruntime.InferenceSession(
        MODEL_FILE,
        providers=onnx_providers,
        provider_options=None,
    )
    app.state.model = SCRFD(MODEL_FILE, onnx_session)
    if GPU:
        app.state.model.prepare(
            0, input_size=DETECTION_SIZE, det_threshold=DETECTION_THRESHOLD
        )
    else:
        app.state.model.prepare(
            -1, input_size=DETECTION_SIZE, det_threshold=DETECTION_THRESHOLD
        )
    simple_logger.info("Model initialized")


@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    augmented_logger.exception("Unhandled exception")
    problemJSON = ProblemJsonResponse(
        type="/problems/InternalError",
        title="Internal error",
        status=500,
        detail=f"An internal error occured; {str(exc)}",
    )
    return JSONResponse(
        content=jsonable_encoder(problemJSON),
        status_code=problemJSON.status,
        media_type="application/problem+json",
    )


@app.exception_handler(DownloadError)
async def download_exception_handler(request, exc):
    augmented_logger.exception("Download error")
    problemJSON = ProblemJsonResponse(
        type="/problems/BadRequest",
        title="Bad Request",
        status=400,
        detail=f"An error occured while downloading the video; {str(exc)}",
    )
    return JSONResponse(
        content=jsonable_encoder(problemJSON),
        status_code=problemJSON.status,
        media_type="application/problem+json",
    )


@app.exception_handler(RequestValidationError)
async def http_exception_handler(request, exc):
    problemJSON = ProblemJsonResponse(
        type="/problems/BadRequest",
        title="Bad Request",
        status=422,
        detail="Request validation error",
    )
    return JSONResponse(
        content=jsonable_encoder(problemJSON),
        status_code=problemJSON.status,
        media_type="application/problem+json",
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    augmented_logger.exception("HTTP error")
    problemJSON = ProblemJsonResponse(
        type="/problems/BadRequest",
        title="Bad Request",
        status=exc.status_code,
        detail=str(exc.detail),
    )
    return JSONResponse(
        content=jsonable_encoder(problemJSON),
        status_code=problemJSON.status,
        media_type="application/problem+json",
    )


app.include_router(video_face_blurring_router)


if __name__ == "__main__":
    uvicorn.run("face_blurring.main:app", host="0.0.0.0", port=52512, reload=False)
