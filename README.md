# PSBOT - Виртуальный психолог на базе Telegram и YandexGPT

## Описание

PSBOT - это Telegram-бот, который предоставляет пользователю возможность поговорить с виртуальным психологом, работающим на основе YandexGPT. Бот использует библиотеку `yandex_cloud_ml_sdk` для взаимодействия с YandexGPT и Telegram Bot API для обмена сообщениями с пользователем. Бот умеет поддерживать контекст диалога, запоминая предыдущие сообщения пользователя.

## Возможности

*   Общение с виртуальным психологом на базе YandexGPT.
*   Поддержка контекста диалога (история сообщений сохраняется для каждого пользователя).
*   Реагирует на команды `/start` и `/help`.

## Требования

*   Python 3.7+
*   Библиотеки:
    *   `telegram`
    *   `yandex_cloud_ml_sdk`
*   Аккаунт в Yandex Cloud с подключенным YandexGPT.
*   Telegram Bot API Token.
*   IAM-токен Yandex Cloud (или API-ключ).

## Установка

1.  Клонируйте репозиторий:

    ```bash
    git clone <URL вашего репозитория>
    cd PSBOT
    ```

2.  Создайте виртуальное окружение:

    ```bash
    python -m venv .venv
    ```

3.  Активируйте виртуальное окружение:

    *   Windows:

        ```bash
        .venv\Scripts\activate
        ```

    *   Linux/macOS:

        ```bash
        source .venv/bin/activate
        ```

4.  Установите необходимые библиотеки:

    ```bash
    pip install -r requirements.txt
    ```

    Если файла `requirements.txt` нет, создайте его и добавьте туда:

    ```
    telegram
    yandex-cloud-ml-sdk
    ```

    Затем выполните `pip install -r requirements.txt`

## Настройка

1.  **Получите Telegram Bot API Token:**
    *   Создайте нового бота в Telegram через BotFather и получите его токен.

2.  **Получите IAM-токен Yandex Cloud:**
    *   Следуйте инструкциям в документации Yandex Cloud, чтобы получить IAM-токен для вашего сервисного аккаунта. Убедитесь, что у сервисного аккаунта есть права на использование YandexGPT.

3.  **Укажите ID каталога Yandex Cloud:**
    *   Получите ID каталога, в котором у вас настроен YandexGPT.

4.  **Настройте переменные окружения (рекомендуется):**
    *   Установите переменные окружения `TELEGRAM_TOKEN` и `IAM_TOKEN` со значениями токена Telegram и IAM-токена Yandex Cloud, соответственно. Это более безопасно, чем хранить токены непосредственно в коде.
    *   В Windows:

        ```bash
        set TELEGRAM_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
        set IAM_TOKEN=YOUR_IAM_TOKEN
        ```

    *   В Linux/macOS:

        ```bash
        export TELEGRAM_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
        export IAM_TOKEN=YOUR_IAM_TOKEN
        ```

5.  **Настройте файл `botPs.py`:**
    *   Замените значения `TELEGRAM_TOKEN` и `IAM_TOKEN` в файле `botPs.py` на ваши значения.
    *   Замените значение `FOLDER_ID` в функции `main()` на ID вашего каталога Yandex Cloud.

## Запуск

1.  Убедитесь, что активировано виртуальное окружение.
2.  Запустите бота:

    ```bash
    python botPs.py
    ```

## Использование

1.  Запустите Telegram-бота.
2.  Начните общение с ботом в Telegram.
3.  Используйте команду `/start`, чтобы начать диалог.
4.  Используйте команду `/help`, чтобы получить помощь.
5.  Просто отправляйте боту сообщения, и он будет отвечать, используя YandexGPT.

## Структура проекта
