from fastapi.staticfiles import StaticFiles
from routers.websockets import router as socket_router
from routers.api import router as api_router
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from supermiddleware import supermiddleware

import os
print("SUPABASE URL:", os.getenv("SUPABASE_URL"))
print("SUPABASE KEY:", os.getenv("SUPABASE_KEY")[:20])
app = FastAPI()
app.add_middleware(BaseHTTPMiddleware,supermiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router)
app.include_router(socket_router)
