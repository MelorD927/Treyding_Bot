import asyncio
import requests
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- SOZLAMALAR ---
API_TOKEN = '8176485041:AAHOcooQBvWgC0sxdbebJpOKnY8ab1zsHy4'
NEWS_API_KEY = '5a70717208154109867011d871788220'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- TAHLIL FUNKSIYASI ---
def get_signal_data(symbol, is_forex=False):
    try:
        # Tilla uchun PAXG, boshqalar uchun o'zi
        api_sym = "PAXGUSDT" if "XAU" in symbol else symbol
        url = f"https://api.binance.com/api/v3/klines?symbol={api_sym}&interval=1h&limit=20"
        res = requests.get(url, timeout=10).json()
        
        # Narxlarni olish va tahlil qilish
        closes = [float(c[4]) for c in res]
        current = closes[-1]
        ma = sum(closes) / len(closes)

        # Signal mantiqi (MA asosida)
        status = "🟢 BUY" if current < ma else "🔴 SELL"
        tp_coeff = 1.005 if is_forex else 1.03
        sl_coeff = 0.997 if is_forex else 0.98
        
        tp = current * tp_coeff if "BUY" in status else current * (2 - tp_coeff)
        sl = current * sl_coeff if "BUY" in status else current * (2 - sl_coeff)

        name = "🌕 XAU/USD (Gold)" if "XAU" in symbol else f"💎 {symbol}"
        return (f"{name} **Tahlili**\n\n"
                f"📊 Signal: {status}\n"
                f"🎯 Narx: {current:,.2f}\n"
                f"✅ Take-Profit: {tp:,.2f}\n"
                f"🛑 Stop-Loss: {sl:,.2f}")
    except:
        return "⚠️ Ma'lumot olishda xatolik yuz berdi."

# --- MENYULAR ---
def main_menu():
    kb = [
        [types.KeyboardButton(text="💰 Narxlar"), types.KeyboardButton(text="🚨 Signallar")],
        [types.KeyboardButton(text="🌍 Yangiliklar"), types.KeyboardButton(text="📈 Tahlil")],
        [types.KeyboardButton(text="🇺🇿 Valyuta Kursi"), types.KeyboardButton(text="🔝 Top 5 Kripto")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def signal_menu():
    kb = [
        [types.KeyboardButton(text="🪙 Kripto Signallar"), types.KeyboardButton(text="💱 Forex Signallar")],
        [types.KeyboardButton(text="⬅️ Orqaga")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def forex_list():
    kb = [
        [types.KeyboardButton(text="🌕 XAU/USD (GOLD)"), types.KeyboardButton(text="🇪🇺 EUR/USD")],
        [types.KeyboardButton(text="⬅️ Signallarga qaytish")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# --- HANDLERLAR ---
@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    await m.answer("🚀 WinnerMaster PRO ishga tushdi!", reply_markup=main_menu())

@dp.message(F.text == "🚨 Signallar")
async def signals_main(m: types.Message):
    await m.answer("Bozorni tanlang:", reply_markup=signal_menu())

@dp.message(F.text == "💱 Forex Signallar")
async def forex_main(m: types.Message):
    await m.answer("Instrumentni tanlang:", reply_markup=forex_list())

@dp.message(F.text == "🌕 XAU/USD (GOLD)")
async def gold_sig(m: types.Message):
    await m.answer(get_signal_data("XAUUSD", True), parse_mode="Markdown")

@dp.message(F.text == "⬅️ Signallarga qaytish")
async def back_to_sig(m: types.Message):
    await m.answer("Signallar bo'limi:", reply_markup=signal_menu())

@dp.message(F.text == "⬅️ Orqaga")
async def back_to_main(m: types.Message):
    await m.answer("Asosiy menyu:", reply_markup=main_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
