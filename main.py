import asyncio
import logging
import requests
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- TO'G'RI TOKEN ---
API_TOKEN = '8176485041:AAHOcooQBvWgC0sxdbebJpOKnY8ab1zsHy4'
NEWS_API_KEY = '632332ae0c46482b96f51b05a1609773'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def get_main_menu():
    kb = [
        [types.KeyboardButton(text="💰 Real Narxlar"), types.KeyboardButton(text="🎯 Signallar")],
        [types.KeyboardButton(text="🌍 Dunyo Yangiliklari"), types.KeyboardButton(text="📊 Bozor Tahlili")],
        [types.KeyboardButton(text="🧮 Risk Kalkulyatori"), types.KeyboardButton(text="📈 Grafika (TradingView)")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    name = message.from_user.first_name
    kb = [[types.KeyboardButton(text="🇺🇿 O'zbek tili")], [types.KeyboardButton(text="🇷🇺 Русский язык")]]
    await message.answer(f"Assalomu alaykum, {name}! Tilni tanlang:", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

@dp.message(F.text.in_(["🇺🇿 O'zbek tili", "🇷🇺 Русский язык"]))
async def set_lang(message: types.Message):
    await message.answer("Asosiy menyu:", reply_markup=get_main_menu())

@dp.message(F.text == "💰 Real Narxlar")
async def handle_prices(message: types.Message):
    try:
        btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        await message.answer(f"📊 BTC/USDT: `${float(btc['price']):,.2f}`", parse_mode="Markdown")
    except:
        await message.answer("❌ Xatolik yuz berdi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
