import asyncio

from misc.config import TOKEN
from aiogram import Bot, Dispatcher

from app.handlers import router as handler_router
from app.expense_FSM import router as expense_router
from app.income_FSM import router as income_router
from app.transfer_FSM import router as transfer_router
from app.create_FSM import router as create_router
from app.update_FSM import router as update_router

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(
        handler_router,
        expense_router,
        income_router,
        transfer_router,
        create_router,
        update_router
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit!")
