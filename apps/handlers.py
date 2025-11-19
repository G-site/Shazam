from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)


from apps.database import set_user


router = Router()


start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ℹ️ О нас', callback_data='about')],
    [InlineKeyboardButton(text='❓ FAQ', callback_data='instruction')]
    ])
about_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📣 Telegram-канал', url='https://t.me/+_9w-PYa9LQJlMGUy')],
    [InlineKeyboardButton(text='🛠 Поддержка', url='https://t.me/orlovurasuper')],
    [InlineKeyboardButton(text='🤝 Поделиться', url='https://t.me/share/url?url=По этой ссылке можно найти любую песню👉 t.me/shazam_W_bot')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='start')]
    ])
instruction_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад', callback_data='start')]
    ])


@router.message(CommandStart())
async def start(message: Message):
    await set_user(message.from_user.id, message.from_user.username,  message.from_user.first_name)
    await message.answer(text="👋 <b>Привет, меломан!</b>\nЯ — твой музыкальный помощник 🎧\n\n🎶 Отправь мне песню, запись или голосовое сообщение — и я скажу, <b>что это за трек</b>, кто его исполнил и где его послушать 💿\n\n✨ <b>Что я умею:</b>\n🎵 Распознаю песни по аудио\n🔗 Показываю ссылки на треки\n💬 Отвечаю быстро и с настроением\n\n👇 Выбери действие из меню или просто отправь аудио!", reply_markup=start_menu, parse_mode="HTML")


@router.message(Command('about'))
async def about(message: Message):
    await message.answer(text="🎶 <b>О нас</b>\n\nПривет! 👋\nЯ — музыкальный бот, который помогает тебе <b>узнавать песни</b> по аудио и голосовым 🎧\n\nПросто отправь фрагмент песни — и я найду её название, исполнителя и ссылку 💫\n\n✨ Музыка ближе, чем кажется!\nСпасибо, что пользуешься нашим ботом ❤️", reply_markup=about_menu, parse_mode="HTML")


@router.callback_query(F.data == 'about')
async def about2(callback: CallbackQuery):
    await callback.message.edit_text(text="🎶 <b>О нас</b>\n\nПривет! 👋\nЯ — музыкальный бот, который помогает тебе <b>узнавать песни</b> по аудио и голосовым 🎧\n\nПросто отправь фрагмент песни — и я найду её название, исполнителя и ссылку 💫\n\n✨ Музыка ближе, чем кажется!\nСпасибо, что пользуешься нашим ботом ❤️", reply_markup=about_menu, parse_mode="HTML")
    await callback.answer("ℹ️ О нас")


@router.callback_query(F.data == 'instruction')
async def instruction(callback: CallbackQuery):
    await callback.message.edit_text(text="❓ <b>Частые вопросы (FAQ)</b>\n\n🎧 <b>Как распознать песню?</b>\nПросто отправь мне аудио, голосовое или короткий фрагмент трека — я всё сделаю сам 🎶\n\n📂 <b>Какие форматы поддерживаются?</b>\nmp3, m4a, ogg, wav и Telegram voice 🎙️\n\n⏱️ <b>Сколько ждать результат?</b>\nОбычно 3–10 секунд, в зависимости от длины записи ⚡\n\n🚫 <b>Песня не найдена?</b>\nПопробуй отправить более чёткий отрывок без посторонних шумов 🎵\n\n💡 <i>Совет:</i>\nЛучше всего бот распознаёт фрагменты с вокалом 🎤", reply_markup=instruction_menu, parse_mode="HTML")
    await callback.answer("❓ FAQ")


@router.callback_query(F.data == 'start')
async def start2(callback: CallbackQuery):
    await callback.message.edit_text(text="👋 <b>Привет, меломан!</b>\nЯ — твой музыкальный помощник 🎧\n\n🎶 Отправь мне песню, запись или голосовое сообщение — и я скажу, <b>что это за трек</b>, кто его исполнил и где его послушать 💿\n\n✨ <b>Что я умею:</b>\n🎵 Распознаю песни по аудио\n🔗 Показываю ссылки на треки\n💬 Отвечаю быстро и с настроением\n\n👇 Выбери действие из меню или просто отправь аудио!", reply_markup=start_menu, parse_mode="HTML", disable_web_page_preview=True)
    await callback.answer("📋 Меню")


@router.message(Command('instruction'))
async def instruction2(message: Message):
    await message.answer(text="❓ <b>Частые вопросы (FAQ)</b>\n\n🎧 <b>Как распознать песню?</b>\nПросто отправь мне аудио, голосовое или короткий фрагмент трека — я всё сделаю сам 🎶\n\n📂 <b>Какие форматы поддерживаются?</b>\nmp3, m4a, ogg, wav и Telegram voice 🎙️\n\n⏱️ <b>Сколько ждать результат?</b>\nОбычно 3–10 секунд, в зависимости от длины записи ⚡\n\n🚫 <b>Песня не найдена?</b>\nПопробуй отправить более чёткий отрывок без посторонних шумов 🎵\n\n💡 <i>Совет:</i>\nЛучше всего бот распознаёт фрагменты с вокалом 🎤", reply_markup=instruction_menu, parse_mode="HTML")
