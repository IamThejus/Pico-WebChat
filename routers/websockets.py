from fastapi.websockets import WebSocket,WebSocketDisconnect
from fastapi import APIRouter
from models import *
from socket_connections import manager


router=APIRouter()

# WebSocket
@router.websocket("/ws/{user}")
async def websocket_endpoint(websocket: WebSocket, user: str):

    await websocket.accept()

    if user in manager.active_connections:
        datapipe = DataPipe(
            type="error",
            data={"log": "User already exists"}
        )
        await websocket.send_json(datapipe.model_dump())
        await websocket.close()
        return

    manager.active_connections[user] = websocket

    users = list(manager.active_connections.keys())

    datapipe = DataPipe(
        type="active-users-list",
        data={"users": users}
    )
    await manager.broadcast(datapipe)

    try:
        while True:
            data = await websocket.receive_json()

            sender = manager.get_user(websocket)
            get_type=data["type"]
            message = data["message"]

            if get_type=="public":
                # For sending public messages
                datamessage = DataMessagePublic(
                    message=message,
                    sender=sender
                )

                datapipe=DataPipe(type="message",data=datamessage.model_dump())
                await manager.broadcast(datapipe)

            else:
                #For sending  private messages
                datamessage=DataMessagePrivate(message=data["message"],receiver=data["receiver"],sender=sender)
                await manager.send_personal_message(datamessage)


    except WebSocketDisconnect:
        manager.disconnect(user)

        datapipe = DataPipe(
            type="active-users-list",
            data={"users": list(manager.active_connections.keys())}
        )
        print(datapipe)

        await manager.broadcast(datapipe)
