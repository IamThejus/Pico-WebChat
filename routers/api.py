from fastapi import APIRouter
from fastapi.responses import FileResponse
from tools.socket_pico_connections import active_connections
from tools.superdb import *
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.responses  import Response
import requests


router=APIRouter()



# routers/api.py


@router.get("/api/history/public")
async def public_history():
    data = await get_public_chats()
    return JSONResponse(data or [])

@router.get("/api/history/private/{other_user}")
async def private_history(request: Request, other_user: str):
    username = getattr(request.state, "username", None)
    data = await get_private_chats(username, other_user)
    print("Username from state:", username)
    print("Cookies:", request.cookies)
    return JSONResponse(data or [])

@router.get("/api/history/pico")
async def pico_history(request: Request):
    username = getattr(request.state, "username", None)
    data = await get_pico(username)
    print(data)
    return JSONResponse(data or {"chat_history": []})


@router.get("/")
async def get_login():
    return FileResponse("templates/login.html")
    
@router.get("/chat/{username}")
async def get_chat(request:Request,response: Response,username:str):
    file_response=FileResponse("templates/chat.html")
    file_response.set_cookie(key="token",value=username)
    return file_response

@router.post('/setcookies')
async def setcookie(response:Response,request:Request,username:str):
    response.set_cookie(key="token",value=username)
    return f"Cookies set :{username}"

@router.get("/deletecookie")
async def get_chat(response:Response):
    response.delete_cookie("token")
    return "Cookie deleted successfully"


@router.get("/active-users-count")
async def active_users_count():
    return {"data": {"count": len(active_connections)}}