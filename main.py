# Импорт сторонних библиотек
import asyncio
import os

from dotenv import load_dotenv
# Импорты aiogram
from aiogram import Bot, Dispatcher
# Импорты из файлов
from app.user_handlers import user_router


async def main():
    # Загрузка переменных среды
    load_dotenv()

    # Получение токена и инициализация Bot и Dispatcher
    token = os.getenv('BOT_TOKEN')
    bot = Bot(token=token)
    dp = Dispatcher()

    # Подключение роутера
    dp.include_router(user_router)
    await dp.start_polling(bot, skip_updates=True)


# Запуск бота
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
