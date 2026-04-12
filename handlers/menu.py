from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

def menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="🎒 Инвентарь", callback_data="inv")],
        [InlineKeyboardButton(text="💰 Бонус", callback_data="daily")],
        [InlineKeyboardButton(text="🏆 Топ", callback_data="top")]
    ])

@router.message(commands=["menu", "start"])
async def menu(message: types.Message):
    await message.answer("📋 Главное меню:", reply_markup=menu_kb())
