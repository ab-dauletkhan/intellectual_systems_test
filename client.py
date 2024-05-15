import asyncio
import random
import datetime


async def send_messages(reader, writer):
    request_number = 0
    try:
        while True:
            await asyncio.sleep(random.randint(300, 3000) / 1000)
            message = f"[{request_number}] PING\n"
            request_time = datetime.datetime.now()
            writer.write(message.encode())
            await writer.drain()
            log(request_time, message.strip(), "")
            try:
                data = await asyncio.wait_for(reader.readline(), timeout=3)
                response_time = datetime.datetime.now()
                response = data.decode().strip()
                log(request_time, message.strip(), response, response_time)
            except asyncio.TimeoutError:
                log(request_time, message.strip(), "(таймаут)")
            request_number += 1
    except asyncio.CancelledError:
        print("Клиентская задача была отменена")
    finally:
        writer.close()
        await writer.wait_closed()
        print("Клиент отсоединился")


def log(request_time, request_message, response_message, response_time=None):
    if response_time:
        log_entry = f"{request_time.strftime('%Y-%m-%d')};{request_time.strftime('%H:%M:%S.%f')[:-3]};{request_message};{response_time.strftime('%H:%M:%S.%f')[:-3]};{response_message}"
    else:
        log_entry = f"{request_time.strftime('%Y-%m-%d')};{request_time.strftime('%H:%M:%S.%f')[:-3]};{request_message};;{response_message}"
    # print(log_entry)
    with open("client_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry + "\n")


async def run_client():
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)
    try:
        await send_messages(reader, writer)
    except asyncio.CancelledError:
        print("Клиент отсоединился!")
    finally:
        writer.close()
        await writer.wait_closed()


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client_task = loop.create_task(run_client())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nКлиент отсоединяется...")
        client_task.cancel()
        loop.run_until_complete(client_task)
    finally:
        loop.close()


if __name__ == "__main__":
    main()
