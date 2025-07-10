from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command

import additional_features.db_working as db
import app.keyboards as kb

router = Router()


class Create(StatesGroup):
    notion_token = State()
    page_id = State()


@router.message(Command("create"))
async def cmd_create(message: Message, state: FSMContext):
    await state.set_state(Create.notion_token)
    await message.answer("Введите токен из 1-ой инструкции:")


@router.message(Create.notion_token)
async def get_token(message: Message, state: FSMContext):
    await state.update_data(notion_token=message.text)
    await state.set_state(Create.page_id)
    await message.answer("Введите ссылку на страницу из 2-ой инструкции:")


@router.message(Create.page_id)
async def get_page(message: Message, state: FSMContext):
    await state.update_data(page_id=message.text)
    data = await state.get_data()
    notion_token, page_id = data["notion_token"], data["page_id"]
    await state.clear()
    db_connection = db.DBConnection()
    if db_connection.check_user(message.from_user.id):
        await message.answer("Ваши данные были в базе данных до этого!!\nВыберите дальнейшее действие:",
                             reply_markup=kb.bot_actions)
    else:
        db_connection.create_user(message.from_user.id, notion_token, page_id)
        await message.answer("Ваши данные успешно загружены. Выберите дальнейшее действие:",
                             reply_markup=kb.bot_actions)
