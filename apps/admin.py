import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)


from apps.database import check_admin, get_all_users


admin_router = Router()


admin_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сообщить о тех-перерыве', callback_data='message1')],
    [InlineKeyboardButton(text='Попросить поделиться с другом', callback_data='message2')],
    [InlineKeyboardButton(text='Попросить подписаться на тгк', callback_data='message3')]
    ])
subscribe_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔔 Подписаться', url='https://t.me/+jhfsYb5BsaZlNTI6')]])
share_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔗 Поделиться', url="https://t.me/share/url?url=По этой ссылке можно найти любую песню👉 t.me/shazam_W_bot")]])


@admin_router.message(Command('admin'))
async def admin(message: Message):
    status = await check_admin(message.from_user.id)
    if status == 'M':
        name = message.from_user.first_name
        await message.answer(f"Добро пожаловать в админ-панель, <b>{name}</b>!", reply_markup=admin_menu, parse_mode="HTML")
    else:
        await message.answer(text="⚠️ <b>Упс!</b>\n\nУ тебя нет прав администратора для выполнения этой команды ❌\n\nЕсли ты считаешь, что это ошибка, свяжись с поддержкой 🛠️", parse_mode="HTML")


@admin_router.callback_query(F.data == 'message3')
async def subscribe(callback: CallbackQuery):
    users = await get_all_users()
    sent = 0
    for id in users:
        try:
            await callback.bot.send_message(
                chat_id=id,
                text="📢 <b>Не пропусти новости!</b>\n\nПодписывайся на наш Telegram-канал, чтобы быть в курсе всех обновлений 🎶\n\n🎵 Новые функции\n🔥 Музыкальные подборки\n🎁 Подарки и акции для активных пользователей",
                parse_mode="HTML",
                reply_markup=subscribe_menu
            )
            sent += 1
            await asyncio.sleep(0.5)
        except TelegramAPIError:
            pass
    await callback.answer(f"✅ Отправлено {sent} пользователям!")


@admin_router.callback_query(F.data == 'message2')
async def share(callback: CallbackQuery):
    users = await get_all_users()
    sent = 0
    for id in users:
        try:
            await callback.bot.send_message(
                chat_id=id,
                text="🤝 <b>Поделись с другом!</b>\n\nЕсли тебе нравится наш бот, отправь ссылку другу и помоги ему узнавать песни так же легко 🎶\n\n📩 Просто нажми «Поделиться» и рассылай ссылку\n\n💫 Спасибо за поддержку! ❤️",
                parse_mode="HTML",
                reply_markup=share_menu
            )
            sent += 1
            await asyncio.sleep(0.5)
        except TelegramAPIError:
            pass
    await callback.answer(f"✅ Отправлено {sent} пользователям!")


@admin_router.callback_query(F.data == 'message1')
async def tech(callback: CallbackQuery):
    users = await get_all_users()
    sent = 0
    for id in users:
        try:
            await callback.bot.send_message(
                chat_id=id,
                text="⚠️ <b>Внимание!</b>\n\nЗавтра планируется <b>технический перерыв</b> 🛠️\nВо время него бот может быть недоступен ⏳\n\n🎵 Мы вернёмся как можно скорее, чтобы снова радовать тебя музыкой!\nСпасибо за понимание ❤️",
                parse_mode="HTML"
            )
            sent += 1
            await asyncio.sleep(0.5)
        except TelegramAPIError:
            pass
    await callback.answer(f"✅ Отправлено {sent} пользователям!")
