import os
import telebot

from sdxl_turbo import SdxlTurbo


def read_config():
    with open('src\\config.cfg', 'r') as cfg:
        cfg_lines = cfg.readlines()
        
        cfg_dict = {}
        for cfg_line in cfg_lines:
            cfg_line_split = cfg_line.split('=')
            cfg_dict[cfg_line_split[0]] = cfg_line_split[1]

        return cfg_dict




cfg = read_config()
bot = telebot.TeleBot(cfg['token'])
generator = SdxlTurbo()


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    image_stream = generator.generate(message.text)
    bot.send_photo(message.chat.id, photo=image_stream)



bot.infinity_polling()

if __name__ == "__main__":
    pass