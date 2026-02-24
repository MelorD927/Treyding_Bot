import asyncio
import logging
import requests
import random
import pandas as pd  # Ma'lumotlar bilan ishlash uchun eng kuchli kutubxona
import pytz          # Vaqt zonalarini aniq hisoblash uchun
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- KONFIGURATSIYA ---
API_TOKEN = '8176485041:AAHOcooQBvWgC0sxdbebJpOKnY8ab1zsHy4'
NEWS_API_KEY = '5a70717208154109867011d871788220'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- PROFESSIONAL TAHLIL FUNKSIYALARI ---

def get_technical_signal(symbol, is_forex=False):
    """Moving Average va Volatility asosida professional signal"""
    try:
        # Tilla uchun PAXG, Kripto uchun o'z symbol'i
        api_symbol = "PAXGUSDT" if symbol == "XAUUSD" else symbol
        url = f"https://api.binance.com/api/v3/klines?symbol={api_symbol}&interval=1h&limit=50"
        res = requests.get(url, timeout=10).json()
        
        # Pandas orqali ma'lumotlarni tahlil qilish
        df = pd.DataFrame(res, columns=['time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'q_vol', 'trades', 'tb_base', 'tb_quote', 'ignore'])
        df['close'] = df['close'].astype(float)
        
        current_price = df['close'].iloc[-1]
        ma_fast = df['close'].rolling(window=10).mean().iloc[-1]
        ma_slow = df['close'].rolling(window=20).mean().iloc[-1]
        
        # Signal mantiqi: Fast MA Slow MA'dan yuqorida bo'lsa - Trend tepaga
        if ma_fast > ma_slow:
            status = "🟢 BUY (Kuchli trend)"
            tp = current_price * (1.02 if not is_forex else 1.005)
            sl = current_price * (0.99 if not is_forex else 0.997)
        else:
            status = "🔴 SELL (Pasayish trendi)"
            tp = current_price * (0.98 if not is_forex else 0.995)
            sl = current_price * (1.01 if not is_forex else 1.003)
            
        name = "🌕 XAU/USD (Gold)" if symbol == "XAUUSD" else f"💎 {symbol}"
        return (f"{name} **Tahlili**\n\n"
                f"📊 Signal: {status}\n"
                f"🎯 Hozirgi narx: {current_price:,.2f}\n"
                f"✅ Take-Profit: {tp:,.2f}\n"
                f"🛑 Stop-Loss: {sl:,.2f}\n"
                f"📈 MA10: {ma_fast:,.2f} | MA20: {ma_slow:,.2f}")
    except Exception as e:
        return f"⚠️ Tahlil qilishda xatolik: {str(e)}"

# --- MENYULAR ---

def main_menu():
    kb = [
        [types.KeyboardButton(text="💰 Narxlar"), types.KeyboardButton(text="🚨 Signallar")],
        [types.KeyboardButton(text="🌍 Yangiliklar"), types.KeyboardButton(text="📈 Bozor Tahlili")],
        [types.KeyboardButton(text="🇺🇿 Valyuta Kursi"), types.KeyboardButton(text="🔝 Top 5 Kripto")],
        [types.KeyboardButton(text="🕒 Birja Vaqti")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def signal_category_menu():
    kb = [
        [types.KeyboardButton(text="🪙 Kripto Signallar"), types.KeyboardButton(text="💱 Forex Signallar")],
        [types.KeyboardButton(text="⬅️ Orqaga")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def forex_list_menu():
    kb = [
        [types.KeyboardButton(text="🌕 XAU/USD (GOLD)"), types.KeyboardButton(text="🇪🇺 EUR/USD")],
        [types.KeyboardButton(text="⬅️ Signallarga qaytish")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# (Boshqa menyular avvalgi koddagidek qoladi...)

# --- HANDLERS ---

@dp.message(Command("start"))
async def start_cmd(m: types.Message):
    await m.answer("🔥 **WinnerMaster PRO** terminali ishga tushdi. Kuchli tahlil tizimi yoniq.", reply_markup=main_menu())

@dp.message(F.text == "🚨 Signallar")
async def sig_cat(m: types.Message):
    await m.answer("Signal bo'limini tanlang:", reply_markup=signal_category_menu())

@dp.message(F.text == "💱 Forex Signallar")
async def forex_list(m: types.Message):
    await m.answer("Forex yoki Metalni tanlang:", reply_markup=forex_list_menu())

@dp.message(F.text == "🌕 XAU/USD (GOLD)")
async def gold_signal(m: types.Message):
    res = get_technical_signal("XAUUSD", is_forex=True)
    await m.answer(res, parse_mode="Markdown")

@dp.message(F.text == "⬅️ Signallarga qaytish")
async def back_to_sig(m: types.Message):
    await m.answer("Signallar bo'limi:", reply_markup=signal_category_menu())

@dp.message(F.text == "⬅️ Orqaga")
async def back_to_main(m: types.Message):
    await m.answer("Asosiy menyu:", reply_markup=main_menu())

# --- BOTNI ISHGA TUSHIRISH ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
