import asyncio
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- KONFIGURATSIYA ---
API_TOKEN = '8176485041:AAHOcooQBvWgC0sxdbebJpOKnY8ab1zsHy4'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- BOZOR TAHLILI (MA20) ---
def get_signal_analysis(symbol, is_forex=False):
    try:
        # Tilla uchun PAXGUSDT, Kripto uchun o'zi
        api_sym = "PAXGUSDT" if "XAU" in symbol else symbol
        url = f"https://api.binance.com/api/v3/klines?symbol={api_sym}&interval=1h&limit=20"
        res = requests.get(url, timeout=10).json()
        
        closes = [float(c[4]) for c in res]
        current = closes[-1]
        ma = sum(closes) / len(closes) # Bozor tahlili asosi (MA)

        status = "🟢 BUY" if current < ma else "🔴 SELL"
        tp_ratio = 1.005 if is_forex else 1.03
        sl_ratio = 0.997 if is_forex else 0.98

        if "BUY" in status:
            tp, sl = current * tp_ratio, current * sl_ratio
        else:
            tp, sl = current * (2 - tp_ratio), current * (2 - sl_ratio)

        name = "🌕 XAU/USD (Gold)" if "XAU" in symbol else f"💎 {symbol}"
        return (f"{name} **BOZOR TAHLILI**\n\n"
                f"📊 Signal: {status}\n"
                f"🎯 Narx: {current:,.2f}\n"
                f"✅ Take-Profit: {tp:,.2f}\n"
                f"🛑 Stop-Loss: {sl:,.2f}")
    except:
        return "⚠️ Bozor ma'lumotlarini olishda xatolik."

# --- ASOSIY TUGMALAR ---
def main_kb():
    return types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="🚨 Signallar"), types.KeyboardButton(text="🇺🇿 Valyuta Kursi")],
        [types.KeyboardButton(text="🔝 Top 5 Kripto")]
    ], resize_keyboard=True)

def signal_kb():
    return types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="🪙 BTC/USDT"), types.KeyboardButton(text="🌕 XAU/USD (GOLD)")],
        [types.KeyboardButton(text="⬅️ Orqaga")]
    ], resize_keyboard=True)

# --- HANDLERLAR ---
@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer("🤖 **WinnerMaster** ishga tushdi! Bozor tahlili yoniq.", reply_markup=main_kb())

@dp.message(F.text == "🚨 Signallar")
async def sig_menu(m: types.Message):
    await m.answer("Tahlil uchun instrumentni tanlang:", reply_markup=signal_kb())

@dp.message(F.text == "🪙 BTC/USDT")
async def btc_sig(m: types.Message):
    await m.answer(get_signal_analysis("BTCUSDT"), parse_mode="Markdown")

@dp.message(F.text == "🌕 XAU/USD (GOLD)")
async def gold_sig(m: types.Message):
    await m.answer(get_signal_analysis("XAUUSD", True), parse_mode="Markdown")

@dp.message(F.text == "🇺🇿 Valyuta Kursi")
async def rates(m: types.Message):
    try:
        res = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()
        usd = next(i for i in res if i["Code"] == "USD")
        await m.answer(f"🇺🇿 **MB Kursi:**\n1 USD = {usd['Rate']} so'm")
    except:
        await m.answer("⚠️ Kursni olishda xatolik.")

@dp.message(F.text == "⬅️ Orqaga")
async def back(m: types.Message):
    await m.answer("Asosiy menyu:", reply_markup=main_kb())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
