import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from db.sqlite import init_db

from handlers import start, profile, menu, dig, daily, tree, inventory, top, chat

async def main():
    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(profile.router)
    dp.include_router(dig.router)
    dp.include_router(daily.router)
    dp.include_router(tree.router)
    dp.include_router(inventory.router)
    dp.include_router(top.router)
    dp.include_router(chat.router)

    print("BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
