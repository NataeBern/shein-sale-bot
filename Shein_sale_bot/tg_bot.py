from aiogram import Bot, Dispatcher, executor, types
from config import token_API, chanel_ID
from aiogram.dispatcher.filters import Text

from keyboards import kb
from main import check_inf_update
from stickers import stickers

import json
import random
import asyncio

bot = Bot(token=token_API)
dp = Dispatcher(bot)



async def on_startup(_):
    print('Бот был успешно запущен!')


@dp.message_handler(commands=['start'])
async def start_commands(message: types.Message) -> None:
    await message.delete()
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Приветствую тебя, <b>{message.from_user.first_name}</b>!\n\n'
                                f'Ты хочешь узнать о самых свежих товарах со скидкой? Я помогу тебе в этом!\n\n'
                                f'Нажимай на кнопку ниже и в течение нескольких минут мы будем оповещать тебя о всех найденных товарах. 😊',
                           reply_markup=kb,
                           parse_mode='HTML')


@dp.message_handler(Text(equals='Жми сюда!', ignore_case=True))
async def new_products_command(message: types.Message) -> None:
    await message.delete()
    fresh_inf_dict = check_inf_update()
    if len(fresh_inf_dict) >= 1:
        await message.answer('Нашли! Скоро мы тебе их покажем!')
        article_id, inf = random.choice(list(fresh_inf_dict.items()))
        await asyncio.sleep(random.randint(60, 180))
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=inf['img_inf'],
                             caption=f'<b>{random.choice(stickers)} {inf["name_inf"]}</b>\n\n'
                                     f'{inf["dis_prices_inf"]} | <s>{inf["prices_inf"]}</s> | {inf["discounts_inf"]}\n\n'
                                     f'<a href="{inf["link"]}">Ссылка на товар! 👈</a>\n\n\n'
                                     f'Если хочешь узнавать о свежайших новинках раньше всех - тогда напиши нашему <a href="https://t.me/Shein_sale_bot">Telegram-боту</a>!',
                             parse_mode='HTML')
    else:
        await message.answer('Прости, но пока нет свежих товаров со скидкой...')


@dp.message_handler(commands=['startinchanel'])
async def start_in_chanel_commands(message: types.Message) -> None:
    with open('inf_dict.json', 'r') as file:
        inf_dict = json.load(file)

        while True:
            article_id, inf = random.choice(list(inf_dict.items()))
            await asyncio.sleep(random.randint(1200, 1800))
            await bot.send_photo(chat_id=chanel_ID,
                                 photo=inf['img_inf'],
                                 caption=f'<b>{random.choice(stickers)} {inf["name_inf"]}</b>\n\n'
                                         f'{inf["dis_prices_inf"]} | <s>{inf["prices_inf"]}</s> | {inf["discounts_inf"]}\n\n'
                                         f'<a href="{inf["link"]}">Ссылка на товар! 👈</a>\n\n\n'
                                         f'Если хочешь узнавать о свежайших новинках раньше всех - тогда напиши нашему <a href="https://t.me/Shein_sale_bot">Telegram-боту</a>!',
                                 parse_mode='HTML')



if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           on_startup=on_startup)