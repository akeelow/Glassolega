from auth import token
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton
import re

reg = re.compile('[^a-zA-Z ]')

button_stat = KeyboardButton('📊Статистика')
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_stat)



bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    if message.from_user.username != "akeelow":
        await message.answer("Введите модель телефона.\n" + 
                            "Пример: Samsung Galaxy A52\n" + 
                            "Если ввести не полное название модели телефона, тогда бот найдет больше результатов. Каждый результат это совместимые только между собой модели.")
    else:
        await message.reply("📊Статистика", reply_markup=admin_kb)

@dp.message_handler()
async def echo(message: types.Message):
    if message.text != "📊Статистика":
        if reg.sub('', message.text):
            if message.from_user.username:
                add_username_to_file(message.from_user.username)
            else:
                add_username_to_file(str(message.from_user.id))
            full_match = search_for_full_match(message.text)
            answers = find_element(message.text)

            if full_match:
                await message.answer("📲Совместимые стёкла для «" + message.text + "»:" +
                                    "\n " + "".join(full_match))

            elif answers:
                await message.answer('Идет поиск «' + message.text + '»...')
                for index, answer in enumerate(answers):
                    time.sleep(1)
                    await message.answer('📲' + answer.replace('/', '📲'))
                    if index == 5:
                        break

            else:
                await message.answer('😔Для *«' + message.text + '»* нет совместимых стёкол.')
        else:
            await message.answer('📵 Не похоже на модель телефона 📵')
    else:
        await message.answer(get_stat())

def get_stat():
    users = set(read_file("usernames.txt"))
    return "Users ({0}): {1}".format(len(users), str(users))

def add_username_to_file(username):
    with open('usernames.txt','a') as file:
        file.write(username + "\n")


def read_file(filename):
    with open(filename, 'r') as fp:
        data = fp.read()
    return data.splitlines()

def find_element(message):
    is_elem = lambda x: x.lower().find(message.lower()) != -1
    elems = filter(is_elem, list_of_glasses)
    return list(elems)

def search_for_full_match(message_from_user):
    is_match = lambda x: message_from_user.lower() in x.lower().split('/')
    return list(filter(is_match, list_of_glasses))

def main():
    global list_of_glasses
    list_of_glasses = read_file("glassolega.txt")
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()