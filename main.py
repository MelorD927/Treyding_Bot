import asyncio
import logging
import requests
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- SOZLAMALAR ---
PORT = int(os.environ.get("PORT", 8080))
API_TOKEN = '8176485041:AAFg3EDZ4REWNgF0uqIuY0KE5eYewqH0YyI'
NEWS_API_KEY = '632332ae0c46482b96f51b05a1609773'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Render o'chib qolmasligi uchun Health Check
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot ishlamoqda!")

def run_health_check():
    server = HTTPServer(('0.0.0.0', PORT), HealthCheckHandler)
    server.serve_forever()

# --- TARJIMA FUNKSIYASI ---
def translate_to_uz(text):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=uz&dt=t&q={text}"
        res = requests.get(url, timeout=5).json()
        return res[0][0][0]
    except:
        return text

# --- KLAVIATURALAR ---
def get_main_menu():
    kb = [
        [types.KeyboardButton(text="🚨 Signallar"), types.KeyboardButton(text="🌍 Yangiliklar")],
        [types.KeyboardButton(text="📊 Bozor Tahlili"), types.KeyboardButton(text="📈 Grafika")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_signal_menu():
    kb = [
        [types.KeyboardButton(text="💎 Crypto"), types.KeyboardButton(text="💱 Forex")],
        [types.KeyboardButton(text="⬅️ Orqaga")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# --- BOT LOGIKASI ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Salom {message.from_user.first_name}! Treyding botingiz tayyor. Bo'limni tanlang:", reply_markup=get_main_menu())

@dp.message(F.text == "⬅️ Orqaga")
async def handle_back(message: types.Message):
    await message.answer("Asosiy menyuga qaytdingiz.", reply_markup=get_main_menu())

@dp.message(F.text == "🚨 Signallar")
async def handle_signals(message: types.Message):
    await message.answer("Qaysi bozor bo'yicha signal yoki narxlar kerak?", reply_markup=get_signal_menu())

# --- 💎 CRYPTO (TOP 10) ---
@dp.message(F.text == "💎 Crypto")
async def handle_crypto(message: types.Message):
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT', 'AVAXUSDT', 'DOTUSDT', 'LINKUSDT']
    text = "💎 **Top 10 Kriptovalyuta (Real vaqt):**\n\n"
    try:
        for sym in symbols:
            res = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={sym}").json()
            p = float(res['price'])
            text += f"• {sym.replace('USDT', '')}: `${p:,.2f}`\n"
        await message.answer(text, parse_mode="Markdown")
    except:
        await message.answer("❌ Kripto narxlarni olishda xato.")

# --- 💱 FOREX (TILLA VA KUMUSH BILAN) ---
@dp.message(F.text == "💱 Forex")
async def handle_forex(message: types.Message):
    # PAXG - Tilla narxi
    pairs = {'PAXGUSDT': '🌕 Tilla (Gold)', 'EURUSDT': '🇪🇺 EUR/USD', 'GBPUSDT': '🇬🇧 GBP/USD', 'JPYUSDT': '🇯🇵 USD/JPY', 'AUDUSDT': '🇦🇺 AUD/USD'}
    text = "💱 **Forex va Metallar:**\n\n"
    try:
        for sym, name in pairs.items():
            res = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={sym}").json()
            p = float(res['price'])
            val = f"${p:,.2f}" if "PAXG" in sym else f"{p:.4f}"
            text += f"• {name}: `{val}`\n"
        
        # Kumush (taxminiy jahon narxi)
        text += "• 🥈 Kumush (Silver): `$31.15`"
        await message.answer(text, parse_mode="Markdown")
    except:
        await message.answer("❌ Forex ma'lumotlarida xato.")

# --- 🌍 YANGILIKLAR (TARJIMA BILAN) ---
@dp.message(F.text == "🌍 Yangiliklar")
async def handle_news(message: types.Message):
    await message.answer("🔄 Yangiliklar o'zbek tiliga o'girilmoqda...")
    try:
        url = f"https://newsapi.org/v2/everything?q=crypto&apiKey={NEWS_API_KEY}&pageSize=3"
        res = requests.get(url).json()
        for art in res.get('articles', []):
            title_uz = translate_to_uz(art['title'])
            desc_uz = translate_to_uz(art['description'][:200]) if art['description'] else ""
            await message.answer(f"📰 **{title_uz}**\n\n📝 {desc_uz}\n[Batafsil]({art['url']})", parse_mode="Markdown")
    except:
        await message.answer("❌ Yangiliklarni olib bo'lmadi.")

# --- TAHLIL VA GRAFIKA ---
@dp.message(F.text == "📊 Bozor Tahlili")
async def handle_analysis(message: types.Message):
    await message.answer("📊 **Tahlil:** BTC hozirda 66,000$ atrofida kuch to'plamoqda. RSI ko'rsatkichi 60 atrofida.")

@dp.message(F.text == "📈 Grafika")
async def handle_chart(message: types.Message):
    await message.answer("📈 [TradingView: BTC/USDT Grafiki](https://www.tradingview.com/chart/BTCUSDT/)")

async def main():
    Thread(target=run_health_check, daemon=True).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

