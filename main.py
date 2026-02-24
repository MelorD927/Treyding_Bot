import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# BotFather bergan YANGI tokenni shu yerga qo'ying
API_TOKEN = '8176485041:AAF5_DipZmFT3w5S5SLpI0QWnfbY4UPirvI' 

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer("✅ Bot muvaffaqiyatli ulandi va ishlayapti!")

async def main():
    # Eski webhook ulanishlarini butunlay tozalash
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
