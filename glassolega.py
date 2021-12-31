from os import sep
from auth import token
from aiogram import Bot, Dispatcher, executor, types


bot = Bot(token=token, parse_mode="Markdown")
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("Привет! Введи модель телефона, чтобы найти совместимое защитное стекло.")

@dp.message_handler()
async def echo(message: types.Message):
    db_list = read_file()
    answers = find_element(message.text, db_list)

    if answers:
        for index, answer in enumerate(answers):
            print(message.text + " : " + answer)
            await message.answer('Совместимые между собой модели:\n\n' + answer)
            if index == 2:
                break
    else:
        await message.answer('Нет совместимых')
    #answer = answers[0] if answers else "Нет совместимых"

def read_file():
    with open('glassolega.txt', 'r') as fp:
        data = fp.read()

    return data.splitlines()

def find_element(message, db_list):
    is_elem = lambda x: x.lower().find(message.lower()) > 0
    elems = filter(is_elem, db_list)
    return list(elems)

def main():
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()