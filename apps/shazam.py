from aiogram import Router, F
from aiogram.types import Message
import os
from dotenv import load_dotenv
import aiohttp
import asyncio
from shazamio import Shazam
from pydub import AudioSegment
from pydub.utils import which
import ffmpeg

from bot_instance import bot

shazam_router = Router()

load_dotenv()
TOKEN = os.getenv("TOKEN")


ffmpeg_path = which("ffmpeg")
if not ffmpeg_path:
    raise FileNotFoundError("❌ FFmpeg не найден в системе. Установи через 'apt install ffmpeg' или добавь в PATH")
AudioSegment.converter = ffmpeg_path


async def recognize_song(file_path: str):
    shazam = Shazam()
    try:
        result = await shazam.recognize(file_path)
        return result
    except Exception as e:
        print("Ошибка распознавания Shazamio:", e)
        return None


async def convert_to_wav_normalized(input_path: str, output_path: str):
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(44100).set_channels(2).apply_gain(-audio.max_dBFS)
    audio.export(output_path, format="wav")


@shazam_router.message(F.audio | F.voice)
async def music(message: Message):
    file = message.voice or message.audio
    file_id = file.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    os.makedirs("downloads", exist_ok=True)
    input_file = f"downloads/{message.from_user.id}_input.ogg"
    output_file = f"downloads/{message.from_user.id}_output.wav"
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            with open(input_file, "wb") as f:
                f.write(await resp.read())
    first_msg = await message.answer(text="🎧 <b>Распознаю твою песню...</b> ", parse_mode="HTML")
    await convert_to_wav_normalized(input_file, output_file)
    data = await recognize_song(output_file)
    if data and data.get("track"):
        track = data["track"]
        title = track.get("title", "Неизвестно")
        artist = track.get("subtitle", "Неизвестен")
        link = track["share"]["href"]
        cover = track.get("images", {}).get("coverart", "https://i.postimg.cc/wMYwZNbP/photo-2025-11-06-17-46-35.jpg")
        await first_msg.delete()
        await message.answer_photo(
            photo=cover,
            caption=f"🎉 <b>Песня найдена!</b>\n\n🎵 <b>Название:</b> {title}\n👤 <b>Исполнитель:</b> {artist}\n\n🔗 <a href='{link}'>Слушать трек</a> ",
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    else:
        await first_msg.delete()
        await message.answer(
            "😕 <b>Упс...</b>\nМне не удалось распознать эту песню 🎧\n\nПопробуй отправить <b>более чёткий фрагмент</b> — желательно с вокалом и без шумов 🔊\n\n🎵 <i>Я обязательно попробую снова!</i>",
            parse_mode="HTML"
        )
    try:
        os.remove(input_file)
        os.remove(output_file)
    except FileNotFoundError:
        pass
