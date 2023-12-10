from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import json
import asyncio
from tasks import parse
import work_with_date

bot = Bot("6250546591:AAHxsjV-y51EkwJiyasjrwZJt0_v7JzRC1w")
dp = Dispatcher()
mapa = {}



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, я телеграм бот, который позволяет узнать, сколько задач было решено пользователем за какой-то период времени.\nЕсли есть вопросы по работе бота используйте команду /help.")
    await message.answer("Введите имя пользователя статиску которого хотите узнать:")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("""
Команды:
/start - запустить бота
/help - прочитать справочную информацию о боте
Общая информация:
В любой момент вы можете ввести имя пользователя для которого хотите узнать статистику
В любой момент вы можете ввести число от 0 до 11 чтобы выбрать тип временного промежутка, в таком случае статистика посчитается для последнего введённого пользователя
В любой момент вы можете ввести две даты, тогда статистика посчитается для указанного временного промежутка, для пользователя, чей ник вы указали последним
Бот не работает с датами, которые меньше 01.01.1970
""")
    await message.answer("Введите имя пользователя статиску которого хотите узнать:")


@dp.message(F.text.isdigit())
async def type_of_responce(message: types.Message):
    ans = message.text
    nick = mapa[message.chat.id]
    result = []
    if ans == "0":
        result = parse(nick, [0])
    elif ans == "1":
        result = work_with_date.how_solve_today(nick)
    elif ans == "2":
        result = work_with_date.how_solve_in_week(nick)
    elif ans == "3":
        result = work_with_date.how_solve_in_this_week(nick)
    elif ans == "4":
        result = work_with_date.how_solve_in_last_week(nick)
    elif ans == "5":
        result = work_with_date.how_solve_in_month(nick)
    elif ans == "6":
        result = work_with_date.how_solve_in_this_month(nick)
    elif ans == "7":
        result = work_with_date.how_solve_in_last_month(nick)
    elif ans == "8":
        result = work_with_date.how_solve_in_year(nick)
    elif ans == "9":
        result = work_with_date.how_solve_in_this_year(nick)
    elif ans == "10":
        result = work_with_date.how_solve_in_last_year(nick)
    elif ans == "11":
        await message.answer("Введите даты через пробел в формате 'ДД.ММ.ГГГГ'")
    else:
        await message.answer("Выбран недопустимый тип")
    s = ""
    for key in sorted(result[0].keys(), key=lambda x: x if str(type(x)) == "<class 'int'>" else 0):
        s = s + str(key) + ": " + str(result[0][key]) + "\n"
    await message.answer(f"""Всего решено за выбранный период: {result[1]}\n{s}
    """)
    await message.answer("Введите имя пользователя статиску которого хотите узнать, или выберите число если хотите узнать статистику текущего пользователя за другой период:")
    await get_name(message)


@dp.message(F.text.split(".").len() == 5)
async def get_date(message: types.Message):
    dates = message.text.split()
    nick = mapa[message.chat.id]
    try:
        result = work_with_date.how_solve_between(nick, dates[0], dates[1])
    except Exception as err:
        await message.answer(f"Ошибка: {err}\nПроверьте корректность введённой даты")
        return
    s = ""
    for key in sorted(result[0].keys(), key=lambda x: x if str(type(x)) == "<class 'int'>" else 0):
        s = s + str(key) + ": " + str(result[0][key]) + "\n"
    await message.answer(f"Всего решено за выбранный период: {result[1]}\n{s}")
    


@dp.message(F.text)
async def get_name(message: types.Message):
    if not message.text.isdigit():
        mapa[message.chat.id] = message.text
    await message.answer(f"""
        Выберите для какого временного промежутка вы хотите узнать статистику пользователя {mapa[message.chat.id]}
0: за всё время
1: за сегодня
2: за неделю
3: за эту неделю
4: за прошлую неделю
5: за месяц
6: за этот месяц
7: за прошлый месяц
8: за год
9: за этот год
10: за прошлый год
11: с даты1 по дату2
    """)
    builder = ReplyKeyboardBuilder()
    all_types = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    for i in range(len(all_types)):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True),
    )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
