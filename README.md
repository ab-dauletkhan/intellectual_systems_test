# Тестовое задание ООО "Интеллектуальные системы"

## Описание

Проект состоит из сервера и двух клиентов, которые взаимодействуют через TCP соединение.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ab-dauletkhan/intellectual_systems_test
   # или
   gh repo clone ab-dauletkhan/intellectual_systems_test
   
   # дальше зайдите в директорию
   cd intellectual_systems_test
   ```
2. Установите зависимости с помощью Poetry:
    ```bash
    poetry install
    ```

## Использование

1. Запустите сервер и клиентов с помощью скрипта start.py:
    ```bash
    poetry run python start.py
    ```
    > Для остановки нажмите Ctrl+C. Скрипт завершит все процессы корректно.

## Структура проекта

- server.py: Код сервера
- client.py: Код клиента
- start.py: Скрипт для запуска сервера и клиентов
- pyproject.toml: Информация о проекте и зависимости


## Логирование

- Логи сервера сохраняются в `server_log.txt`.
- Логи клиентов сохраняются в `client_log.txt`.