# Импорты aiogram
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (Message, LabeledPrice, PreCheckoutQuery,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)

# Инициализация роутера
user_router = Router()


# Обработчик команды /start
@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text=f"Привет {message.from_user.username}")
    await message.answer(text="Я бот, который может предоставить доступ в канал и группу с индивидуальными уроками!",
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [InlineKeyboardButton(text="Доступ в группу 5 ⭐", callback_data="group_access")],
                                 [InlineKeyboardButton(text="Доступ в канал 10 ⭐", callback_data="channel_access")],
                                 [InlineKeyboardButton(text="Полный доступ 12 ⭐", callback_data="all_access")],
                             ]
                         ))


# Обработчик команды /paysupport, обязательной для всех платежный ботов
@user_router.message(Command(commands=["paysupport"]))
async def cmd_paysupport(message: Message):
    await message.answer(text="Команда paysupport")


# Обработчик команды /help
@user_router.message(Command(commands=["help"]))
async def cmd_help(message: Message):
    await message.answer(text="Команда help")


# Обработка нажатия на кнопку доступа в группу
@user_router.callback_query(F.data == "group_access")
async def pay_access_group(callback: CallbackQuery):
    await callback.message.answer_invoice(
        provider_token="",
        title="Доступ в группу",
        description="После оплаты вы получаете доступ в нашу закрытую телеграм группу с наставниками!",
        payload="group_access",
        currency="XTR",
        prices=[LabeledPrice(label="Доступ в канал", amount=5)],
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Оплата 5 XTR", pay=True)],
                             [InlineKeyboardButton(text="Отмена ❌", callback_data="cancel")]]
        )
    )
    await callback.answer()


# Обработка нажатия на кнопку доступа в канал
@user_router.callback_query(F.data == "channel_access")
async def pay_access_channel(callback: CallbackQuery):
    await callback.message.answer_invoice(
        provider_token="",
        title="Доступ в канал",
        description="После оплаты вы получаете доступ в наш закрытый телеграм канал с уроками!",
        payload="channel_access",
        currency="XTR",
        prices=[LabeledPrice(label="Доступ в канал", amount=10)],
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Оплата 10 XTR", pay=True)],
                             [InlineKeyboardButton(text="Отмена ❌", callback_data="cancel")]]
        )
    )
    await callback.answer()


# Обработка нажатия на полный доступ
@user_router.callback_query(F.data == "all_access")
async def pay_access_all(callback: CallbackQuery):
    await callback.message.answer_invoice(
        provider_token="",
        title="Доступ в канал и группу",
        description="После оплаты вы получаете доступ в нашу закрытую"
                    " телеграм группу с наставниками, а также в наш телеграм канал с уроками!",
        payload="all_access",
        currency="XTR",
        prices=[LabeledPrice(label="Доступ в группу и канал", amount=12)],
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Оплата 12 XTR", pay=True)],
                             [InlineKeyboardButton(text="Отмена ❌", callback_data="cancel")]]
        )
    )
    await callback.answer()


# Обработка кнопки отмены
@user_router.callback_query(F.data == "cancel")
async def pay_access_cancel(callback: CallbackQuery):
    await callback.message.answer(
        text="Я бот, который может предоставить доступ в канал и группу с индивидуальными уроками!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Доступ в группу 5 ⭐", callback_data="group_access")],
                [InlineKeyboardButton(text="Доступ в канал 10 ⭐", callback_data="channel_access")],
                [InlineKeyboardButton(text="Полный доступ 12 ⭐", callback_data="all_access")],
            ]
        ))
    await callback.answer()


# Промежуточная обработка платежа
@user_router.pre_checkout_query()
async def pre_checkout_query(query: PreCheckoutQuery):
    await query.answer(ok=True)


# Ссылка приглашение в канал
@user_router.message(F.successful_payment.invoice_payload == "channel_access")
async def successful_channel_payment(message: Message):
    await message.answer(
        text=f"Оплата прошла успешно!\nВот id транзакции:\n{message.successful_payment.telegram_payment_charge_id}")
    link = await message.bot.create_chat_invite_link(
        chat_id="@test_kris888",
        member_limit=1
    )
    await message.answer(text=f"Спасибо за покупку!\nВот ссылка на наш канал:\n{link.invite_link}")


# Ссылка приглашение в группу
@user_router.message(F.successful_payment.invoice_payload == "group_access")
async def successful_group_payment(message: Message):
    await message.answer(
        text=f"Оплата прошла успешно!\nВот id транзакции:\n{message.successful_payment.telegram_payment_charge_id}")
    link = await message.bot.create_chat_invite_link(
        chat_id=-4548261452,
        member_limit=1
    )
    await message.answer(text=f"Спасибо за покупку!\nВот ссылка на нашу группу:\n{link.invite_link}")


# Ссылки на полный доступ
@user_router.message(F.successful_payment.invoice_payload == "all_access")
async def successful_all_payment(message: Message):
    await message.answer(
        text=f"Оплата прошла успешно!\nВот id транзакции:\n{message.successful_payment.telegram_payment_charge_id}")
    group_link = await message.bot.create_chat_invite_link(
        chat_id=-4548261452,
        member_limit=1
    )
    channel_link = await message.bot.create_chat_invite_link(
        chat_id="@test_kris888",
        member_limit=1
    )
    await message.answer(text=f"Спасибо за покупку!\nВот ссылка на нашу группу:\n{group_link.invite_link}\n"
                              f"А вот на наш канал:\n{channel_link.invite_link}")
