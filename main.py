from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import api, websockets

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(api.router)
app.include_router(websockets.router)
