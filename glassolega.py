from auth import token
from aiogram import Bot, Dispatcher, executor, types


bot = Bot(token=token, parse_mode="Markdown")
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("Привет! Введите модель телефона, чтобы найти совместимое защитное стекло.")

@dp.message_handler()
async def echo(message: types.Message):
    add_username_to_file(message.from_user.username)
    answers = find_element(message.text)
    print('*************')
    print(search_for_full_match(message.text))
    print('*************')
    if answers:
        print(message.from_user.username + " " + message.text + ":")
        await message.answer('📲 Поиск по *«' + message.text + '»*:')
        for index, answer in enumerate(answers):
            print("→→→ " + answer)
            await message.answer('Совместимые между собой модели:\n\n' + answer)
            if index == 2:
                break
    else:
        await message.answer('Нет совместимых')

def add_username_to_file(username):
    with open('usernames.txt','a') as file:
        file.write(username + "\n")


def read_file():
    with open('glassolega.txt', 'r') as fp:
        data = fp.read()
    return data.splitlines()

def find_element(message):
    is_elem = lambda x: x.lower().find(message.lower()) != -1
    elems = filter(is_elem, list_of_glasses)
    return list(elems)

def search_for_full_match(message_from_user):
    results = []
    for line in list_of_glasses:
        compatible_phones = line.split('/')
        for compatible_phone in compatible_phones:
            if compatible_phone.lower() == message_from_user.lower():
                results.append(compatible_phones)
    return results

def main():
    global list_of_glasses
    list_of_glasses = read_file()
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()