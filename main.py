import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from deep_translator import GoogleTranslator # Tarjimon kutubxonasi

# 1. KALITLAR
API_TOKEN = '8176485041:AAGdq2QtQbJnh_oJSGas5zqBIvZYU1bxS1s' 
NEWS_API_KEY = '632332ae0c46482b96f51b05a1609773' # NewsAPI kalitingiz

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Tarjima funksiyasi
def translate_to_uz(text):
    try:
        return GoogleTranslator(source='auto', target='uz').translate(text)
    except:
        return text # Agar tarjima o'xshamasa, borini qaytaradi

def get_menu():
    btns = [[types.KeyboardButton(text="📊 Bozor Tahlili"), types.KeyboardButton(text="🎯 Signal")],
            [types.KeyboardButton(text="🗞 Dunyo Yangiliklari")]]
    return types.ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True)

def fetch_global_market_news():
    try:
        url = f"https://newsapi.org/v2/everything?q=forex+OR+crypto&language=en&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            if not articles: return "📭 Yangilik topilmadi."
            
            text = "🌍 **DUNYO BOZORI YANGILIKLARI (O'ZBEK TILIDA):**\n\n"
            for art in articles:
                title_en = art.get('title')
                # Sarlavhani o'zbekchaga o'giramiz
                title_uz = translate_to_uz(title_en)
                link = art.get('url')
                source = art.get('source', {}).get('name', 'Manba')
                
                text += f"🏛 **{source}**\n🇺🇿 {title_uz}\n🔗 [O'qish]({link})\n\n"
            return text
        return "❌ Yangiliklarni olishda xatolik."
    except:
        return "❌ Xizmat vaqtincha ishlamayapti."

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await bot.delete_webhook(drop_pending_updates=True)
    await message.answer("🚀 Bot yangilandi! Endi yangiliklar o'zbekchaga tarjima qilinadi.", reply_markup=get_menu())

@dp.message(lambda m: m.text == "🗞 Dunyo Yangiliklari")
async def handle_news(message: types.Message):
    await message.answer("📡 Dunyo xabarlari o'zbek tiliga o'girilmoqda...")
    news_text = fetch_global_market_news()
    await message.answer(news_text, parse_mode="Markdown", disable_web_page_preview=True)

# ... (Analiz va Signal qismlari avvalgidek qoladi)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())