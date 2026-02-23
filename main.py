import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from deep_translator import GoogleTranslator

# 1. KALITLAR
API_TOKEN = '8176485041:AAHqdq2QtQbJnh_oJSGas5zqBIvZYU1bxS1s'
NEWS_API_KEY = '632332ae0c46482b96f51b05a1609773'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
translator = GoogleTranslator(source='en', target='uz')

# 2. MENU TUGMALARI
def get_menu():
    kb = [
        [types.KeyboardButton(text="📊 Bozor Tahlili")],
        [types.KeyboardButton(text="🎯 Signal")],
        [types.KeyboardButton(text="🌍 Dunyo Yangiliklari")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# 3. START BUYRUG'I
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🚀 Bot ishga tushdi! Bo'limni tanlang:", reply_markup=get_menu())

# 4. DUNYO YANGILIKLARI
@dp.message(lambda m: m.text == "🌍 Dunyo Yangiliklari")
async def handle_news(message: types.Message):
    await message.answer("⌛️ Yangiliklar olinmoqda...")
    url = f'https://newsapi.org/v2/everything?q=crypto&language=en&apiKey={NEWS_API_KEY}'
    res = requests.get(url).json()
    articles = res.get('articles', [])[:3]
    for art in articles:
        title_uz = translator.translate(art['title'])
        await message.answer(f"🔹 {title_uz}\n🔗 [O'qish]({art['url']})", parse_mode="Markdown")

# 5. BOZOR TAHLILI (Tuzatilgan qismi)
@dp.message(lambda m: m.text == "📊 Bozor Tahlili")
async def handle_analysis(message: types.Message):
    await message.answer("📈 **Bozor Tahlili (BTC/USDT)**\n\nNarx barqaror darajada. Qarshilik: $52,500. Qo'llab-quvvatlash: $51,000.")

# 6. SIGNAL (Tuzatilgan qismi)
@dp.message(lambda m: m.text == "🎯 Signal")
async def handle_signal(message: types.Message):
    await message.answer("🎯 **Yangi Signal**\n\n💰 Juftlik: BTC/USDT\n🟢 Tur: LONG\n🎯 Maqsad: $54,000\n🛑 Stop: $50,200")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
