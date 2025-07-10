from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

from additional_features import notion_integration as ni
import additional_features.db_working as db
import additional_features.get_img_1 as instr_1
import additional_features.get_img_2 as instr_2

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.username}! У тебя уже есть скопированный шаблон 'Finance Tracker by Rosidssoy' в Notion?",
        reply_markup=kb.template_availability_answer)


@router.callback_query(F.data == "template_instruction")
async def template_instruction(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        '''<a href='https://www.notion.so/templates/finance-tracker-by-rosidssoy'>
        Это ссылка на шаблон, необходимый для работы с ботом.</a>
<b>Иснтрукция по добавлению шаблона в Notion:</b>
        1) Нажмите кнопку Get template
        2) Выберите аккаунт, в который вы хотите скопировать шаблон
        3) Подождите, пока шаблон скопируется и все будет готово!\n
        Если шаблон появился у вас в Notion, то можно продолжить работу с ботом, выбрав пункт "Шаблон успешно скопирован!"
        Если у вас что-то не получилось, проверьте делаете ли вы все в соответствии с инструкцией выше.
        ''', reply_markup=kb.end_of_instruction, disable_web_page_preview=True,
        parse_mode="HTML")


@router.callback_query(F.data == "create_db_record")
async def create_db_record(callback: CallbackQuery):
    await callback.answer()
    media_1 = [
        InputMediaPhoto(media=FSInputFile(r".\img\instruction_1\\" + i)) for i in instr_1.get_img()
    ]
    media_2 = [
        InputMediaPhoto(media=FSInputFile(r".\img\instruction_2\\" + i)) for i in instr_2.get_img()
    ]
    await callback.message.answer(
        '''Чтобы пользоваться ботом необходимо обеспечить его некоторыми данными.
        <b>Инструкция 1:</b>
        1) <a href='https://www.notion.so/profile/integrations'>Перейдите по ссылке:</a>
        2) Делайте все так, как показано на скриншотах ниже
        3) Перейти ко 2-ой инструкции''', disable_web_page_preview=True, parse_mode="HTML")
    await callback.message.answer_media_group(media_1)
    await callback.message.answer_media_group(media_2)
    await callback.message.answer("Далее пропишите команду /create, чтобы добавить свои данные в нашу базу")


@router.callback_query(F.data == "db_check")
async def db_check(callback: CallbackQuery):
    await callback.answer()
    db_connection = db.DBConnection()
    try:
        notion_token, page_id = db_connection.check_user(callback.from_user.id)
        await callback.message.answer("Ваши данные успешно найдены, выберите дальнейшее действие:",
                                      reply_markup=kb.bot_actions)
    except Exception as ex:
        await callback.message.edit_text("""
                    Ваши данные не были найдены в базе данных. Введите команду /create для добавления своих данных в нашу базу
                    """)


@router.message(Command('actions'))
async def cmd_actions(message: Message):
    await message.answer("Вот список того, что может сделать бот:", reply_markup=kb.bot_actions)


@router.callback_query(F.data == "actions")
async def actions(callback: CallbackQuery):
    await callback.message.edit_text("Вот список того, что может сделать бот:", reply_markup=kb.bot_actions)


@router.callback_query(F.data == "check_balance")
async def check_balance(callback: CallbackQuery):
    db_connection = db.DBConnection()
    notion_token, page_id = db_connection.check_user(callback.from_user.id)
    try:
        notion_connection = ni.NotionConnection(notion_token, page_id)
        await callback.message.edit_text("Выберите кошелек, для которого хотите узнать баланс:",
                                         reply_markup=await kb.wallet_list_balance(notion_connection.get_accounts()))
    except Exception:
        await callback.message.edit_text("Невозможно подключиться к Notion, обновите данные, введя команду /update!")


@router.callback_query(F.data.startswith("get_balance"))
async def get_balance(callback: CallbackQuery):
    db_connection = db.DBConnection()
    notion_token, page_id = db_connection.check_user(callback.from_user.id)
    try:
        notion_connection = ni.NotionConnection(notion_token, page_id)
        account = callback.data.split("_")[-1]
        accounts = notion_connection.get_accounts()

        if account == "All accounts":
            sm = notion_connection.get_full_balance(accounts)
            await callback.message.edit_text(f"Общий баланс ваших кошельков составляет: {sm} рублей",
                                             reply_markup=kb.wallet_back)
        else:
            sm = notion_connection.get_balance(account, accounts)
            await callback.message.edit_text(f"Баланс '{account}' составляет: {sm} рублей",
                                             reply_markup=kb.wallet_back)
    except Exception:
        await callback.message.edit_text("Невозможно подключиться к Notion, обновите данные, введя команду /update!")


@router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Вот список того, что может сделать бот:", reply_markup=kb.bot_actions)
