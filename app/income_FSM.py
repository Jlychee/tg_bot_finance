from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import app.keyboards as kb

from additional_features import notion_integration as ni
import additional_features.db_working as db

router = Router()


class Income(StatesGroup):
    account_name = State()
    amount = State()
    income_name = State()


@router.callback_query(F.data == 'income_call')
async def income_call(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Income.account_name)
    db_connection = db.DBConnection()
    notion_token, page_id = db_connection.check_user(callback.from_user.id)
    try:
        notion_connection = ni.NotionConnection(notion_token, page_id)
        await callback.message.edit_text("Выберите кошелек, который необходимо пополнить:",
                                         reply_markup=await kb.income_wallet_list(notion_connection.get_accounts()))
    except Exception:
        await callback.message.edit_text("Невозможно подключиться к Notion, обновите данные, введя команду /update!")


@router.callback_query(F.data.startswith("income_remember_acc"))
async def remember_acc(callback: CallbackQuery, state: FSMContext):
    db_connection = db.DBConnection()
    notion_token, page_id = db_connection.check_user(callback.from_user.id)
    try:
        notion_connection = ni.NotionConnection(notion_token, page_id)
        accounts = notion_connection.get_accounts()
        await state.update_data(account_name=accounts[callback.data.split("_")[-1]][0])
        await state.set_state(Income.amount)
        await callback.message.edit_text("Введите сумму пополнения:", reply_markup=kb.cancel)
    except Exception:
        await callback.message.edit_text("Невозможно подключиться к Notion, обновите данные, введя команду /update!")


@router.message(Income.amount)
async def remember_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await state.set_state(Income.income_name)
    await message.answer("Введите название пополнения:", reply_markup=kb.cancel)


@router.message(Income.income_name)
async def remember_income_name(message: Message, state: FSMContext):
    await state.update_data(Income_name=message.text)
    data = await state.get_data()
    db_connection = db.DBConnection()
    notion_token, page_id = db_connection.check_user(message.from_user.id)
    try:
        notion_connection = ni.NotionConnection(notion_token, page_id)
        notion_connection.new_income_record(*[i for i in data.values()])
        await state.clear()
        await message.answer("Запись успешно внесена!", reply_markup=kb.bot_actions)
    except Exception:
        await message.edit_text("Невозможно подключиться к Notion, обновите данные, введя команду /update!")
