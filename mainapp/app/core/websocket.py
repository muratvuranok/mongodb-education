from fastapi import WebSocket

active_connections = []


async def add_connection(websocket: WebSocket):
    active_connections.append(websocket)


async def remove_connection(websocket: WebSocket):
    active_connections.remove(websocket)


async def broadcast_message(message: str):
    for connection in active_connections:
        await connection.send_text(message)
