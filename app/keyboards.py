from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

template_availability_answer = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да, у меня уже загружен шаблон", callback_data="db_check")],
    [InlineKeyboardButton(text="Нет, у меня еще нет шаблона", callback_data="template_instruction")]
])

end_of_instruction = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Шаблон успешно скопирован!", callback_data="create_db_record")]
])

bot_actions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Узнать мой баланс", callback_data="check_balance"),
     InlineKeyboardButton(text="Добавить запись расходов", callback_data="expense_call")],
    [InlineKeyboardButton(text="Добавить запись доходов", callback_data="income_call"),
     InlineKeyboardButton(text="Добавить запись переводов", callback_data="transfer_call")]
])

wallet_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад к выбору кошелька", callback_data="check_balance")]
])

cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отменить и вернуться к выбору действия", callback_data="cancel")]
])


async def wallet_list_balance(wallet_data):
    keyboard = InlineKeyboardBuilder()
    size = [2 for i in range(len(wallet_data) // 2)] + [1, 1]
    for ind, wallet in enumerate(wallet_data):
        keyboard.add(InlineKeyboardButton(text=wallet, callback_data=f"get_balance_{wallet}"))
    keyboard.add(InlineKeyboardButton(text="All accounts", callback_data="get_balance_All accounts"))
    keyboard.add(InlineKeyboardButton(text="Назад к выбору действия", callback_data="actions"))
    return keyboard.adjust(*size).as_markup()


async def expense_wallet_list(wallet_data):
    keyboard = InlineKeyboardBuilder()
    size = [2 for i in range(len(wallet_data) // 2)] + [1, 1]
    for ind, wallet in enumerate(wallet_data):
        keyboard.add(InlineKeyboardButton(text=wallet, callback_data=f"expense_remember_acc_{wallet}"))
    keyboard.add(InlineKeyboardButton(text="Отменить и вернуться к выбору действия", callback_data="cancel"))
    return keyboard.adjust(*size).as_markup()


async def income_wallet_list(wallet_data):
    keyboard = InlineKeyboardBuilder()
    size = [2 for i in range(len(wallet_data) // 2)] + [1, 1]
    for ind, wallet in enumerate(wallet_data):
        keyboard.add(InlineKeyboardButton(text=wallet, callback_data=f"income_remember_acc_{wallet}"))
    keyboard.add(InlineKeyboardButton(text="Отменить и вернуться к выбору действия", callback_data="cancel"))
    return keyboard.adjust(*size).as_markup()


async def transfer_from_wallet_list(wallet_data):
    keyboard = InlineKeyboardBuilder()
    size = [2 for i in range(len(wallet_data) // 2)] + [1, 1]
    for ind, wallet in enumerate(wallet_data):
        keyboard.add(InlineKeyboardButton(text=wallet, callback_data=f"transfer_from_remember_acc_{wallet}"))
    keyboard.add(InlineKeyboardButton(text="Отменить и вернуться к выбору действия", callback_data="cancel"))
    return keyboard.adjust(*size).as_markup()


async def transfer_to_wallet_list(wallet_data):
    keyboard = InlineKeyboardBuilder()
    size = [2 for i in range(len(wallet_data) // 2)] + [1, 1]
    for ind, wallet in enumerate(wallet_data):
        keyboard.add(InlineKeyboardButton(text=wallet, callback_data=f"transfer_to_remember_acc_{wallet}"))
    keyboard.add(InlineKeyboardButton(text="Отменить и вернуться к выбору действия", callback_data="cancel"))
    return keyboard.adjust(*size).as_markup()


async def categories_list(categories_data):
    keyboard = InlineKeyboardBuilder()
    size = [2 for i in range(len(categories_data) // 2)] + [1, 1]
    for ind, categories in enumerate(categories_data):
        keyboard.add(InlineKeyboardButton(text=categories, callback_data=f"remember_cat_{categories}"))
    keyboard.add(InlineKeyboardButton(text="Отменить и вернуться к выбору действия", callback_data="cancel"))
    return keyboard.adjust(*size).as_markup()
