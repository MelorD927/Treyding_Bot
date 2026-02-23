import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# --- SOZLAMALAR ---
API_TOKEN = '8176485041:AAHqdq2QtQbJnh_oJSGas5zqBIvZYU1bxS1s'
NEWS_API_KEY = '632332ae0c46482b96f51b05a1609773'

# Loggingni to'g'ri sozlash
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- MENU TUGMALARI ---
def get_menu():
    buttons = [
        [types.KeyboardButton(text="Bozor Tahlili")],
        [types.KeyboardButton(text="Signal")],
        [types.KeyboardButton(text="Yangiliklar")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# --- BUYRUQLAR ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🚀 Bot ishga tushdi! Bo'limni tanlang:", reply_markup=get_menu())

@dp.message(lambda m: m.text == "Bozor Tahlili")
async def handle_analysis(message: types.Message):
    await message.answer("📈 BTC/USDT Tahlili:\n\nNarx hozirda barqaror darajada. Qarshilik: $52,500.")

@dp.message(lambda m: m.text == "Signal")
async def handle_signal(message: types.Message):
    await message.answer("🎯 Yangi Signal:\n\nJuftlik: BTC/USDT\nYo'nalish: LONG\nMaqsad: $54,000")

@dp.message(lambda m: m.text == "Yangiliklar")
async def handle_news(message: types.Message):
    await message.answer("🌍 Kripto yangiliklari o'qilmoqda...")
    url = f'https://newsapi.org/v2/everything?q=crypto&language=en&apiKey={NEWS_API_KEY}'
    try:
        res = requests.get(url).json()
        articles = res.get('articles', [])[:3]
        for art in articles:
            await message.answer(f"🔹 {art['title']}\n🔗 [Batafsil]({art['url']})", parse_mode="Markdown")
    except:
        await message.answer("Xatolik: Yangiliklarni olib bo'lmadi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
