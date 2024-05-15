import asyncio
import random
import datetime

clients = []
response_number = 0


async def handle_client(reader, writer):
    global response_number
    addr = writer.get_extra_info("peername")
    clients.append(writer)
    client_number = len(clients)
    print(f"Новый клиент {client_number} от {addr}")
    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            message = data.decode().strip()
            request_number = message.split()[0][1:-1]
            log_time = datetime.datetime.now()
            if random.random() <= 0.1:
                # print(f"Игнорируется запрос от клиента {client_number}: {message}")
                log(log_time, message, "(проигнорировано)")
                continue
            delay = random.randint(100, 1000) / 1000
            await asyncio.sleep(delay)
            response = f"[{response_number}/{request_number}] PONG ({client_number})\n"
            response_number += 1
            writer.write(response.encode())
            await writer.drain()
            log(log_time, message, response.strip())
    except asyncio.CancelledError:
        pass
    finally:
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()
        print(f"Клиент {client_number} отсоединился")


async def send_keepalive():
    global response_number
    while True:
        await asyncio.sleep(5)
        message = f"[{response_number}] keepalive\n"
        response_number += 1
        for client in clients:
            client.write(message.encode())
            await client.drain()
        # log(datetime.datetime.now(), "", message.strip())


def log(request_time, request_message, response_message):
    log_time = datetime.datetime.now()
    if response_message == "(проигнорировано)":
        log_entry = f"{request_time.strftime('%Y-%m-%d')};{request_time.strftime('%H:%M:%S.%f')[:-3]};{request_message};(проигнорировано)"
    else:
        log_entry = f"{request_time.strftime('%Y-%m-%d')};{request_time.strftime('%H:%M:%S.%f')[:-3]};{request_message};{log_time.strftime('%H:%M:%S.%f')[:-3]};{response_message}"
    # print(log_entry)
    with open("server_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry + "\n")


async def run_server():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 8888)
    async with server:
        try:
            await asyncio.gather(server.serve_forever(), send_keepalive())
        except asyncio.CancelledError:
            print("Сервер завершил работу!")


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server_task = loop.create_task(run_server())

    try:
        print("Сервер запущен!")
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nСервер прервался и корректно завершает работу...")
        server_task.cancel()
        loop.run_until_complete(server_task)
    finally:
        loop.close()


if __name__ == "__main__":
    main()
