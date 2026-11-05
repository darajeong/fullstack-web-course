from fastapi import FastAPI
from .routers import members

app = FastAPI()
app.include_router(members.router)