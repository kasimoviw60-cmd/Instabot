import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
import yt_dlp

TOKEN = "8618465943:AAERniDYzZn1C5ujZVcJEEfJd21iOjoMh9g"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Instagram link yubor.")


@dp.message(F.text)
async def downloader(message: Message):
    url = message.text.strip()

    if "instagram.com" not in url:
        return await message.answer("Instagram link yubor.")

    await message.answer("Yuklanmoqda...")

    file_name = f"{message.from_user.id}.mp4"

    ydl_opts = {
        "outtmpl": file_name,
        "format": "mp4/best"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        caption = info.get("description", "")[:1000]

        video = FSInputFile(file_name)
        await message.answer_video(video=video, caption=caption)

        os.remove(file_name)

    except Exception:
        await message.answer("Video olinmadi.")


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
