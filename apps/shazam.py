from aiogram import Router, F
from aiogram.types import Message
import os
from dotenv import load_dotenv
import ffmpeg
import aiohttp
import asyncio
from shazamio import Shazam

from bot_instance import bot

shazam_router = Router()

load_dotenv()
ADMIN = os.getenv("ADMIN")
TOKEN = os.getenv("TOKEN")


async def recognize_song(file_path):
    shazam = Shazam()
    try:
        result = await shazam.recognize_song(file_path)
        return result
    except Exception as e:
        print("Ошибка распознавания Shazamio:", e)
        return None


async def convert_to_mp3(input_path: str, output_path: str):
    ffmpeg_path = os.path.join("ffmpeg", "ffmpeg.exe")
    abs_path = os.path.abspath(ffmpeg_path)
    print("🔍 Проверяю ffmpeg:", abs_path)
    if not os.path.exists(ffmpeg_path):
        raise FileNotFoundError(f"❌ FFmpeg не найден по пути: {abs_path}")
    stream = ffmpeg.input(input_path)
    stream = ffmpeg.output(stream, output_path, format="mp3", acodec="libmp3lame")
    await asyncio.to_thread(
        ffmpeg.run,
        stream,
        cmd=ffmpeg_path,
        overwrite_output=True,
        quiet=True
    )


@shazam_router.message(F.audio | F.voice)
async def music(message: Message):
    file = message.voice or message.audio
    file_id = file.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

    os.makedirs("downloads", exist_ok=True)
    input_file = f"downloads/{message.from_user.id}_input.ogg"
    output_file = f"downloads/{message.from_user.id}_output.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            with open(input_file, "wb") as f:
                f.write(await resp.read())
    await message.answer(text="🎧 <b>Распознаю твою песню...</b> ", parse_mode="HTML")
    await convert_to_mp3(input_file, output_file)
    data = await recognize_song(output_file)
    if data and data.get("track"):
        track = data["track"]
        title = track.get("title", "Неизвестно")
        artist = track.get("subtitle", "Неизвестен")
        await message.delete()
        await message.answer(text=f"🎉 <b>Песня найдена!</b>\n\n🎵 <b>Название:</b> {title}\n👤 <b>Исполнитель:</b> {artist}", parse_mode="HTML", disable_web_page_preview=True)
    else:
        await message.delete()
        await message.answer("😕 <b>Упс...</b>\nМне не удалось распознать эту песню 🎧\n\nПопробуй отправить <b>более чёткий фрагмент</b> — желательно с вокалом и без шумов 🔊\n\n🎵 <i>Я обязательно попробую снова!</i>", parse_mode="HTML")
    try:
        os.remove(input_file)
        os.remove(output_file)
    except FileNotFoundError:
        pass
