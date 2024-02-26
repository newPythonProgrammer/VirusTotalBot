import datetime

import aiogram.utils.exceptions
import fake_useragent
from bot import bot, dp
from database.spam import Spam
from database.client import User, Language
from database.token import Token
from database.proxy import Proxy
from database.chat import Chat
from virustotal.vt import VirusTotal
import config
from states import states
from keyboard import keyboard

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import Message, CallbackQuery, ContentType, MediaGroup, InlineKeyboardButton, InlineKeyboardMarkup, ChatActions
from aiogram.dispatcher.middlewares import BaseMiddleware

import ast
from typing import List, Union
import asyncio
import aiohttp
import requests
import fake_useragent
Spam_db = Spam()
User_db = User()
Chat_db = Chat()
Language_db = Language()
Token_db = Token()
Proxy_db = Proxy()
VirusTotal = VirusTotal()
User_agent = fake_useragent.UserAgent()

class AlbumMiddleware(BaseMiddleware):
    """This middleware is for capturing media groups."""

    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        """
        You can provide custom latency to make sure
        albums are handled properly in highload.
        """
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: Message, data: dict):
        if not message.media_group_id:
            return

        try:
            self.album_data[message.media_group_id].append(message)
            raise CancelHandler()  # Tell aiogram to cancel handler for this group element
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            message.conf["is_last"] = True
            data["album"] = self.album_data[message.media_group_id]

    async def on_post_process_message(self, message: Message, result: dict, data: dict):
        """Clean up after handling our album."""
        if message.media_group_id and message.conf.get("is_last"):
            del self.album_data[message.media_group_id]


@dp.message_handler(lambda message: message.from_user.id in config.ADMINS, commands='panel', state='*')
async def show_panel(message: Message, state: FSMContext):
    await state.finish()
    text = f'{await User_db.stat_text()}\n' \
           f'{await Chat_db.get_chat_stat()}\n' \
           f'{await Language_db.stat_text()}\n' \
           f'{await Token_db.get_stat_text()}'
    await message.answer(text, reply_markup=keyboard.admin_panel())

