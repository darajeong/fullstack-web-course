from fastapi import FastAPI

from app.routers.member_router import router as member_router


app = FastAPI()

app.include_router(member_router)