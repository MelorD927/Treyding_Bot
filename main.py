import logging
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# --- SOZLAMALAR ---
API_TOKEN = '8176485041:AAHqdq2QtQbJnh_oJSGas5zqBIvZYU1bxS1s' 
NEWS_API_KEY = '632332ae0c46482b96f51b05a1609773' 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def get_menu():
    kb = [
        [types.KeyboardButton(text="Bozor Tahlili")],
        [types.KeyboardButton(text="Signal")],
        [types.KeyboardButton(text="Yangiliklar")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Bot ishga tushdi! Tugmalardan birini tanlang:", reply_markup=get_menu())

@dp.message(lambda m: m.text == "Bozor Tahlili")
async def handle_analysis(message: types.Message):
    await message.answer("📈 BTC/USDT Tahlili:\nNarx: $52,100\nHolat: Barqaror o'sish kutilmoqda.")

@dp.message(lambda m: m.text == "Signal")
async def handle_signal(message: types.Message):
    await message.answer("🎯 Yangi Signal:\nJuftlik: BTC/USDT\nYo'nalish: LONG\nMaqsad: $54,000")

@dp.message(lambda m: m.text == "Yangiliklar")
async def handle_news(message: types.Message):
    await message.answer("🌍 Yangiliklar: Kripto bozori ijobiy tomonga o'zgarmoqda.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
