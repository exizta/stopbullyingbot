import asyncio, os
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = [int(x) for x in os.getenv("ADMINS", "").split(",") if x.strip().isdigit()]

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📨 Отправить историю")],
        [KeyboardButton(text="ℹ️ О проекте")],
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Это бот для анонимного сбора историй о буллинге.\n"
        "Вы можете отправить свою историю — она будет передана модератору без указания вашего имени.",
        reply_markup=main_kb
    )

@dp.message(F.text == "ℹ️ О проекте")
async def about(message: Message):
    await message.answer(
        "Этот бот создан для того, чтобы анонимно делиться историями о буллинге.\n"
        "Все сообщения поступают только модератору."
    )

@dp.message(F.text == "📨 Отправить историю")
async def ask_story(message: Message):
    await message.answer("Напишите вашу историю. Она будет отправлена анонимно.")

@dp.message()
async def handle_story(message: Message):
    if not message.text:
        await message.answer("Можно отправлять только текстовые истории.")
        return
    for admin_id in ADMINS:
        try:
            await bot.send_message(admin_id, f"📨 Новая анонимная история:\n\n{message.text}")
        except Exception as e:
            print(f"Не удалось отправить админу {admin_id}: {e}")
    await message.answer("✅ Спасибо! Ваша история отправлена анонимно.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())