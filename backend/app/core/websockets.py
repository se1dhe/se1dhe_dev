from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from typing import Dict, List
import logging
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.core.security import get_current_user_ws
from backend.app.models.user import User

logger = logging.getLogger(__name__)

websocket_router = APIRouter()

# Активные соединения
active_connections: Dict[int, List[WebSocket]] = {}


async def connect_user(websocket: WebSocket, user_id: int):
    await websocket.accept()
    if user_id not in active_connections:
        active_connections[user_id] = []
    active_connections[user_id].append(websocket)
    logger.info(f"User {user_id} connected. Active connections: {len(active_connections)}")


async def disconnect_user(websocket: WebSocket, user_id: int):
    if user_id in active_connections:
        active_connections[user_id].remove(websocket)
        if not active_connections[user_id]:
            del active_connections[user_id]
    logger.info(f"User {user_id} disconnected. Active connections: {len(active_connections)}")


async def broadcast_to_user(user_id: int, message: dict):
    if user_id in active_connections:
        for connection in active_connections[user_id]:
            await connection.send_json(message)


async def broadcast_to_all(message: dict):
    for user_id in active_connections:
        for connection in active_connections[user_id]:
            await connection.send_json(message)


@websocket_router.websocket("/ws/notifications")
async def websocket_notifications(
        websocket: WebSocket,
        token: str = None,
        db: Session = Depends(get_db)
):
    try:
        # Аутентификация пользователя по токену
        if not token:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        current_user = await get_current_user_ws(token=token, db=db)
        if not current_user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        await connect_user(websocket, current_user.id)

        try:
            while True:
                # Ждем сообщения от клиента
                data = await websocket.receive_json()
                # Обработка команд от клиента
                if data.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
        except WebSocketDisconnect:
            await disconnect_user(websocket, current_user.id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)