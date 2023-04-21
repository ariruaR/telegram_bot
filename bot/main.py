import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command,CommandObject
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
import os
from function import *
#? ТЕХНИЧЕСКАЯ СОСТАВЛЯЮЩАЯ
# session = AiohttpSession(proxy="http://proxy.server:3128")
load_dotenv()
HELP = f'Это бот, который основан на нейросети ChatGPT, разработанной корпорацией OpenAi\nРазработчик конкретно этого бота: @ARIRUAR'
START = f'/question "текст вопроса" - вопрос ChatGPT\n/image "описание картинки" - сгенерировать картинку\nЧтобы увидеть информацию про бота /help'
TOKEN = os.getenv('TELEGRAM_API_KEY')
openai.api_key = os.getenv('OPENAI_API_KEY')
#? САМ БОТ
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
async def start():
    await dp.start_polling(bot)

#? START
@dp.message(Command("start"))
async def message_handler(message: types.Message) -> None:
    await message.answer(START)
#? HELP
@dp.message(Command("help"))
async def message_handler(message: types.Message) -> None:
    await message.answer(HELP)
#? QUESTION AI
@dp.message(Command("question", "quest", "q"))
async def handle_message(message: types.Message) -> None:
  try:
        func_name = 'quest_func'
        log_start(func_name)
        #? Получаем текст сообщения от пользователя
        user_input = message.text
        if user_input == 'кто самый тупой человек во вселенной':
            await message.reply(f'ВСЕ ЗНАЮТ ЧТО ЭТО\nМИХАИЛ ТРЮЮЮЮЮЮЮПИН!!!!!!!')
            log_end(func_name)
            return
        await message.answer('Запрос обратывается, пожалуйста подождите')
        er = check_len(user_input)
        ai_answer = get_openai(er,func_name,user_input)
        await message.answer(ai_answer)     
        if er == True:
            await message.answer(f'Длина запроса не должна превышать 250 символов')
            log_end(func_name, f'end for error')
  except Exception as e:
        await message.answer('Произошла какая-то ошибка, повторите позднее')
        print(f'ERROR: {e} ')
#? IMAGE
@dp.message(Command("image", "img", "i"))
async def generate_image(message: types.Message):
    try:
          
            #? Отправляем запрос DALL-E
            func_name = 'image_func'
            log_start(func_name)
            await message.answer('Запрос обратывается, пожалуйста подождите')
            user_desc = message.text
            print(user_desc)
            response = openai.Image.create(
            prompt=user_desc,
            n=1,
            size="1024x1024")
            image_url = response['data'][0]['url']
            log_end(func_name)
            #? Получаем картинку
            await bot.send_photo(chat_id=message.chat.id, photo=image_url)
    except Exception as e:
          await message.answer('Произошла какая-то ошибка, повторите позднее')
          print(f'ERROR: {e} ')
#? ADMIN LOGING
@dp.message(Command("admin", "adm", "a"))
async def auth(message: types.Message, command: CommandObject):
  try:
    if command.args:
      auth_login = message.from_user.username
      print(auth_login)
      auth_password = command.args
      check = admin_panel(auth_login, auth_password)
      print(auth_password)
      if check == True:
          await message.answer('Авторизация прошла успешно')
      if check == False:
          await message.answer('Неверный логин или пароль')
  except Exception as e:
      await message.answer('Произошла непредвиденная ошибка')
      print(f'ERROR: {e}')
#? RUN BOT
if __name__ == '__main__':
    asyncio.run(start())