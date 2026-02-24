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

# --- PROFESSIONAL TAHLIL (Yengil variant) ---
def get_signal_logic(symbol, is_forex=False):
    try:
        # Tilla uchun PAXG, boshqalar uchun o'zi
        api_sym = "PAXGUSDT" if "XAU" in symbol else symbol
        url = f"https://api.binance.com/api/v3/klines?symbol={api_sym}&interval=1h&limit=20"
        res = requests.get(url, timeout=10).json()
        
        # Narxlarni olish
        closes = [float(c[4]) for c in res]
        current = closes[-1]
        ma = sum(closes) / len(closes) # O'rtacha (MA20)

        # Signal mantiqi
        if current < ma:
            status = "🟢 BUY (Sotib olish)"
            tp = current * (1.03 if not is_forex else 1.005)
            sl = current * (0.98 if not is_forex else 0.997)
        else:
            status = "🔴 SELL (Sotish)"
            tp = current * (0.97 if not is_forex else 0.995)
            sl = current * (1.02 if not is_forex else 1.003)

        name = "🌕 XAU/USD (Gold)" if "XAU" in symbol else f"💎 {symbol}"
        return (f"{name} **Tahlili (MA20)**\n\n"
                f"📊 Signal: {status}\n"
                f"🎯 Hozirgi narx: {current:,.2f}\n"
                f"✅ Take-Profit: {tp:,.2f}\n"
                f"🛑 Stop-Loss: {sl:,.2f}")
    except:
        return "⚠️ Hozirda ma'lumot olishning imkoni bo'lmadi."

# --- MENYULAR ---
def main_menu():
    return types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="💰 Narxlar"), types.KeyboardButton(text="🚨 Signallar")],
        [types.KeyboardButton(text="🌍 Yangiliklar"), types.KeyboardButton(text="📈 Tahlil")],
        [types.KeyboardButton(text="🇺🇿 Valyuta Kursi"), types.KeyboardButton(text="🔝 Top 5 Kripto")]
    ], resize_keyboard=True)

def signal_menu():
    return types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="🪙 Kripto Signallar"), types.KeyboardButton(text="💱 Forex Signallar")],
        [types.KeyboardButton(text="⬅️ Orqaga")]
    ], resize_keyboard=True)

def forex_list():
    return types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="🌕 XAU/USD (GOLD)"), types.KeyboardButton(text="🇪🇺 EUR/USD")],
        [types.KeyboardButton(text="⬅️ Signallarga qaytish")]
    ], resize_keyboard=True)

# --- HANDLERS ---
@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer("🚀 WinnerMaster PRO Terminaliga xush kelibsiz!", reply_markup=main_menu())

@dp.message(F.text == "🚨 Signallar")
async def sig_main(m: types.Message):
    await m.answer("Bozorni tanlang:", reply_markup=signal_menu())

@dp.message(F.text == "💱 Forex Signallar")
async def fx_list(m: types.Message):
    await m.answer("Instrumentni tanlang:", reply_markup=forex_list())

@dp.message(F.text == "🌕 XAU/USD (GOLD)")
async def gold_sig(m: types.Message):
    await m.answer(get_signal_logic("XAUUSD", True), parse_mode="Markdown")

@dp.message(F.text == "⚡️ BTC/USDT")
async def btc_sig(m: types.Message):
    await m.answer(get_signal_logic("BTCUSDT"), parse_mode="Markdown")

@dp.message(F.text == "⬅️ Signallarga qaytish")
async def back_sig(m: types.Message):
    await m.answer("Signallar bo'limi:", reply_markup=signal_menu())

@dp.message(F.text == "⬅️ Orqaga")
async def back_main(m: types.Message):
    await m.answer("Asosiy menyu:", reply_markup=main_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
