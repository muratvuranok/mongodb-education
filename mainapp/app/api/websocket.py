from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from services.category import get_categories
from core.websocket import (
    remove_connection,
    add_connection,
)

router = APIRouter(prefix="/ws", tags=["WebSocket"])


@router.websocket("/categories")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    await add_connection(websocket)

    categories = get_categories(db)
    category_names = [category.name for category in categories]
    await websocket.send_text(f"Mevcut Kategoriler: {', '.join(category_names)}")

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await remove_connection(websocket)
        print("Bağlantı kesildi")
