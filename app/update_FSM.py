from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command

import additional_features.db_working as db
import app.keyboards as kb

router = Router()


class Update(StatesGroup):
    new_notion_token = State()
    new_page_id = State()


@router.message(Command("update"))
async def cmd_update(message: Message, state: FSMContext):
    await state.set_state(Update.new_notion_token)
    await message.answer("Введите новый Notion токен(интеграция). Если он остался таким же, введите его еще раз!",
                         reply_markup=kb.cancel)


@router.message(Update.new_notion_token)
async def update_token(message: Message, state: FSMContext):
    await state.update_data(new_notion_token=message.text)
    await state.set_state(Update.new_page_id)
    await message.answer("Введите новую ссылку на страницу шаблона", reply_markup=kb.cancel)


@router.message(Update.new_page_id)
async def update_page(message: Message, state: FSMContext):
    await state.update_data(new_page_token=message.text)
    data = await state.get_data()
    db_connection = db.DBConnection()
    if db_connection.update_user(message.from_user.id, *[i for i in data.values()]):
        await message.answer("Данные успешно обновлены!", reply_markup=kb.bot_actions)
    else:
        await message.answer(
            "Пользователь с таким id не найден в базе данных!\nВведите команду /create, чтобы внести ваши данные в нашу базу")
