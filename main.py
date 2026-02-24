import asyncio
import logging
import requests
import random
import pytz
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- SOZLAMALAR ---
API_TOKEN = '8176485041:AAHOcooQBvWgC0sxdbebJpOKnY8ab1zsHy4'
NEWS_API_KEY = '5a70717208154109867011d871788220'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- YORDAMCHI FUNKSIYALAR (REAL-TIME) ---

def get_uzb_rates():
    try:
        res = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()
        usd = next(i for i in res if i["Code"] == "USD")
        eur = next(i for i in res if i["Code"] == "EUR")
        rub = next(i for i in res if i["Code"] == "RUB")
        return f"🇺🇿 **MB Kurslari:**\n💵 1 USD = {usd['Rate']} so'm\n💶 1 EUR = {eur['Rate']} so'm\n🇷🇺 1 RUB = {rub['Rate']} so'm"
    except Exception: return "⚠️ Kurslarni olishda xatolik."

def get_top_5():
    try:
        symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT']
        text = "📈 **Top 5 Kripto:**\n\n"
        for s in symbols:
            p = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={s}").json()
            text += f"• {s.replace('USDT','')}: {float(p['price']):,.2f} USD\n"
        return text
    except Exception: return "⚠️ Kripto ma'lumotlarida xatolik."

def get_market_status():
    tashkent_tz = pytz.timezone('Asia/Tashkent')
    now = datetime.now(tashkent_tz)
    h = now.hour
    if now.weekday() >= 5: return "🛑 Bozor yopiq (Dam olish kuni)"
    tokyo = "🟢 Ochiq" if 5 <= h <= 14 else "🔴 Yopiq"
    london = "🟢 Ochiq" if 13 <= h <= 21 else "🔴 Yopiq"
    ny = "🟢 Ochiq" if 18 <= h or h <= 1 else "🔴 Yopiq"
    return f"🕒 **Birja holati (UZ):**\n🇯🇵 Tokio: {tokyo}\n🇬🇧 London: {london}\n🇺🇸 Nyu-York: {ny}"

# --- MENYULAR ---

def main_menu():
    return types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="💰 Narxlar"), types.KeyboardButton(text="🚨 Signallar")],
        [types.KeyboardButton(text="🌍 Yangiliklar"), types.KeyboardButton(text="📈 Bozor Tahlili")],
        [types.KeyboardButton(text="🇺🇿 Valyuta Kursi"), types.KeyboardButton(text="🔝 Top 5 Kripto")],
        [types.KeyboardButton(text="🕒 Birja Vaqti")]
    ], resize_keyboard=True)

def signal_menu():
    return types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="🪙 Kripto Signallar"), types.KeyboardButton(text="💱 Forex Signallar")],
        [types.KeyboardButton(text="⬅️ Orqaga")]
    ], resize_keyboard=True)

def news_menu():
    return types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="🪙 Kripto Yangiliklar"), types.KeyboardButton(text="💱 Forex Yangiliklar")],
        [types.KeyboardButton(text="⬅️ Orqaga")]
    ], resize_keyboard=True)

# --- HANDLERS ---

@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer("🚀 **WinnerMaster Terminaliga xush kelibsiz!**\nBarcha ma'lumotlar real vaqt rejimida yangilanadi.", reply_markup=main_menu())

@dp.message(F.text == "🚨 Signallar")
async def sig_main(m: types.Message):
    await m.answer("Qaysi bozor signali kerak?", reply_markup=signal_menu())

@dp.message(F.text == "🌍 Yangiliklar")
async def news_main(m: types.Message):
    await m.answer("Yangilik turini tanlang:", reply_markup=news_menu())

@dp.message(F.text == "🇺🇿 Valyuta Kursi")
async def show_rates(m: types.Message):
    await m.answer(get_uzb_rates(), parse_mode="Markdown")

@dp.message(F.text == "🔝 Top 5 Kripto")
async def show_top(m: types.Message):
    await m.answer(get_top_5(), parse_mode="Markdown")

@dp.message(F.text == "🕒 Birja Vaqti")
async def show_time(m: types.Message):
    await m.answer(get_market_status(), parse_mode="Markdown")

@dp.message(F.text == "⬅️ Orqaga")
async def back_main(m: types.Message):
    await m.answer("Asosiy menyu:", reply_markup=main_menu())

# --- RUN BOT ---
async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
