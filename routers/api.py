from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from socket_connections import manager
from models import *
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

router.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# Login page
@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Chat page
@router.get("/chat/{username}", response_class=HTMLResponse)
async def chat_page(request: Request, username: str):
    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "username": username}
    )

@router.get("/active-users-count")
async def get_active_users():
    count={
    "count": len(list(manager.active_connections.keys()))
    }
    print(count)
    datapipe=DataPipe(type="active-users-count",data=count)
    return datapipe.model_dump()

