import openai
from datetime import datetime
import logging
from dotenv import load_dotenv
import os
logging.basicConfig(level='ERROR', filename='telegram-bot\log.log')
load_dotenv()
# Текстовый ответ на различные команды
HELP = f'Это бот, который основан на нейросети ChatGPT, разработанной корпорацией OpenAi\nРазработчик конкретно этого бота: @ARIRUAR'
START = f'/question "текст вопроса" - вопрос ChatGPT\n/image "описание картинки" - сгенерировать картинку\nЧтобы увидеть информацию про бота /help'
TOKEN = os.getenv('TELEGRAM_API_KEY')
API = os.getenv('OPENAI_API_KEY')
#! ФУНКЦИИ
def get_time():
    now = datetime.now() 
    current_time = now.strftime("%H:%M:%S") 
    return current_time

def start(cr_time):
    print(f'BOT START\nTIME:{cr_time}')

def log_start(func_name):
    start_time = get_time()
    info = f'START {func_name} IS {start_time}'
    print(info)
def log_end(func_name):
    end_time = get_time()
    info = f'END {func_name} IS {end_time}'
    print(info)

def check_len(user_input):
    if len(user_input) >= 250:
        error = True
        return error

def get_openai(er,func_name,user_input):
    if er != True:
          #? Выполняем запрос к API OpenAI, чтобы получить ответ на вопрос пользователя
          completion = openai.ChatCompletion.create( 
      model = 'gpt-3.5-turbo',
      messages = [ 
        {'role': 'user', 'content': user_input}
      ],
      temperature = 0  
    )
          #? Получаем ответ от API OpenAI
          answer = completion['choices'][0]['message']['content']
          log_end(func_name)
          #? Отправляем ответ пользователю
          return answer

def admin_panel(auth_login, auth_password):
    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    if auth_login == login and auth_password == password:
        return True
    else:
        return False

cr_time = get_time()
start(cr_time)
