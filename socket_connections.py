from fastapi.websockets import WebSocket,WebSocketDisconnect
from typing import Dict
from models  import *

class ConnectionManager:
    def __init__(self):
        self.active_connections:Dict[str,WebSocket]={}

    async def connect(self,user:str,websocket:WebSocket) -> bool:
        if user in self.active_connections.keys():
            return False
        await websocket.accept()
        self.active_connections[user]=websocket
        return True

    def disconnect(self,user):
        self.active_connections.pop(user,None)
    
    # To get username from socketObject
    def get_user(self,websocket:WebSocket) -> str|None:
        for user in self.active_connections:
            if self.active_connections[user]==websocket:
                return user
        return None
    
    async def send_personal_message(self,privatemessage:DataMessagePrivate):
        websocket=self.active_connections.get(privatemessage.receiver)
        datapipe=DataPipe(type="message",data=privatemessage.model_dump())
        if websocket:
            await websocket.send_json(datapipe.model_dump())
    
    
    async def broadcast(self,datapipe:DataPipe):
        for websocket in self.active_connections.values():
            await websocket.send_json(datapipe.model_dump())

manager=ConnectionManager()