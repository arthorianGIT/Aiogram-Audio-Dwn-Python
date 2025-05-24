from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from os import getenv
from dotenv import load_dotenv
from core import download_audio, download_info

load_dotenv('.env')
bot_key = getenv('bot_key')
channel_id = getenv('channel_id')

bot = Bot(bot_key)
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(f'Hello {message.from_user.full_name}\nSend me a url and i download audio for you!')

async def bot_download(url, kbps):
    if url.startswith('http'):
        outtmpl = await download_audio(url, kbps)
        audio_file = types.FSInputFile(f'E:/test_videos_audios/{outtmpl}.mp3')
        thumbnail = types.FSInputFile(f'E:/test_videos_audios/{outtmpl}.jpeg')
        await bot.send_audio(channel_id, audio_file, caption='📢 NEW SHITPOST', request_timeout=120, thumbnail=thumbnail)

@dp.message()
async def audio_info(message: types.Message):
    if message.text.startswith('http'):
        global url
        url = message.text
        markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="64kbps", callback_data="64"),
            types.InlineKeyboardButton(text="128kbps", callback_data="128"),
            types.InlineKeyboardButton(text="192kbps", callback_data="192"),
            types.InlineKeyboardButton(text="320kbps", callback_data="320")
        ]])
        info_tuple = await download_info(message.text)
        await message.answer(f'Title: {info_tuple[0]}\nAuthor: {info_tuple[1]}\nDate: {info_tuple[2]}', reply_markup=markup)

@dp.callback_query()
async def kbps_data(call: types.CallbackQuery):
    global url
    if call.data == '64':
        await bot_download(url, call.data)
    elif call.data == '128':
        await bot_download(url, call.data)
    elif call.data == '192':
        await bot_download(url, call.data)
    elif call.data == '320':
        await bot_download(url, call.data)

async def main():
    await dp.start_polling(bot)