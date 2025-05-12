from fastapi import FastAPI

from urban_eye.api.routers.user import router as user_router

app = FastAPI()


app.include_router(user_router)
