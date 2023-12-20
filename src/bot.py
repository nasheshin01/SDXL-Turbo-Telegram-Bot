import os
import telebot

from sdxl_turbo import SdxlTurbo, SdxlQuery


DEFAULT_MAIN_PROMPT = "beatiful face of bear"


# Функция чтения конфига для получения информации о токене бота
def read_config():
    with open('src\\config.cfg', 'r') as cfg:
        cfg_lines = cfg.readlines()
        
        cfg_dict = {}
        for cfg_line in cfg_lines:
            cfg_line_split = cfg_line.split('=')
            cfg_dict[cfg_line_split[0]] = cfg_line_split[1]

        return cfg_dict


queries = {}

# Функция для проверки того, что сессия для юзера запущена, если нет - создаем сессию
def check_and_create_new_query_if_necessary(chat_id, main_prompt=DEFAULT_MAIN_PROMPT):
    if not chat_id in queries:
        queries[chat_id] = SdxlQuery(main_prompt)


# Функция для генерации и отправки изображения
def generate_and_send_image(chat_id):
    image_stream = generator.generate(queries[chat_id])
    bot.send_photo(chat_id, photo=image_stream)
    

cfg = read_config()
bot = telebot.TeleBot(cfg['token'])
generator = SdxlTurbo()


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_session(message):
    chat_id = message.chat.id
    queries[chat_id] = SdxlQuery(DEFAULT_MAIN_PROMPT)
    generate_and_send_image(message.chat.id)
    bot.send_message(chat_id, "Welcome to this student helper app for generating images!")
    bot.send_message(chat_id, "Main commands:\n" +
                     "/start - starts session and gives some helphul info\n" +
                     "/session_info - gives information about parameters of current session\n" +
                     "/set {main_prompt} - sets new main prompt for generating\n" +
                     "/add {tag} - adds new tag for generating\n" +
                     "/remove [optional]{tag} - removes written tag or the last (if command used without argument)\n" +
                     "/new_seed - generates new random number, to randomize images")

# Обработчик команды /set
@bot.message_handler(commands=['set'])
def set_main_prompt(message):
    set_prompt = ' '.join(message.text.split()[1:])
    chat_id = message.chat.id
    check_and_create_new_query_if_necessary(chat_id)
    queries[chat_id].main_prompt = set_prompt
    bot.send_message(chat_id, f'Main prompt was set to "{set_prompt}"')
    generate_and_send_image(chat_id)
    
# Обработчик команды /session_info
@bot.message_handler(commands=['session_info'])
def session_info(message):
    chat_id = message.chat.id
    check_and_create_new_query_if_necessary(chat_id)
    bot.send_message(chat_id, queries[chat_id].query_info())

# Обработчик команды /new_seed
@bot.message_handler(commands=['new_seed'])
def new_seed(message):
    chat_id = message.chat.id
    check_and_create_new_query_if_necessary(chat_id)
    queries[chat_id].new_seed()
    bot.send_message(chat_id, "Creating image with new seed...")
    generate_and_send_image(chat_id)

# Обработчик команды /add
@bot.message_handler(commands=['add'])
def add_tag(message):
    tag = ' '.join(message.text.split()[1:])
    chat_id = message.chat.id
    check_and_create_new_query_if_necessary(chat_id)

    
    queries[chat_id].add_tag(tag)
    bot.send_message(chat_id, "Creating image with new tags...")
    generate_and_send_image(chat_id)

# Обработчик команды /remove
@bot.message_handler(commands=['remove'])
def remove_tag(message):
    chat_id = message.chat.id
    check_and_create_new_query_if_necessary(chat_id)

    # Здесь проверяем задан ли аргумент у команды
    message_split = message.text.split()[1:]
    if len(message_split) == 0:
        is_removed = queries[chat_id].try_remove_last_tag()
    else:
        is_removed = queries[chat_id].try_remove_tag(' '.join(message_split))

    if not is_removed:
        bot.send_message(chat_id, "No tags or tag was not found")
        return
    
    bot.send_message(chat_id, "Tag removed. Generating new image...")
    generate_and_send_image(chat_id)


# Запуск бота для бесконечной обработки ввода в бот
bot.infinity_polling()

if __name__ == "__main__":
    pass