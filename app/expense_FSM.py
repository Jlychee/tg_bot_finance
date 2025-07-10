from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import app.keyboards as kb

from additional_features import notion_integration as ni
import additional_features.db_working as db

router = Router()


class Expense(StatesGroup):
    account_name = State()
    categories_name = State()
    amount = State()
    expense_name = State()


@router.callback_query(F.data == 'expense_call')
async def expense_call(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Expense.account_name)
    db_connection = db.DBConnection()
    notion_token, page_id = db_connection.check_user(callback.from_user.id)
    try:
        notion_connection = ni.NotionConnection(notion_token, page_id)
        await callback.message.edit_text("Выберите кошелек, с которого необходимо произвести списание:",
                                         reply_markup=await kb.expense_wallet_list(notion_connection.get_accounts()))
    except Exception:
        await callback.message.edit_text("Невозможно подключиться к Notion, обновите данные, введя команду /update!")


@router.callback_query(F.data.startswith("expense_remember_acc"))
async def expense_remember_acc(callback: CallbackQuery, state: FSMContext):
    db_connection = db.DBConnection()
    notion_token, page_id = db_connection.check_user(callback.from_user.id)
    try:
        notion_connection = ni.NotionConnection(notion_token, page_id)
        accounts = notion_connection.get_accounts()
        await state.update_data(account_name=accounts[callback.data.split("_")[-1]][0])
        await state.set_state(Expense.categories_name)
        await callback.message.edit_text("Выберите категорию:",
                                         reply_markup=await kb.categories_list(notion_connection.get_categories()))
    except Exception:
        await callback.message.edit_text("Невозможно подключиться к Notion, обновите данные, введя команду /update!")


@router.callback_query(F.data.startswith("remember_cat"))
async def remember_cat(callback: CallbackQuery, state: FSMContext):
    db_connection = db.DBConnection()
    notion_token, page_id = db_connection.check_user(callback.from_user.id)
    try:
        notion_connection = ni.NotionConnection(notion_token, page_id)
        categories = notion_connection.get_categories()
        await state.update_data(categories_name=categories[callback.data.split("_")[-1]])
        await state.set_state(Expense.amount)
        await callback.message.edit_text("Введите сумму списания:", reply_markup=kb.cancel)
    except Exception:
        await callback.message.edit_text("Невозможно подключиться к Notion, обновите данные, введя команду /update!")


@router.message(Expense.amount)
async def remember_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await state.set_state(Expense.expense_name)
    await message.answer("Введите название 'товара':", reply_markup=kb.cancel)


@router.message(Expense.expense_name)
async def remember_expense_name(message: Message, state: FSMContext):
    await state.update_data(expense_name=message.text)
    data = await state.get_data()
    db_connection = db.DBConnection()
    notion_token, page_id = db_connection.check_user(message.from_user.id)
    try:
        notion_connection = ni.NotionConnection(notion_token, page_id)
        notion_connection.new_expense_record(*[i for i in data.values()])
        await state.clear()
        await message.answer("Запись успешно внесена!", reply_markup=kb.bot_actions)
    except Exception:
        await message.edit_text("Невозможно подключиться к Notion, обновите данные, введя команду /update!")
