from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from typing import Dict
import json
from pico_ai import *
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")




# Track connected users: username -> WebSocket
active_connections: Dict[str, WebSocket] = {}
pico_connections: Dict[str,PicoAI]={}

@app.get("/")
async def get_login():
    return FileResponse("templates/login.html")


@app.get("/chat/{username}")
async def get_chat(username: str):
    return FileResponse("templates/chat.html")


@app.get("/active-users-count")
async def active_users_count():
    return {"data": {"count": len(active_connections)}}


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    # Reject duplicate usernames
    if username in active_connections:
        await websocket.accept()
        await websocket.send_text(json.dumps({
            "type": "error",
            "data": {"log": f'Username "{username}" is already taken. Please choose another.'}
        }))
        await websocket.close()
        return

    await websocket.accept()
    active_connections[username] = websocket
    pico_connections[username]=PicoAI()
    pico_connections[username].chat("My name is "+str(username))

    # Notify everyone of updated user list
    await broadcast_user_list()

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)

            if data.get("type") == "public":
                # Broadcast to all connected users
                payload = json.dumps({
                    "type": "message",
                    "data": {
                        "type": "public",
                        "sender": username,
                        "message": data.get("message", "")
                    }
                })
                for user, ws in list(active_connections.items()):
                    try:
                        await ws.send_text(payload)
                    except Exception:
                        pass

            elif data.get("type") == "private":
                receiver = data.get("receiver")
                if receiver=="PICO":
                    pico_agent=pico_connections[username]
                    response=pico_agent.chat(data["message"])
                    payload = json.dumps({
                            "type": "message",
                            "data": {
                                "type": "private",
                                "sender": "PICO",
                                "message": response
                            }
                        })
                    await active_connections[username].send_text(payload)
                    
                else:
                    if receiver and receiver in active_connections:
                        payload = json.dumps({
                            "type": "message",
                            "data": {
                                "type": "private",
                                "sender": username,
                                "message": data.get("message", "")
                            }
                        })
                        await active_connections[receiver].send_text(payload)

    except WebSocketDisconnect:
        pass
    finally:
        active_connections.pop(username, None)
        await broadcast_user_list()


async def broadcast_user_list():
    users=list(active_connections.keys())
    users.append("PICO")
    payload = json.dumps({
        "type": "active-users-list",
        "data": {"users": users}
    })
    for ws in list(active_connections.values()):
        try:
            await ws.send_text(payload)
        except Exception:
            pass
