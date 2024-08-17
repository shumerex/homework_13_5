from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["Рассчитать", "Информация"]
keyboard.add(*buttons)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я бот помогающий твоему здоровью.", reply_markup=keyboard)
    print("Привет! Я бот помогающий твоему здоровью.")

@dp.message_handler(Text(equals="Рассчитать"))
async def set_age(message=types.Message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message=types.Message, state=FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message=types.Message, state=FSMContext):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message=types.Message, state=FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    calories = 66 + (13.7 * weight) + (5 * growth) - (6.76 * age)

    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал")
    await state.finish()

@dp.message_handler()
async def all_messages(message: types.Message):
    await message.reply("Введи команду /start для начала работы с ботом.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)