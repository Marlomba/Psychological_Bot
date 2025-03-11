import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import json
from yandex_cloud_ml_sdk import YCloudML  # Импортируем библиотеку

# Замените на свой токен телеграм-бота
TELEGRAM_TOKEN = "7908158612:AAHzMDJ1chi2pnrxnNm-cZGn1-bzKbLJkhU"

# Замените на свой IAM-токен Yandex Cloud
IAM_TOKEN = "t1.9euelZqPisiXm5jOjczHlJKcyYqQiu3rnpWalo6ai5XPkcuLyZyOm5PLmMrl9Pd4Rj9B-e9nSSre3fT3OHU8QfnvZ0kq3s3n9euelZrKnsbOyIyKkciPkcabzcbJl-_8xeuelZrKnsbOyIyKkciPkcabzcbJlw.uT8yCSX1fjrDMXP6TJz5bm7UYmi0vjCsXGWQgxvpJgsGLvoqzP6uEp07UmPNmDoi-cL0_Q6ZHZ3NGkQy9-ZCDQ"

# Хранилище истории сообщений (простой словарь)
user_messages = {}

def get_response(user_message, folder_id, chat_history=None):
    """Получает ответ от YandexGPT."""
    try:
        sdk = YCloudML(folder_id=folder_id, auth=IAM_TOKEN)
        model = sdk.models.completions("llama-lite", model_version="latest") # Используем llama-lite
        model = model.configure(temperature=0.7)

        messages = []
        # Добавляем промт (роль психолога)
        messages.append({"role": "system", "text": "Ты - опытный и сочувствующий психолог.  Отвечай на сообщения пользователей, стараясь понять их чувства и предложить поддержку и советы.  Избегай общих фраз и предлагай конкретные способы решения проблем."})

        if chat_history:
            messages.extend(chat_history) # Добавляем историю сообщений
        messages.append({"role": "user", "text": user_message}) # Добавляем сообщение пользователя

        result = model.run(messages)
        print(f"Ответ от YandexGPT (SDK): {result}")  # Добавлено для отладки
        return result[0].text.strip()  # Получаем текст из объекта Alternative

    except Exception as e:
        print(f"Ошибка YandexGPT (SDK): {e}")
        return "Произошла ошибка при обращении к YandexGPT. Попробуйте позже."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start."""
    await update.message.reply_text("Привет! Я твой виртуальный психолог. Расскажи, что тебя беспокоит.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help."""
    await update.message.reply_text("Я могу помочь тебе разобраться в своих чувствах. Просто напиши мне, что тебя беспокоит.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик всех текстовых сообщений."""
    folder_id = context.bot_data['folder_id']
    user_id = update.message.from_user.id # Получаем ID пользователя
    user_message = update.message.text

    # Получаем историю сообщений для пользователя
    if user_id not in user_messages:
        user_messages[user_id] = [] # Создаем историю, если ее нет
    chat_history = user_messages[user_id]

    # Получаем ответ от YandexGPT, передавая историю
    bot_response = get_response(user_message, folder_id, chat_history)

    # Добавляем сообщение пользователя и ответ бота в историю
    chat_history.append({"role": "user", "text": user_message})
    chat_history.append({"role": "assistant", "text": bot_response})

    # Ограничиваем историю сообщений (чтобы не была слишком длинной)
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]

    # Сохраняем историю сообщений
    user_messages[user_id] = chat_history

    await update.message.reply_text(bot_response)


def main():
    """Запуск бота."""
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Получаем ID облака и каталога
    # CLOUD_ID = get_cloud_id() # Эти функции больше не нужны
    # if CLOUD_ID is None:
    #     print("Не удалось получить ID облака. Бот остановлен.")
    #     return

    # FOLDER_ID = get_folder_id(CLOUD_ID) # Эти функции больше не нужны
    # if FOLDER_ID is None:
    #     print("Не удалось получить ID каталога. Бот остановлен.")
    #     return
    FOLDER_ID = "b1grlj23er77g2vtnr32" # Задаем FOLDER_ID напрямую

    print(f"FOLDER_ID: {FOLDER_ID}")  # Добавлено для отладки
    # Сохраняем FOLDER_ID в context.bot_data
    application.bot_data['folder_id'] = FOLDER_ID

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()


if __name__ == "__main__":
    main()