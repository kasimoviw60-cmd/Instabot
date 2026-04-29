import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# --- 1. RENDER UCHUN WEB SERVER (BOT O'CHIB QOLMASLIGI UCHUN) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run():
    # Render PORT muhit o'zgaruvchisini beradi, bo'lmasa 10000 ishlatiladi
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# -------------------------------------------------------

# Bot sozlamalari
API_TOKEN = '8618465943:AAGhxllucMhyGQOBXmQy9-dFL88lGV9r-CA'
ADMIN_ID = 6052580480 
CHANNEL_ID = "@instagram_kasimov"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# --- Ma'lumotlar bazasi (Oddiy fayl tizimi) ---
def add_user(user_id):
    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as f:
            f.write(f"{user_id}\n")
    else:
        with open("users.txt", "r") as f:
            users = f.read().splitlines()
        if str(user_id) not in users:
            with open("users.txt", "a") as f:
                f.write(f"{user_id}\n")

def count_users():
    if not os.path.exists("users.txt"):
        return 0
    with open("users.txt", "r") as f:
        return len(f.read().splitlines())

# --- Tugmalar (Keyboards) ---
def get_main_menu(user_id):
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add(KeyboardButton("HASHTAG 📊"), KeyboardButton("NAKRUTKA🎁"))
    menu.add(KeyboardButton("Admin habar☎️"))
    if user_id == ADMIN_ID:
        menu.add(KeyboardButton("STAT 📊"))
    return menu

hashtag_inline = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Heshteg olish", url="https://snaplytics.io/instagram-caption-copy/"),
    InlineKeyboardButton("Qoʻllanma📑", url="https://t.me/instagram_kasimov")
)

nakrutka_inline = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Nakrutka urish📌", url="https://leofame.com/free-instagram-views")
)

check_sub_inline = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Kanalga a'zo bo'lish", url=f"https://t.me/{CHANNEL_ID[1:]}"),
    InlineKeyboardButton("Tekshirish ✅", callback_data="check_subs")
)

# --- Funksiyalar ---
async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# --- Handlerlar ---

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    add_user(message.from_user.id)
    
    if await is_subscribed(message.from_user.id):
        text = (
            "Assalomu alaykum! 👋\n\n"
            "Botimiz orqali oʻzingiz hohlagan TOP dagi heshteglarni olishingiz mumkin! 📊\n\n"
            "Va yangi bepul nakrutka boʻlimini ham sizga sovgʻa sifatida qoʻshdik! 😍\n\n"
            "Tugmalardan foydalanib oʻzingizga keraklisini tanlang! 👇"
        )
        await message.answer(text, reply_markup=get_main_menu(message.from_user.id))
    else:
        await message.answer(f"Botdan foydalanish uchun {CHANNEL_ID} kanaliga obuna bo'lishingiz shart!", 
                             reply_markup=check_sub_inline)

@dp.callback_query_handler(text="check_subs")
async def check_callback(call: types.CallbackQuery):
    if await is_subscribed(call.from_user.id):
        await call.message.delete()
        await start_command(call.message)
    else:
        await call.answer("Siz hali a'zo bo'lmadingiz! ❌", show_alert=True)

@dp.message_handler(lambda message: message.text == "STAT 📊")
async def stat_handler(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        total = count_users()
        await message.answer(f"📊 <b>Bot statistikasi:</b>\n\n"
                             f"👥 Jami foydalanuvchilar: <b>{total} ta</b>\n"
                             f"📢 Kanal: {CHANNEL_ID}", parse_mode="HTML")

@dp.message_handler(lambda message: message.text == "HASHTAG 📊")
async def hashtag_handler(message: types.Message):
    await message.answer("Heshteg olish uchun pastdagi tugmani bosing va video LINK ni yuboring! 👇",
                         reply_markup=hashtag_inline)

@dp.message_handler(lambda message: message.text == "NAKRUTKA🎁")
async def nakrutka_handler(message: types.Message):
    text = ("Nakrutka bonuslarimiz!🎉\n"
            "Har xil nakrutkalar mavjud! \n"
            "2000+ koʻrishlar va barcha xizmatlar! 👨🏻‍💻\n"
            "Har kuni bepul limit! ⏳♻️\n"
            "Pastagi tugmani bosing! Batafsil👇")
    await message.answer(text, reply_markup=nakrutka_inline)

@dp.message_handler(lambda message: message.text == "Admin habar☎️")
async def admin_contact_handler(message: types.Message):
    await message.answer("Adminga murojatingiz boʻlsa pastda yozib qoldiring! 👇\n(Xabaringiz avtomatik adminga yuboriladi)")

# --- 2. FOYDALANUVCHILARNI TUGMALARGA YO'NALTIRISH VA ADMINGA XABAR ---
@dp.message_handler(content_types=['text'])
async def forward_to_admin(message: types.Message):
    # Tugmalar ro'yxati
    main_buttons = ["HASHTAG 📊", "NAKRUTKA🎁", "Admin habar☎️", "STAT 📊"]
    
    # Agar foydalanuvchi tugmani bosmasdan nimadir yozsa (masalan, link)
    if message.text not in main_buttons:
        # Foydalanuvchiga javob
        await message.reply("Iltimos, botdan foydalanish uchun tugmalardan foydalaning! 📊\n"
                             "Heshteg olish yoki Nakrutka boʻlimini tanlang. 👇", 
                             reply_markup=get_main_menu(message.from_user.id))
    
    # Har qanday holatda ham yozilgan matnni adminga nusxasini yuborish
    await bot.send_message(ADMIN_ID, 
                           f"📩 <b>Yangi xabar/Link!</b>\n\n"
                           f"👤 Kimdan: @{message.from_user.username}\n"
                           f"🆔 ID: <code>{message.from_user.id}</code>\n"
                           f"📝 Matn: {message.text}")

if __name__ == '__main__':
    # Render o'chirib qo'ymasligi uchun web-serverni yoqamiz
    keep_alive()
    # Botni ishga tushiramiz
    executor.start_polling(dp, skip_updates=True)
    
