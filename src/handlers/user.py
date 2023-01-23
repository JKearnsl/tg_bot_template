from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from models.user import UserStatus
from services import ServiceFactory
from states.user import UserMain


async def user_hello(m: Message, service: ServiceFactory, state: FSMContext):
    await m.reply("Hello, confirmed user!")
    # await state.set_state(UserMain.SOME_STATE)


async def user_unconfirmed(m: Message, service: ServiceFactory, state: FSMContext):
    await m.reply("Hello, unconfirmed user!")


async def user_banend(m: Message, service: ServiceFactory, state: FSMContext):
    await m.reply("Hello, banned user!")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_hello, commands=["start"], user_status=UserStatus.CONFIRMED, state="*")
    dp.register_message_handler(user_unconfirmed, commands=["start"], user_status=UserStatus.UNCONFIRMED, state="*")
    dp.register_message_handler(user_banend, commands=["start"], user_status=UserStatus.BANNED, state="*")
