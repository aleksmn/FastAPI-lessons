from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        # Список активных подключений
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # Принимаем соединение и добавляем его в список
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        # Удаляем соединение из списка при отключении
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # Отправляем сообщение всем подключённым пользователям
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                # Если отправить не удалось, просто пропускаем
                print(e)
                pass


manager = ConnectionManager()


@app.websocket("/chat/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    # Подключаем нового пользователя
    await manager.connect(websocket)
    # Оповещаем всех о его приходе
    await manager.broadcast(
        f"🔵 Пользователь '{username}' присоединился к чату!")

    try:
        # Бесконечно ждём сообщения от этого клиента
        while True:
            data = await websocket.receive_text()
            # Пересылаем сообщение всем остальным
            await manager.broadcast(f"💬 {username}: {data}")

    except WebSocketDisconnect:
        # Если соединение разорвано, удаляем пользователя и сообщаем об этом
        manager.disconnect(websocket)
        await manager.broadcast(f"🔴 Пользователь '{username}' покинул чат.")
