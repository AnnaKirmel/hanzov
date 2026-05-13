import os
import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web

# Бот берет настройки из переменных окружения сервера
BOT_TOKEN = "8775863717:AAFEA4T1bca5mYvLDs283PpWOn2bJTSKxcY"
# Превращаем ID группы в число. Если переменной нет, ставим 0
GROUP_ID = -1003786096127

if not BOT_TOKEN or GROUP_ID == 0:
    raise ValueError("Ошибки в настройках! Проверьте переменные BOT_TOKEN и GROUP_ID в панели Render.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


# Страница для проверки активности бота со стороны Render и пинговщика
async def handle(request):
    return web.Response(text="Бот активен и работает круглосуточно!")


async def send_reminder(text: str):
    try:
        await bot.send_message(chat_id=GROUP_ID, text=text)
        print(f"Отправлено уведомление: {text}")
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")


def setup_schedule():
    scheduler.add_job(send_reminder, "cron", hour=12, minute=0, args=["🏹 Время: 12:00 — Охота!"])
    scheduler.add_job(send_reminder, "cron", hour=19, minute=0, args=["🐍 Время: 19:00 — Питон!"])
    scheduler.add_job(send_reminder, "cron", hour=20, minute=0, args=["👑 Время: 20:00 — Царь!"])
    scheduler.add_job(send_reminder, "cron", hour=20, minute=0, args=["🐍 Время: 20:00 — Питон!"])
    scheduler.add_job(send_reminder, "cron", hour=22, minute=0, args=["🛒 Время: 22:00 — Повозки!"])


async def main():
    setup_schedule()
    scheduler.start()

    # Запуск веб-сервера на порту, который требует Render
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Служебный веб-сервер запущен на порту {port}")

    print("Бот успешно запущен на сервере. Ожидание расписания...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен.")
