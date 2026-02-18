import asyncio
import websockets

async def chat(user):
    uri = f"ws://localhost:8000/ws/{user}"

    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello everyone!")

        while True:
            msg = await websocket.recv()
            print(msg)
user=input("Enter username:")
asyncio.run(chat(user))