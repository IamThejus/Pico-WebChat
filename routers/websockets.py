from fastapi import APIRouter
from tools.socket_pico_connections import active_connections,pico_connections
from fastapi.websockets import WebSocket,WebSocketDisconnect
from tools.superdb import *
import  json
from tools.pico_ai import *
import asyncio





router=APIRouter()


@router.websocket("/ws/{username}")
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
    pico_msg=await get_pico(username)
    if pico_msg:
        pico_connections[username]=PicoAI()
        pico_connections[username].chat_history=pico_msg["chat_history"]
    else:
        pico_connections[username]=PicoAI()
        pico_connections[username].chat("My name is "+str(username))
        pico_connections[username].chat(PICO_SYSTEM_PROMPT)
    asyncio.create_task(add_pico(username=username))

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
                asyncio.create_task(add_public_message(username=username,message=data.get("message","")))
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
                    asyncio.create_task(update_pico_chat(username=username,chat=pico_agent.chat_history))
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
                        asyncio.create_task(add_private_message(sender=username,receiver=receiver,message=data.get("message","")))
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
