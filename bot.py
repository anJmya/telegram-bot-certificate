import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, ADMIN_ID
from sheets import Sheets
from sync import Sync
from certificate import Certificate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class States(StatesGroup):
    waiting_name = State()

# init
bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
scheduler = AsyncIOScheduler()

sheets = Sheets()
sync = Sync(sheets)
cert = Certificate()

@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer("Введите ваше ФИО для получения сертификата:")
    await state.set_state(States.waiting_name)

@dp.message(States.waiting_name)
async def handle_name(message: Message, state: FSMContext):
    name = message.text.strip()
    
    if len(name) < 3:
        await message.answer("Введите полное ФИО")
        return
    
    await message.answer("Поиск...")
    matches = sheets.search_student(name)
    
    if not matches:
        await message.answer(f"'{name}' не найден. Проверьте написание ФИО.")
        await state.clear()
        return
    
    if len(matches) == 1:
        await send_certificate(message, matches[0], state)
    else:
        await show_courses(message, matches, state)

async def show_courses(message, matches, state):
    await state.update_data(matches=matches)
    
    text = f"Найдено {len(matches)} курсов:\n\n"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for i, match in enumerate(matches[:5]):
        course = match['course']
        text += f"{i+1}. {course}\n"
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=f"{i+1}. {course[:30]}", callback_data=f"c_{i}")
        ])
    
    await message.answer(text, reply_markup=keyboard)

@dp.callback_query(F.data.startswith("c_"))
async def handle_course(callback: types.CallbackQuery, state: FSMContext):
    index = int(callback.data.replace("c_", ""))
    data = await state.get_data()
    matches = data['matches']
    
    await callback.answer("Генерирую...")
    await callback.message.edit_reply_markup()
    await send_certificate(callback.message, matches[index], state)

async def send_certificate(message, student, state):
    try:
        print(f"Генерирую сертификат для: {student}")  # Отладка
        
        name = student.get('name', 'Не указано')
        course = student.get('course', 'Не указан') 
        period = student.get('period', 'Не указан')
        cert_num = student.get('num', '№1')
        
        print(f"Данные: name={name}, course={course}, period={period}, num={cert_num}")
        
        # Генерируем PDF
        pdf = cert.generate(name, course, period, cert_num)
        
        file = types.BufferedInputFile(pdf.read(), 
                                     f"Сертификат_{name.replace(' ', '_')}.pdf")
        
        text = f" Ваш сертификат готов!\n\n {name}\n {course}"
        
        await message.answer_document(file, caption=text)
        await state.clear()
        
        print(f"Сертификат успешно отправлен для {name}")
        
    except Exception as e:
        print(f"Ошибка генерации сертификата: {e}")
        import traceback
        traceback.print_exc()  # Полный стек ошибки
        
        await message.answer(" Ошибка генерации сертификата. Обратитесь к менеджеру.")
        await state.clear()


@dp.message(Command("admin"))
async def admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    source_data, target_data = sheets.get_data()  # Статистика по всем данным
    await message.answer(f" Статистика:\nСертификатов: {len(target_data)}\n В форме: {len(source_data)}")

@dp.message(Command("sync"))
async def manual_sync(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    count, students = sync.sync()
    if count:
        text = f"Добавлено {count} студентов:\n" + "\n".join(students[:5])
        await message.answer(text)
    else:
        await message.answer("Новых записей нет")

@dp.message()
async def other(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == States.waiting_name.state:
        await handle_name(message, state)
    else:
        await message.answer("Введите /start")

async def auto_sync():
    """Автосинхронизация"""
    count, students = sync.sync()
    if count:
        text = f"Автосинхронизация: +{count} студентов"
        try:
            await bot.send_message(ADMIN_ID, text)
        except Exception as e:
            print(f"Ошибка уведомления админа: {e}")

async def main():
    # Автосинхронизация каждые 2 часа
    scheduler.add_job(auto_sync, 'interval', hours=2)
    scheduler.start()
    
    print("Бот запущен и готов к работе!")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
