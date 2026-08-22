import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = os.getenv("8930512670:AAG_HAqtzs8Kb6Fp6gEE-_JDmKTTvqgsJu0")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(lambda message: message.text and message.text.startswith(".spam"))
async def spam_command(message: Message):
    try:
        if message.chat.type != "private":
            await message.reply("❌ Я работаю только в личных сообщениях! Напишите мне в ЛС.")
            return
        
        parts = message.text.split(maxsplit=2)
        
        if len(parts) < 3:
            await message.reply("❌ Формат: .spam <текст> <количество>")
            return
        
        text = parts[1]
        count = int(parts[2])
        
        if count > 50:
            await message.reply("⚠️ Максимум 50 сообщений за раз!")
            return
        
        if count < 1:
            await message.reply("❌ Количество должно быть больше 0!")
            return
        
        sent_count = 0
        for i in range(count):
            try:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=text
                )
                sent_count += 1
                await asyncio.sleep(0.1)
            except Exception as e:
                logging.error(f"Ошибка отправки: {e}")
                break
        
        if sent_count > 0:
            await message.answer(f"✅ Отправлено {sent_count} сообщений")
            
    except ValueError:
        await message.reply("❌ Количество должно быть числом! Пример: .spam привет 5")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.reply("❌ Произошла ошибка")

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "🤖 Бот для спама в личных сообщениях\n\n"
        "Использование:\n"
        ".spam <текст> <количество>\n\n"
        "Пример:\n"
        ".spam привет 10\n\n"
        "⚠️ Максимум 50 сообщений за раз\n"
        "🔄 Работает 24/7\n\n"
        "❗ Работает ТОЛЬКО в личных сообщениях"
    )

@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "📚 Помощь:\n\n"
        "1. Напишите мне в личные сообщения\n"
        "2. Отправьте .spam текст количество\n\n"
        "Пример:\n"
        ".spam привет 10\n\n"
        "⚠️ Я не работаю в группах!"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
