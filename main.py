import os
import asyncio
from aiohttp import web

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
import yt_dlp

# ======================
# TOKEN
# ======================
TOKEN = "8618465943:AAERniDYzZn1C5ujZVcJEEfJd21iOjoMh9g"

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ======================
# START COMMAND
# ======================
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Instagram link yubor 📩")


# ======================
# VIDEO DOWNLOAD HANDLER
# ======================
@dp.message(F.text)
async def download_video(message: Message):
    url = message.text.strip()

    if "instagram.com" not in url:
        return await message.answer("Faqat Instagram link yubor!")

    await message.answer("Yuklanmoqda ⏳")

    file_name = f"video_{message.from_user.id}.mp4"

    ydl_opts = {
        "outtmpl": file_name,
        "format": "best",
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        caption = info.get("description", "Instagram video")[:1000]

        video = FSInputFile(file_name)
        await message.answer_video(video=video, caption=caption)

        os.remove(file_name)

    except Exception as e:
        await message.answer("Video yuklab bo‘lmadi ❌")


# ======================
# WEB SERVER (Render uchun)
# ======================
async def handle(request):
    return web.Response(text="Bot is running")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)

    await site.start()


# ======================
# MAIN
# ======================
async def main():
    asyncio.create_task(web_server())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
