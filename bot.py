import os
import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Бот берет настройки из переменных окружения сервера
BOT_TOKEN = "8775863717:AAFEA4T1bca5mYvLDs283PpWOn2bJTSKxcY"
# Превращаем ID группы в число. Если переменной нет, ставим 0
GROUP_ID = -1003786096127

# Проверка, что настройки заданы
if not BOT_TOKEN or not GROUP_ID:
    raise ValueError("Ошибки в настройках! Проверьте переменные BOT_TOKEN и GROUP_ID.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

async def send_reminder(text: str):
    try:
        await bot.send_message(chat_id=GROUP_ID, text=text)
        print(f"Отправлено: {text}")
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def setup_schedule():
    scheduler.add_job(send_reminder, "cron", hour=12, minute=0, args=["🏹 Время: 12:00 — Охота!"])
    scheduler.add_job(send_reminder, "cron", hour=19, minute=0, args=["🐍 Время: 19:00 — Питон!"])
    scheduler.add_job(send_reminder, "cron", hour=20, minute=0, args=["👑 Время: 20:00 — Царь!"])
    scheduler.add_job(send_reminder, "cron", hour=20, minute=0, args=["🐍 Время: 20:00 — Питон!"])
    scheduler.add_job(send_reminder, "cron", hour=22, minute=0, args=["🛒 Время: 22:00 — Повозки!"])

async def main():
    setup_schedule()
    scheduler.start()
    print("Бот успешно запущен на сервере...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен.")