@dp.callback_query_handler(lambda call: (call.from_user.id in config.ADMINS) and (call.data=='add_token'), state='*')
async def add_token(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    await call.message.answer('Пришли токен')
    await states.ADD_TOKEN.token.set()

@dp.message_handler(state=states.ADD_TOKEN.token)
async def add_token2(message: Message, state: FSMContext):
    check = await VirusTotal.check_token(message.text)
    if check != 'OK':
        await message.answer(f'Токен не работает {check}')
    else:
        await Token_db.add_token(message.text)
        await message.answer('Токен добавлен')
    await state.finish()

@dp.callback_query_handler(lambda call: (call.from_user.id in config.ADMINS) and (call.data=='get_tokens'))
async def get_all_tokens(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    tokens = await Token_db.get_all_tokens()
    text = ''
    count = 1
    for token in tokens:
        text += f'{count}) <code>{token}</code>\n'
        count += 1
    try:
        await call.message.answer(text, parse_mode='HTML')
    except aiogram.utils.exceptions.MessageTextIsEmpty:
        await call.message.answer('Токенов нету')
@dp.callback_query_handler(lambda call: (call.from_user.id in config.ADMINS) and (call.data=='del_token'))
async def del_token(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    await call.message.answer('Пришли токен который надо удалить')
    await states.DEL_TOKEN.token.set()

@dp.message_handler(state=states.DEL_TOKEN.token)
async def del_token2(message: Message, state: FSMContext):
    await Token_db.del_token(message.text)
    await message.answer('Токен удаляен')
    await state.finish()


@dp.callback_query_handler(lambda call: (call.data=='add_proxy') and (call.from_user.id in config.ADMINS), state='*')
async def add_proxy(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Пришли мне прокси в формате http://login:password@ip:port')
    await states.ADD_PROXY.proxy.set()

@dp.message_handler(state=states.ADD_PROXY.proxy)
async def add_proxy2(message: Message, state: FSMContext):
    proxy = message.text
    try:
        headers = {
            "User-Agent": User_agent.random,
            "X-Tool": "vt-ui-main",
            "X-VT-Anti-Abuse-Header": VirusTotal.random_header_id(),
            "Accept-Ianguage": "en-US,en;q=0.9,es;q=0.8",
        }
        responce_vt = await VirusTotal.send_aio_get_request('https://www.virustotal.com/ui/analyses/YmZmNmQxZTUzOWRjMzBhMzQ3YWRhYzkxZjAzNTZhYWU6MTcwNzQ5NDY2Mg==', proxy,
                                                         headers)
        response_ip_proxy = requests.get("https://api.ipify.org?format=json",
                                proxies={'https': message.text, 'http': message.text}, timeout=10)
        ip_proxy = response_ip_proxy.json()
        ip_proxy = ip_proxy['ip']
        response_ip = requests.get("https://api.ipify.org?format=json")
        ip_host = response_ip.json()
        ip_host = ip_host['ip']
        if responce_vt:
            await message.answer('Прокси действителен, добавлен')
            await Proxy_db.add_proxy(message.text)
            await state.finish()
        elif ip_proxy==ip_host and not responce_vt:
            await message.answer('Прокси добавлен, но возникла ошибка при синхронизации с VT')
            await Proxy_db.add_proxy(message.text)
            await Proxy_db.disactive_proxy(message.text)
            await state.finish()
        else:
            await message.answer('Прокси недействителен!')

    except:
        await message.answer('Прокси недействителен')

@dp.callback_query_handler(lambda call: (call.data=='get_proxy') and (call.from_user.id in config.ADMINS), state='*')
async def get_proxy(call: CallbackQuery, state: FSMContext):
    await call.answer('Проверяю все прокси, подожди')
    await call.message.answer_chat_action(ChatActions.TYPING)
    proxies = await Proxy_db.get_all_proxy()
    result_text = 'proxi_id - proxy - status\n\n'
    for proxy_id, proxy in proxies:
        text = ''
        proxy_status = await Proxy_db.get_status_proxy(proxy)
        proxy_status = '✅' if proxy_status else '❌'
        text += f'{proxy_id} - {proxy} - {proxy_status}\n'
        result_text += text

    await call.message.answer(result_text)


@dp.callback_query_handler(lambda call: (call.data=='del_proxy') and (call.from_user.id in config.ADMINS), state='*')
async def del_proxy(call: CallbackQuery,):
    await call.answer()
    await states.DEL_PROXY.proxy_id.set()
    await call.message.answer('Пришли мне proxy_id')

@dp.message_handler(state=states.DEL_PROXY.proxy_id)
async def del_proxy2(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Введи proxy_id!')
        return
    await Proxy_db.del_proxy(int(message.text))
    await message.answer('Прокси удален')
    await state.finish()

@dp.callback_query_handler(lambda call: (call.data=='get_all_chats') and (call.from_user.id in config.ADMINS), state='*')
async def get_all_chat(call: CallbackQuery):
    await call.answer()
    chats = await Chat_db.backup_chat()
    text = ''
    for chat_id, title, members, username in chats:
        text += f'{chat_id} | {title} | {members} | {username}\n'

    with open('chats.txt', 'w') as file:
        file.write(text)
    await bot.send_document(call.from_user.id, open('chats.txt', 'rb'))

@dp.callback_query_handler(lambda call: (call.data=='spam') and (call.from_user.id  in config.ADMINS), state='*')
async def spam1(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in config.ADMINS:
        await call.message.answer('Пришли пост')
        await states.FSM_ADMIN_SPAM.text.set()

@dp.message_handler(state=states.FSM_ADMIN_SPAM.text, is_media_group=True, content_types=ContentType.ANY,)
async def spam2_media_group(message: Message, album: List[Message], state: FSMContext):
    """This handler will receive a complete album of any type."""
    media_group = MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            # We can also add a caption to each file by specifying `"caption": "text"`
            media_group.attach({"media": file_id, "type": obj.content_type, "caption": obj.caption,
                                "caption_entities": obj.caption_entities})
        except ValueError:
            return await message.answer("This type of album is not supported by aiogram.")
    media_group = ast.literal_eval(str(media_group))
    async with state.proxy() as data:
        try:
            data['text'] = media_group[0]['caption']
        except:
            data['text'] = 'None'
        data['media'] = media_group
        await Spam_db.add_spam(data['text'], 'None', str(media_group))
    last_id = await Spam_db.select_last_id()
    await message.answer_media_group(media_group)
    await message.answer(f'Пришли команду /sendspam_{last_id} чтоб начать рассылку')
    await state.finish()

@dp.message_handler(state=states.FSM_ADMIN_SPAM.text, content_types=['photo', 'video', 'animation', 'text'])
async def spam2(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        if message.content_type in ('photo', 'video', 'animation'):
            async with state.proxy() as data:
                try:
                    data['text'] = message.html_text
                except:
                    data['text'] = None
                if message.content_type == 'photo':
                    data['media'] = ('photo', message.photo[-1].file_id)
                else:
                    data['media'] = (message.content_type, message[message.content_type].file_id)
        else:
            async with state.proxy() as data:
                data['text'] = message.html_text
                data['media'] = 'None'
        await message.answer('Теперь пришли кнопки например\n'
                             'text - url1\n'
                             'text2 - url2 && text3 - url3\n\n'
                             'text - надпись кнопки url - ссылка'
                             '"-" - разделитель\n'
                             '"&&" - склеить в строку\n'
                             'ЕСЛИ НЕ НУЖНЫ КНОПКИ ОТПРАВЬ 0')
        await states.FSM_ADMIN_SPAM.next()

@dp.message_handler(state=states.FSM_ADMIN_SPAM.btns)
async def spam3(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        if message.text != '0':
            # конструктор кнопок
            try:
                buttons = []
                for char in message.text.split('\n'):
                    if '&&' in char:
                        tmpl = []
                        for i in char.split('&&'):
                            tmpl.append(dict([i.split('-', maxsplit=1)]))
                        buttons.append(tmpl)
                    else:
                        buttons.append(dict([char.split('-', maxsplit=1)]))
                menu = InlineKeyboardMarkup()
                btns_list = []
                items = []
                for row in buttons:
                    if type(row) == dict:
                        url1 = str(list(row.items())[0][1]).strip()
                        text1 = list(row.items())[0][0]
                        menu.add(InlineKeyboardButton(text=text1, url=url1))
                    else:
                        items.clear()
                        btns_list.clear()
                        for d in row:
                            items.append(list(d.items())[0])
                        for text, url in items:
                            url = url.strip()
                            btns_list.append(InlineKeyboardButton(text=text, url=url))
                        menu.add(*btns_list)
                ###########$##############
                async with state.proxy() as data:
                    data['btns'] = str(menu)
                    media = data['media']
                    text = data['text']
                    await Spam_db.add_spam(text, str(menu), str(media))

                    if media != 'None':
                        content_type = media[0]
                        if content_type == 'photo':
                            await message.bot.send_photo(user_id, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=menu)
                        elif content_type == 'video':
                            await message.bot.send_video(user_id, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=menu)
                        elif content_type == 'animation':
                            await message.bot.send_animation(user_id, media[1], caption=text, parse_mode='HTML',
                                                             reply_markup=menu)
                    else:
                        await message.answer(text, reply_markup=menu, parse_mode='HTML', disable_web_page_preview=True)

            except Exception as e:
                await message.reply(f'Похоже что непрвильно введена клавиатура')
        else:
            async with state.proxy() as data:
                data['btns'] = 'None'
                media = data['media']
                text = data['text']
                await Spam_db.add_spam(text, 'None', str(media))


                if media != 'None':
                    content_type = media[0]
                    if content_type == 'photo':
                        await message.bot.send_photo(user_id, media[1], caption=text, parse_mode='HTML')
                    elif content_type == 'video':
                        await message.bot.send_video(user_id, media[1], caption=text, parse_mode='HTML')
                    elif content_type == 'animation':
                        await message.bot.send_animation(user_id, media[1], caption=text, parse_mode='HTML')
                else:
                    await message.answer(text, parse_mode='HTML', disable_web_page_preview=True)
        last_id = await Spam_db.select_last_id()
        await message.answer(f'Пришли команду /sendspam_{last_id} чтоб начать рассылку')
        await state.finish()

@dp.message_handler(lambda message: (message.from_user.id in config.ADMINS) and (message.text.startswith('/sendspam')))
async def start_spam(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        spam_id = int(message.text.replace('/sendspam_', ''))
        text = await Spam_db.select_text(spam_id)
        keyboard = await Spam_db.select_keyboard(spam_id)
        media = await Spam_db.select_media(spam_id)
        if text == 'None':
            text = None
        if keyboard == 'None':
            keyboard = None
        all_user = await User_db.get_all_user()
        await message.answer(f'Считанно {len(all_user)} пользователей запускаю рассылку')
        no_send = 0
        send = 0
        for user in all_user:
            user = int(user)
            try:
                if media != 'None' and media != None:  # Есть медиа
                    if type(media) is list:
                        await message.bot.send_media_group(user, media)
                    else:
                        content_type = media[0]

                        if content_type == 'photo':
                            await message.bot.send_photo(user, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=keyboard)
                        elif content_type == 'video':
                            await message.bot.send_video(user, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=keyboard)
                        elif content_type == 'animation':
                            await message.bot.send_animation(user, media[1], caption=text, parse_mode='HTML',
                                                             reply_markup=keyboard)

                else:  # Нету медиа
                    if keyboard != 'None' and keyboard != None:  # Есть кнопки
                        await message.bot.send_message(chat_id=user, text=text, reply_markup=keyboard,
                                                       parse_mode='HTML', disable_web_page_preview=True)
                    else:
                        await message.bot.send_message(chat_id=user, text=text, parse_mode='HTML',
                                                       disable_web_page_preview=True)
                send += 1

            except:
                no_send += 1
        await message.answer(f'Рассылка окончена.\n'
                             f'Отправленно: {send} пользователям\n'
                             f'Не отправленно: {no_send} пользователям')


dp.middleware.setup(AlbumMiddleware())