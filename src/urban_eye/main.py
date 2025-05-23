from fastapi import FastAPI

from urban_eye.api.routers.user import router as user_router
from urban_eye.api.routers.camera import router as camera_router
from urban_eye.api.routers.auth import router as auth_router
from urban_eye.api.routers.video import router as video_router


app = FastAPI()


app.include_router(user_router)
app.include_router(camera_router)
app.include_router(auth_router)
app.include_router(video_router)