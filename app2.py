from bs4 import BeautifulSoup
import requests
import logging
import os
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.emoji import emojize

with open("parser2.txt") as file:
    array = [row.strip() for row in file]

API_TOKEN = '1666903357:AAEhDQ9L04D6NCr6qwhKyss1zy69NZvTbr0'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
site = 'http://samotlor.tv'


def urlTake(site):
    i = random.randint(18,52)
    url = site + array[i]
    return(url)

def parse(url):
    print(url)
    new_news = []
    news = []
    news_item = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    news = soup.findAll('div', class_="sppb-addon-content")
    new_news.append(url)
    for news_item in news:
        if news_item.find('p') is not None:
            new_news.append(news_item.text)
    return new_news


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Показать", "Полная версия"]
    keyboard.add(*buttons)
    await message.reply(f"\n".join(parse(urlTake(site))))
    await message.answer("Показать следующую новость?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Показать"))
async def with_puree(message: types.Message):
    await message.reply(f"\n".join(parse(urlTake(site))))
    
    
@dp.message_handler(Text(equals="Полная версия"))
async def cmd_inline_url(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Samotlor.tv", url="https://samotlor.tv"),
        types.InlineKeyboardButton(text="Vkontakte", url="https://vk.com/samotlor_tv")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer(emojize('Вы знаете, что с этим делать :astonished:'), reply_markup=keyboard)
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
