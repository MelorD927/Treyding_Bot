import asyncio
import logging
import requests
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- SOZLAMALAR ---
API_TOKEN = '8176485041:AAHqdq2QtQbJnh_oJSGas5zqBIvZYU1bxS1s'
NEWS_API_KEY = '632332ae0c46482b96f51b05a1609773'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- ASOSIY MENYU ---
def get_main_menu():
    kb = [
        [types.KeyboardButton(text="💰 Real Narxlar"), types.KeyboardButton(text="🎯 Signallar")],
        [types.KeyboardButton(text="🌍 Dunyo Yangiliklari"), types.KeyboardButton(text="📊 Bozor Tahlili")],
        [types.KeyboardButton(text="🧮 Risk Kalkulyatori"), types.KeyboardButton(text="📈 Grafika (TradingView)")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# --- START: ISM BILAN MUROJAAT ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    name = message.from_user.first_name
    kb = [
        [types.KeyboardButton(text="🇺🇿 O'zbek tili")],
        [types.KeyboardButton(text="🇷🇺 Русский язык"), types.KeyboardButton(text="🇺🇸 English")]
    ]
    await message.answer(f"Assalomu alaykum, {name}! Botga xush kelibsiz. Iltimos, tilni tanlang:", 
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

@dp.message(F.text.in_(["🇺🇿 O'zbek tili", "🇷🇺 Русский язык", "🇺🇸 English"]))
async def set_language(message: types.Message):
    await message.answer("Asosiy menyuga xush kelibsiz! Kerakli bo'limni tanlang:", reply_markup=get_main_menu())

# --- 1. REAL NARXLAR (BINANCE API) ---
@dp.message(F.text == "💰 Real Narxlar")
async def handle_prices(message: types.Message):
    now = datetime.now().strftime("%H:%M:%S")
    try:
        btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        eth = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT").json()
        text = (f"🕒 **Vaqt:** {now}\n\n"
                f"₿ BTC/USDT: `${float(btc['price']):,.2f}`\n"
                f"Ξ ETH/USDT: `${float(eth['price']):,.2f}`\n\n"
                f"ℹ️ Narxlar har soniyada yangilanadi.")
        await message.answer(text, parse_mode="Markdown")
    except:
        await message.answer("❌ Narxlarni olishda xatolik yuz berdi.")

# --- 2. SIGNALLAR (CRYPTO 8 TA, FOREX 4 TA) ---
@dp.message(F.text == "🎯 Signallar")
async def signal_menu(message: types.Message):
    kb = [
        [types.KeyboardButton(text="💎 Crypto (Top 8)"), types.KeyboardButton(text="💵 Forex (Top 4)")],
        [types.KeyboardButton(text="⬅️ Orqaga")]
    ]
    await message.answer("⚠️ **Ogohlantirish:** Signallarni tanlang:", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

@dp.message(F.text == "💎 Crypto (Top 8)")
async def crypto_signals(message: types.Message):
    text = "🚀 **TOP-8 Crypto Signals:**\n\n"
    coins = ["BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "DOGE", "DOT"]
    for c in coins:
        text += f"✅ {c}/USDT: Buy Zone - Tahlil qilinmoqda...\n"
    await message.answer(text)

@dp.message(F.text == "💵 Forex (Top 4)")
async def forex_signals(message: types.Message):
    text = "📉 **TOP-4 Forex & Gold:**\n\n"
    pairs = ["🥇 GOLD (XAUUSD)", "🇪🇺 EURUSD", "🇬🇧 GBPUSD", "🇯🇵 USDJPY"]
    for p in pairs:
        text += f"🔹 {p}: Signal kutilmoqda...\n"
    await message.answer(text)

# --- 3. YANGILIKLAR ---
@dp.message(F.text == "🌍 Dunyo Yangiliklari")
async def news_choice(message: types.Message):
    kb = [[types.KeyboardButton(text="📰 Crypto News"), types.KeyboardButton(text="📰 Forex News")], [types.KeyboardButton(text="⬅️ Orqaga")]]
    await message.answer("Yangiliklar turini tanlang:", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

@dp.message(F.text.in_(["📰 Crypto News", "📰 Forex News"]))
async def fetch_news(message: types.Message):
    q = "crypto" if "Crypto" in message.text else "forex"
    url = f"https://newsapi.org/v2/everything?q={q}&apiKey={NEWS_API_KEY}&pageSize=1"
    try:
        res = requests.get(url).json()
        art = res['articles'][0]
        await message.answer(f"📌 **{message.text}:**\n\n{art['title']}\n\n🔗 [Maqolani o'qish]({art['url']})", parse_mode="Markdown")
    except:
        await message.answer("❌ Yangiliklarni yuklab bo'lmadi.")

# --- 4. TRADINGVIEW VA TAHLIL ---
@dp.message(F.text == "📈 Grafika (TradingView)")
async def tv_charts(message: types.Message):
    await message.answer("📊 **Jonli grafiklar:**\n\n[Bitcoin](https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT)\n[Gold/Oltin](https://www.tradingview.com/chart/?symbol=OANDA:XAUUSD)", parse_mode="Markdown")

@dp.message(F.text == "📊 Bozor Tahlili")
async def market_analysis(message: types.Message):
    await message.answer_photo(
        photo="https://s3.tradingview.com/i/iS7S0K0k_mid.png",
        caption="📈 **Texnik tahlil:**\nBozor hozirda kutilayotgan korreksiya zonasida. Ehtiyotkor bo'ling!"
    )

@dp.message(F.text == "🧮 Risk Kalkulyatori")
async def risk_calculator(message: types.Message):
    await message.answer("🧮 **Riskni boshqarish:**\n\nLot = (Depozit * Risk%) / StopLoss\n\nDoimo kapitalingizning 1-3% qismidan ortiq tavakkal qilmang!")

@dp.message(F.text == "⬅️ Orqaga")
async def back_home(message: types.Message):
    await message.answer("Asosiy menyu:", reply_markup=get_main_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
