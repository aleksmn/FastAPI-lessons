import asyncio
import sys
import websockets


async def listen(websocket):
    """Фоновый слушатель: выводит сообщения"""
    try:
        async for message in websocket:
            # Стираем текущую строку (затираем пробелами)
            sys.stdout.write('\r' + ' ' * 80 + '\r')
            # Выводим полученное сообщение
            print(message)
            # Снова выводим приглашение
            print("Введите сообщение: ", end="", flush=True)
    except websockets.exceptions.ConnectionClosed:
        print("\n❌ Соединение потеряно.")
        sys.exit(0)


async def main():
    username = input("👤 Ваше имя: ")
    server_url = input("🌍 Адрес сервера (wss://... или ws://...): ")
    # Сервер по умолчанию, для локальных тестов
    if not server_url:
        server_url = "ws://localhost:8000"

    uri = f"{server_url}/chat/{username}"
    print(f"Подключение к {uri}...")

    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Подключено! Введите 'exit' для выхода.\n")
            # Печатаем первое приглашение
            print("Введите сообщение: ", end="", flush=True)

            # Запускаем слушателя
            listener = asyncio.create_task(listen(websocket))

            while True:
                # Читаем ввод без собственного приглашения
                user_input = await asyncio.to_thread(sys.stdin.readline)
                user_input = user_input.rstrip('\n')
                if user_input.lower() == "exit":
                    break
                if user_input == "":
                    # Пустое сообщение не отправляем
                    continue
                await websocket.send(user_input)
                # После отправки снова показываем приглашение
                print("Введите сообщение: ", end="", flush=True)

            listener.cancel()
            await websocket.close()

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
