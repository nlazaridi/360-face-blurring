from fastapi.routing import APIRouter

router = APIRouter()


@router.get("/video_face_blurring")
def video_face_blurring():
    return {"message": "Hello World"}
