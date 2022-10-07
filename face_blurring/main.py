import logging
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from face_blurring.models import ProblemJsonResponse

from .custom_logging import RequestInfo, ctx_request, setup_logging
from .errors import FaceBlurringError
from .video_face_blurring import router as video_face_blurring_router

logger = logging.getLogger("augmented")
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

    logger.info("Received request")
    response = await call_next(request)
    process_time = time.monotonic() - start_time
    logger.info(f"Request took {process_time} seconds")

    return response


@app.on_event("startup")
def initialize_model():
    pass


@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    logger.error(str(exc))
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


@app.exception_handler(FaceBlurringError)
async def face_blurring_exception_handler(request, exc):
    logger.exception("Face Blurring Error")
    problemJSON = exc.problemJSON
    return JSONResponse(
        content=jsonable_encoder(problemJSON),
        status_code=problemJSON.status,
        media_type="application/problem+json",
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
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
    uvicorn.run("face_blurring.main:app", host="0.0.0.0", port=52512, reload=True)
