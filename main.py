import asyncio
import logging
import requests
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# --- RENDER UCHUN PORT (TEKINGA ISHLASHI UCHUN) ---
PORT = int(os.environ.get("PORT", 8080))

# --- TOKENLAR ---
API_TOKEN = '8176485041:AAHOcooQBvWgC0sxdbebJpOKnY8ab1zsHy4'
NEWS_API_KEY = '632332ae0c46482b96f51b05a1609773'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- RENDER "TIMED OUT" BO'LMASLIGI UCHUN SERVER ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive and running!")

def run_health_check():
    server = HTTPServer(('0.0.0.0', PORT), HealthCheckHandler)
    server.serve_forever()

# --- KLAVIATURA ---
def get_main_menu():
    kb = [
        [types.KeyboardButton(text="💰 Real Narxlar"), types.KeyboardButton(text="🌍 Yangiliklar")],
        [types.KeyboardButton(text="📊 Bozor Tahlili"), types.KeyboardButton(text="📈 Grafika")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# --- BOT BUYRUQLARI ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Assalomu alaykum, {message.from_user.first_name}! Treyding botiga xush kelibsiz.", reply_markup=get_main_menu())

@dp.message(F.text == "💰 Real Narxlar")
async def handle_prices(message: types.Message):
    try:
        # Binance API orqali BTC narxini olish
        btc_res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        eth_res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT").json()
        
        text = (f"📊 **Joriy Narxlar:**\n\n"
                f"BTC/USDT: `${float(btc_res['price']):,.2f}`\n"
                f"ETH/USDT: `${float(eth_res['price']):,.2f}`")
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer("❌ Narxlarni olishda xatolik yuz berdi.")

@dp.message(F.text == "🌍 Yangiliklar")
async def handle_news(message: types.Message):
    try:
        url = f"https://newsapi.org/v2/everything?q=crypto&apiKey={NEWS_API_KEY}&pageSize=3"
        news = requests.get(url).json()
        articles = news.get('articles', [])
        for art in articles:
            await message.answer(f"📰 **{art['title']}**\n\n{art['description']}\n[Batafsil]({art['url']})", parse_mode="Markdown")
    except:
        await message.answer("❌ Yangiliklarni yuklashda xatolik.")

# --- ASOSIY ISHGA TUSHIRISH ---
async def main():
    # Render-ni "uxlatib" qo'ymaslik uchun serverni yoqamiz
    Thread(target=run_health_check, daemon=True).start()
    logging.info(f"Health check server started on port {PORT}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
