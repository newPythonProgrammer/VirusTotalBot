
from aiogram.types import Message, CallbackQuery, ChatActions
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
import config
from database.client import User, Language
from database.chat import Chat
from database.token import Token
from database.scan import Scan
from text_function import form_text
from bot import bot, dp, pyrogram_bot
from keyboard import keyboard
from virustotal.vt import VirusTotal
import subprocess
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
import logging


User_db = User()
Language_db = Language()
Token_db = Token()
Chat_db = Chat()
Virus_total = VirusTotal()
Scan_db = Scan()

scheduler = AsyncIOScheduler()
logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')
LAST_MSG_DICT = {}


class UserBannedMiddleware(BaseMiddleware):
    global LAST_MSG_DICT
    async def on_process_message(self, message: Message, data: dict):
        chat_id = message.chat.id
        if message.chat.type == 'supergroup':
            check = await Chat_db.check_chat(chat_id)
            if not check:
                chat = await message.bot.get_chat(chat_id)
                chat_title = chat.title
                username = chat.username
                count_chat_members = await chat.get_member_count()
                await Chat_db.add_chat(chat_id, chat_title, count_chat_members, f'@{username}')

            settings_chat = await Chat_db.get_settings_chat(chat_id)

            if (message.content_type == 'document') and not settings_chat['file_status']:
                raise CancelHandler
            if message.content_type=='text':
                if form_text.find_domain(message.text) and not settings_chat['domain_status']:
                    raise CancelHandler
                if form_text.find_ip_address(message.text) and not settings_chat['ip_status']:
                    raise CancelHandler
            return


        if message.chat.type == 'private' and message.content_type=='text':
            return
        chat = LAST_MSG_DICT.get(chat_id)
        if chat == None:
            LAST_MSG_DICT[chat_id] = datetime.datetime.now()
            return
        if (datetime.datetime.now() - LAST_MSG_DICT[chat_id]).seconds < 240:
            lang = await Language_db.get_lang(message.chat.id)
            await message.answer(config.TEXTS['flood'][lang], parse_mode='HTML')
            raise CancelHandler


dp.middleware.setup(UserBannedMiddleware())


@dp.message_handler(commands='start', state='*')
async def start(message: Message, state: FSMContext):
    await state.finish()
    chat_id = message.chat.id
    await Language_db.add_language(chat_id, 'none')
    lang = await Language_db.get_lang(chat_id)
    username = message.from_user.username

    if message.chat.type == 'supergroup':
        if lang == 'none':
            await message.answer('Choice language', reply_markup=keyboard.select_lang())
            return
        chat = await message.bot.get_chat(chat_id)
        chat_title = chat.title
        username = chat.username
        count_chat_members = await chat.get_member_count()
        check = await Chat_db.check_chat(chat_id)
        if not check:
            await Chat_db.add_chat(chat_id, chat_title, count_chat_members, f'@{username}')
        else:
            await Chat_db.edit_member(chat_id, count_chat_members)
        await message.answer(config.TEXTS['start'][lang], reply_markup=keyboard.main_menu_chat(lang), parse_mode='HTML',
                             disable_web_page_preview=True)



    if message.chat.type == 'private':
        if lang == 'none':
            await User_db.add_user(chat_id, str(username))
            await message.answer('Choice language', reply_markup=keyboard.select_lang())
            return
        await User_db.add_user(chat_id, str(username))
        await message.answer(config.TEXTS['start'][lang], reply_markup=keyboard.main_menu(lang), parse_mode='HTML', disable_web_page_preview=True)


@dp.callback_query_handler(lambda call: call.data == 'main_menu')
async def main_menu(call: CallbackQuery):
    await call.answer()
    chat_id = call.message.chat.id
    lang = await Language_db.get_lang(chat_id)
    if call.message.chat.type == 'supergroup':
        await call.bot.edit_message_text(config.TEXTS['start'][lang], chat_id, call.message.message_id,
                                     reply_markup=keyboard.main_menu_chat(lang), parse_mode='HTML')
        return
    await call.bot.edit_message_text(config.TEXTS['start'][lang], chat_id, call.message.message_id,
                                     reply_markup=keyboard.main_menu(lang), parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data in ('ru', 'eng', 'ukr', 'deut', 'esp', 'fren', 'ital'))
async def choice_language(call: CallbackQuery):
    await call.answer()
    lang = call.data
    chat_id = call.message.chat.id
    await Language_db.update_lang(chat_id, lang)
    if call.message.chat.type == 'supergroup':
        await call.bot.edit_message_text(config.TEXTS['start'][lang], chat_id, call.message.message_id,
                                         reply_markup=keyboard.main_menu_chat(lang), parse_mode='HTML', disable_web_page_preview=True)
        return
    await call.bot.edit_message_text(config.TEXTS['start'][lang], chat_id, call.message.message_id,
                                     reply_markup=keyboard.main_menu(lang), parse_mode='HTML', disable_web_page_preview=True)


@dp.callback_query_handler(lambda call: call.data == 'choice_lang')
async def update_lang(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    if call.message.chat.type == 'supergroup':
        chat = await call.bot.get_chat(chat_id)
        admins = await chat.get_administrators()
        admins_id = [admin.user.id for admin in admins]
        if user_id not in admins_id:
            await call.answer('You are not an administrator!')
            return
    await call.bot.edit_message_text('Choice language', chat_id, call.message.message_id,
                                     reply_markup=keyboard.select_lang())


@dp.callback_query_handler(lambda call: call.data == 'info')
async def information(call: CallbackQuery):
    await call.answer()
    chat_id = call.message.chat.id
    lang = await Language_db.get_lang(chat_id)
    await call.bot.edit_message_text(config.TEXTS['info'][lang], chat_id, call.message.message_id,
                                     reply_markup=keyboard.back_btn(lang), parse_mode='HTML',
                                     disable_web_page_preview=True)


@dp.message_handler(commands='info')
async def information(message: Message):
    chat_id = message.chat.id
    lang = await Language_db.get_lang(chat_id)
    await message.answer(config.TEXTS['info'][lang], reply_markup=keyboard.back_btn(lang),
                         disable_web_page_preview=True,
                         parse_mode='HTML')


async def progress(current, total, message: Message, lang):
    if round(current * 100 / total, 0) % 5 == 0:
        try:
            await message.edit_text(
                f'<i>{config.TEXTS["scan_file_texts"]["download_file"][lang]} {round(current * 100 / total, 1)}%</i>',
                parse_mode='HTML')
        except:
            pass


DICT_FILE_SCAN = {}


@dp.message_handler(lambda message: message.chat.type == 'private', content_types=['document', 'audio'], state='*')
async def scan_files(message: Message):
    global LAST_MSG_DICT
    chat_id = message.chat.id
    LAST_MSG_DICT[chat_id] = datetime.datetime.now()
    lang = await Language_db.get_lang(chat_id)
    file_type = message.content_type
    if file_type == 'document':
        file_download = message.document
    else:
        file_download = message.audio

    file_size = file_download.file_size
    if file_size >= 681574400:
        await message.reply(config.TEXTS['big_file'][lang])
        return
    edit_msg = await message.reply(f'<i>{config.TEXTS["scan_file_texts"]["download_file"][lang]} 0%</i>',
                                   parse_mode='HTML')
    file_name_download = f'files/{file_download.file_name}'
    file_name = file_download.file_name
    logging.info(f'CLIENT scan_files {file_name} {file_size}')
    try:
        await pyrogram_bot.download_media(file_download, file_name=file_name_download, progress=progress,
                                      progress_args=(edit_msg, lang)) # скачиваем файл
    except:
        await pyrogram_bot.download_media(file_download, file_name=file_name_download, progress=progress,
                                          progress_args=(edit_msg, lang))  # скачиваем файл

    await edit_msg.edit_text(config.TEXTS["scan_file_texts"]["download_completed"][lang])
    hash_file = await Virus_total.get_hash(file_name_download)  # хэш файла
    result = await Scan_db.get_result(hash_file)  # проверяем файл в нашей базе
    logging.info(f'CLIENT check hash {hash_file} in db')
    if result:
        logging.info(f'CLIENT check hash {hash_file} in db GOOD')
        await edit_msg.edit_text(f'{config.TEXTS["scan_file_texts"]["download_completed"][lang]}\n'
                                 f'{config.TEXTS["scan_file_texts"]["file_find"][lang]}')
        logging.info(f'CLIENT remove {file_name_download}')
        # os.remove(file_name_download)
        subprocess.run(['rm', file_name_download])
        subprocess.run(['rm', file_name_download.replace('.temp', '')])
        try:
            key = list(DICT_FILE_SCAN.keys())[-1]
        except IndexError:
            key = 0
        key = key + 1
        DICT_FILE_SCAN[key] = [hash_file, file_name]
        await edit_msg.edit_text(form_text.form_text(result, file_name, lang), parse_mode='HTML',
                                 reply_markup=keyboard.main_scan_btn(lang, key))
        return
    logging.info(f'CLIENT check hash {hash_file} in db BAD')
    result = await Virus_total.check_hash(hash_file)
    logging.info(f'CLIENT check hash {hash_file} in VT')
    if not result:
        logging.info(f'CLIENT check hash in VT BAD')
        await edit_msg.edit_text(f'{config.TEXTS["scan_file_texts"]["download_completed"][lang]}\n'
                                 f'<i>{config.TEXTS["scan_file_texts"]["load_virus_total"][lang]}</i>',
                                 parse_mode='HTML')
        if file_size <= 33554432:
            result = await Virus_total.scan_file(file_name_download, edit_msg, lang)
        else:
            result = await Virus_total.scan_big_file(file_name_download, edit_msg, lang)
        await edit_msg.edit_text(f'{config.TEXTS["scan_file_texts"]["download_completed"][lang]}\n'
                                 f'{config.TEXTS["scan_file_texts"]["load_virus_total_complited"][lang]}\n'
                                 f'{config.TEXTS["scan_file_texts"]["analiz_complited"][lang]}', parse_mode='HTML')
        result = await Virus_total.get_file(result['meta']['file_info']['sha256'])
    else:
        logging.info(f'CLIENT check hash {hash_file} in VT GOOD')
        await edit_msg.edit_text(f'{config.TEXTS["scan_file_texts"]["download_completed"][lang]}\n'
                                 f'{config.TEXTS["scan_file_texts"]["file_find"][lang]}')
    await Scan_db.add_scan(hash_file, result)
    logging.info(f'CLIENT remove {file_name_download}')
    # os.remove(file_name_download)
    subprocess.run(['rm', file_name_download])
    subprocess.run(['rm', file_name_download.replace('.temp', '')])
    try:
        key = list(DICT_FILE_SCAN.keys())[-1]
    except IndexError:
        key = 0
    key = key + 1
    DICT_FILE_SCAN[key] = [hash_file, file_name]
    await edit_msg.edit_text(form_text.form_text(result, file_name, lang), parse_mode='HTML',
                             reply_markup=keyboard.main_scan_btn(lang, key))


@dp.message_handler(lambda message: message.chat.type=='supergroup', content_types=['document', 'audio'], state='*')
async def scan_file(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = await Language_db.get_lang(chat_id)
    await message.reply(config.TEXTS['find_file'][lang], reply_markup=keyboard.scan_file(lang))

@dp.callback_query_handler(lambda call: call.data=='scan_chat_file', state='*')
async def scan_file(call: CallbackQuery, state: FSMContext):
    await call.answer()
    global LAST_MSG_DICT
    chat_id = call.message.chat.id
    LAST_MSG_DICT[chat_id] = datetime.datetime.now()
    lang = await Language_db.get_lang(chat_id)
    file_type = call.message.reply_to_message.content_type
    if file_type == 'document':
        file_download = call.message.reply_to_message.document
    else:
        file_download = call.message.reply_to_message.audio

    file_size = file_download.file_size
    if file_size >= 681574400:
        await call.message.edit_text(config.TEXTS['big_file'][lang])
        return
    edit_msg = await call.message.edit_text(f'<i>{config.TEXTS["scan_file_texts"]["download_file"][lang]} 0%</i>',
                                   parse_mode='HTML')
    file_name_download = f'files/{file_download.file_name}'
    file_name = file_download.file_name
    logging.info(f'CLIENT scan_files {file_name} {file_size}')
    await pyrogram_bot.download_media(file_download, file_name=file_name_download, progress=progress,
                                      progress_args=(edit_msg, lang))  # скачиваем файл
    await edit_msg.edit_text(config.TEXTS["scan_file_texts"]["download_completed"][lang])
    hash_file = await Virus_total.get_hash(file_name_download)  # хэш файла
    result = await Scan_db.get_result(hash_file)  # проверяем файл в нашей базе
    logging.info(f'CLIENT check hash {hash_file} in db')
    if result:
        logging.info(f'CLIENT check hash {hash_file} in db GOOD')
        await edit_msg.edit_text(f'{config.TEXTS["scan_file_texts"]["download_completed"][lang]}\n'
                                 f'{config.TEXTS["scan_file_texts"]["file_find"][lang]}')
        logging.info(f'CLIENT remove {file_name_download}')
        # os.remove(file_name_download)
        subprocess.run(['rm', file_name_download])
        subprocess.run(['rm', file_name_download.replace('.temp', '')])
        try:
            key = list(DICT_FILE_SCAN.keys())[-1]
        except IndexError:
            key = 0
        key = key + 1
        DICT_FILE_SCAN[key] = [hash_file, file_name]
        await edit_msg.edit_text(form_text.form_text(result, file_name, lang), parse_mode='HTML',
                                 reply_markup=keyboard.main_scan_btn(lang, key))
        return
    logging.info(f'CLIENT check hash {hash_file} in db BAD')
    result = await Virus_total.check_hash(hash_file)
    logging.info(f'CLIENT check hash {hash_file} in VT')
    if not result:
        logging.info(f'CLIENT check hash in VT BAD')
        await edit_msg.edit_text(f'{config.TEXTS["scan_file_texts"]["download_completed"][lang]}\n'
                                 f'<i>{config.TEXTS["scan_file_texts"]["load_virus_total"][lang]}</i>',
                                 parse_mode='HTML')
        if file_size <= 33554432:
            result = await Virus_total.scan_file(file_name_download, edit_msg, lang)
        else:
            result = await Virus_total.scan_big_file(file_name_download, edit_msg, lang)
        await edit_msg.edit_text(f'{config.TEXTS["scan_file_texts"]["download_completed"][lang]}\n'
                                 f'{config.TEXTS["scan_file_texts"]["load_virus_total_complited"][lang]}\n'
                                 f'{config.TEXTS["scan_file_texts"]["analiz_complited"][lang]}', parse_mode='HTML')
        result = await Virus_total.get_file(result['meta']['file_info']['sha256'])
    else:
        logging.info(f'CLIENT check hash {hash_file} in VT GOOD')
        await edit_msg.edit_text(f'{config.TEXTS["scan_file_texts"]["download_completed"][lang]}\n'
                                 f'{config.TEXTS["scan_file_texts"]["file_find"][lang]}')
    await Scan_db.add_scan(hash_file, result)
    logging.info(f'CLIENT remove {file_name_download}')
    # os.remove(file_name_download)
    subprocess.run(['rm', file_name_download])
    subprocess.run(['rm', file_name_download.replace('.temp', '')])
    try:
        key = list(DICT_FILE_SCAN.keys())[-1]
    except IndexError:
        key = 0
    key = key + 1
    DICT_FILE_SCAN[key] = [hash_file, file_name]
    await edit_msg.edit_text(form_text.form_text(result, file_name, lang), parse_mode='HTML',
                             reply_markup=keyboard.main_scan_btn(lang, key))




@dp.callback_query_handler(lambda call: call.data.startswith('detection_'))
async def show_detection(call: CallbackQuery):
    global DICT_FILE_SCAN
    await call.answer()
    chat_id = call.message.chat.id
    lang = await Language_db.get_lang(chat_id)
    scan_id = int(call.data.split('_')[1])
    scan_hash = DICT_FILE_SCAN[scan_id][0]
    result = await Virus_total.get_file(scan_hash)
    detection_text = form_text.form_text_antivirus(result, lang)
    await call.message.edit_text(detection_text, reply_markup=keyboard.back_scan_manu(lang, scan_id), parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data.startswith('signature_'))
async def show_signature(call: CallbackQuery):
    chat_id = call.message.chat.id
    lang = await Language_db.get_lang(chat_id)
    scan_id = int(call.data.split('_')[1])
    scan_hash = DICT_FILE_SCAN[scan_id][0]
    result = await Virus_total.get_file(scan_hash)
    bad_find = result['data']['attributes']['last_analysis_stats']['malicious']
    if bad_find == 0:
        await call.answer(config.TEXTS['no_signature'][lang])
    else:
        await call.answer()
        await call.message.edit_text(form_text.form_text_signature(result, lang),
                                     reply_markup=keyboard.back_scan_manu(lang, scan_id), parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data.startswith('back_file_'))
async def main_scan(call: CallbackQuery):
    await call.answer()
    chat_id = call.message.chat.id
    lang = await Language_db.get_lang(chat_id)
    scan_id = int(call.data.split('_')[-1])
    file_name = DICT_FILE_SCAN[scan_id][1]
    scan_hash = DICT_FILE_SCAN[scan_id][0]
    result = await Virus_total.get_file(scan_hash)
    result_text = form_text.form_text(result, file_name, lang)
    await call.message.edit_text(result_text, parse_mode='HTML', reply_markup=keyboard.main_scan_btn(lang, scan_id))


DICT_IP_ADDRESS = {}
DICT_IP_SCAN = {}


@dp.message_handler(
    regexp=r'\b(?:(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.){3}(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\b',
    state='*')
async def scan_ip_address(message: Message):
    global DICT_IP_ADDRESS
    global DICT_IP_ADDRESS
    lang = await Language_db.get_lang(message.chat.id)
    ip_address = form_text.find_ip_address(message.text)
    logging.info(f'CLIENT scan_ip_address {ip_address}')
    await message.answer_chat_action(ChatActions.TYPING)
    result = await Virus_total.scan_ip_address(ip_address)
    result_text = form_text.form_text_ip_address(result, lang)
    try:
        key = list(DICT_IP_ADDRESS.keys())[-1]
    except IndexError:
        key = 0
    key = key + 1
    DICT_IP_ADDRESS[key] = ip_address
    DICT_IP_SCAN[ip_address] = result

    await message.reply(result_text, parse_mode='HTML', reply_markup=keyboard.main_scan_ip(lang, key),
                        disable_web_page_preview=True)


@dp.callback_query_handler(lambda call: call.data.startswith('ip_detection_'))
async def detection_ip(call: CallbackQuery):
    await call.answer()
    scan_id = int(call.data.split('_')[-1])
    lang = await Language_db.get_lang(call.message.chat.id)
    domain = DICT_IP_ADDRESS[scan_id]
    result = DICT_IP_SCAN[domain]
    result_text = form_text.form_text_antivirus(result, lang)
    await call.message.edit_text(result_text, reply_markup=keyboard.back_ip_address(lang, scan_id),
                                 disable_web_page_preview=True, parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data.startswith('ip_signature_'))
async def signature_ip(call: CallbackQuery):
    scan_id = int(call.data.split('_')[-1])
    lang = await Language_db.get_lang(call.message.chat.id)
    domain = DICT_IP_ADDRESS[scan_id]
    result = DICT_IP_SCAN[domain]
    bad_find = result['data']['attributes']['last_analysis_stats']['malicious']
    if bad_find == 0:
        await call.answer(config.TEXTS['no_signature'][lang])
    else:
        await call.answer()
        result_text = form_text.form_text_signature(result, lang)
        await call.message.edit_text(result_text,
                                     reply_markup=keyboard.back_ip_address(lang, scan_id), parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data.startswith('ip_whois_'))
async def whois_ip_addres(call: CallbackQuery):
    lang = await Language_db.get_lang(call.message.chat.id)
    scan_id = int(call.data.split('_')[-1])
    ip_address = DICT_IP_ADDRESS[scan_id]
    result = DICT_IP_SCAN[ip_address]
    result_text = form_text.form_whois(result, lang)
    if result_text:
        await call.message.edit_text(result_text, parse_mode='HTML', reply_markup=keyboard.back_ip_address(lang, scan_id),
                                 disable_web_page_preview=True)
        return
    await call.answer('Не удалось получить данные с WhoIs', show_alert=True)

@dp.callback_query_handler(lambda call: call.data.startswith('back_ip_'))
async def back_ip_address(call: CallbackQuery):
    lang = await Language_db.get_lang(call.message.chat.id)
    scan_id = int(call.data.split('_')[-1])
    ip_address = DICT_IP_ADDRESS[scan_id]
    result = DICT_IP_SCAN[ip_address]
    result_text = form_text.form_text_ip_address(result, lang)
    await call.message.edit_text(result_text, parse_mode='HTML', reply_markup=keyboard.main_scan_ip(lang, scan_id),
                                 disable_web_page_preview=True)


DICT_DOMAIN_ADDRESS = {}
DICT_DOMAIN_SCAN = {}


@dp.message_handler(
    regexp=r'(?:(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}|(?<=\bgui/domain/)[a-zA-Z0-9-]+\.[a-zA-Z]{2,})',
    state='*')
async def scan_domain(message: Message):
    global DICT_DOMAIN_ADDRESS
    global DICT_DOMAIN_SCAN
    lang = await Language_db.get_lang(message.chat.id)
    domain = form_text.find_domain(message.text)
    logging.info(f'CLIENT scan_domain {domain}')
    await message.answer_chat_action(ChatActions.TYPING)
    result = await Virus_total.scan_domain(domain)
    result_text = form_text.form_text_domain(result, lang)
    try:
        key = list(DICT_DOMAIN_ADDRESS.keys())[-1]
    except IndexError:
        key = 0
    key = key + 1
    DICT_DOMAIN_ADDRESS[key] = domain
    DICT_DOMAIN_SCAN[domain] = result
    if result_text != 'not_found':
        await message.answer(result_text, parse_mode='HTML', reply_markup=keyboard.main_scan_domain(lang, key),
                             disable_web_page_preview=True)
        return
    await message.answer('Virustotal еще не анализировал данный домен, попробуйте через пару минут.', parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data.startswith('domain_detection'))
async def detection_domain(call: CallbackQuery):
    await call.answer()
    scan_id = int(call.data.split('_')[-1])
    lang = await Language_db.get_lang(call.message.chat.id)
    domain = DICT_DOMAIN_ADDRESS[scan_id]
    result = DICT_DOMAIN_SCAN[domain]
    result_text = form_text.form_text_antivirus(result, lang)
    await call.message.edit_text(result_text, reply_markup=keyboard.back_domain(lang, scan_id),
                                 disable_web_page_preview=True, parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data.startswith('domain_signature_'))
async def signature_domain(call: CallbackQuery):
    scan_id = int(call.data.split('_')[-1])
    lang = await Language_db.get_lang(call.message.chat.id)
    domain = DICT_DOMAIN_ADDRESS[scan_id]
    result = DICT_DOMAIN_SCAN[domain]
    bad_find = result['data']['attributes']['last_analysis_stats']['malicious']
    if bad_find == 0:
        await call.answer(config.TEXTS['no_signature'][lang])
    else:
        await call.answer()
        result_text = form_text.form_text_signature(result, lang)
        await call.message.edit_text(result_text,
                                     reply_markup=keyboard.back_domain(lang, scan_id), parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data.startswith('domain_whois_'))
async def whois_domain(call: CallbackQuery):
    await call.answer()
    scan_id = int(call.data.split('_')[-1])
    lang = await Language_db.get_lang(call.message.chat.id)
    domain = DICT_DOMAIN_ADDRESS[scan_id]
    result = DICT_DOMAIN_SCAN[domain]
    result_text = form_text.form_whois(result, lang)
    if result_text:
        await call.message.edit_text(result_text, parse_mode='HTML', reply_markup=keyboard.back_domain(lang, scan_id),
                                 disable_web_page_preview=True)
        return
    await call.answer('Не удалось получить данные с WhoIs', show_alert=True)

@dp.callback_query_handler(lambda call: call.data.startswith('back_domain_'))
async def back_domain(call: CallbackQuery):
    await call.answer()
    scan_id = int(call.data.split('_')[-1])
    lang = await Language_db.get_lang(call.message.chat.id)
    domain = DICT_DOMAIN_ADDRESS[scan_id]
    result = DICT_DOMAIN_SCAN[domain]
    result_text = form_text.form_text_domain(result, lang)
    await call.message.edit_text(result_text, parse_mode='HTML', reply_markup=keyboard.main_scan_domain(lang, scan_id),
                                 disable_web_page_preview=True)


@dp.callback_query_handler(lambda call: call.data == 'close')
async def close_scan(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    if call.message.chat.type == 'supergroup':
        chat = await call.bot.get_chat(chat_id)
        admins = await chat.get_administrators()
        admins_id = [admin.user.id for admin in admins]
        if user_id not in admins_id:
            await call.answer('You are not an administrator!')
            return
    await call.message.delete()


@dp.callback_query_handler(lambda call: call.data == 'settings')
async def get_settings_chat(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    lang = await Language_db.get_lang(chat_id)
    chat = await call.bot.get_chat(chat_id)
    admins = await chat.get_administrators()
    admins_id = [admin.user.id for admin in admins]
    if user_id not in admins_id:
        await call.answer('You are not an administrator!')
        return
    settings_chat = await Chat_db.get_settings_chat(chat_id)
    await call.message.edit_text(config.TEXTS['settings'][lang], reply_markup=keyboard.settings_scan(lang, settings_chat))


@dp.callback_query_handler(lambda call: call.data == 'set_file')
async def set_file_setting(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    lang = await Language_db.get_lang(chat_id)
    chat = await call.bot.get_chat(chat_id)
    admins = await chat.get_administrators()
    admins_id = [admin.user.id for admin in admins]
    if user_id not in admins_id:
        await call.answer('You are not an administrator!')
        return
    await Chat_db.set_file_setting(chat_id)
    settings_chat = await Chat_db.get_settings_chat(chat_id)
    await call.message.edit_reply_markup(keyboard.settings_scan(lang, settings_chat))

@dp.callback_query_handler(lambda call: call.data == 'del_file')
async def del_file_setting(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    lang = await Language_db.get_lang(chat_id)
    chat = await call.bot.get_chat(chat_id)
    admins = await chat.get_administrators()
    admins_id = [admin.user.id for admin in admins]
    if user_id not in admins_id:
        await call.answer('You are not an administrator!')
        return
    await Chat_db.del_file_setting(chat_id)
    settings_chat = await Chat_db.get_settings_chat(chat_id)
    await call.message.edit_reply_markup(keyboard.settings_scan(lang, settings_chat))

@dp.callback_query_handler(lambda call: call.data == 'set_domain')
async def set_file_setting(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    lang = await Language_db.get_lang(chat_id)
    chat = await call.bot.get_chat(chat_id)
    admins = await chat.get_administrators()
    admins_id = [admin.user.id for admin in admins]
    if user_id not in admins_id:
        await call.answer('You are not an administrator!')
        return
    await Chat_db.set_domain_setting(chat_id)
    settings_chat = await Chat_db.get_settings_chat(chat_id)
    await call.message.edit_reply_markup(keyboard.settings_scan(lang, settings_chat))

@dp.callback_query_handler(lambda call: call.data == 'del_domain')
async def del_file_setting(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    lang = await Language_db.get_lang(chat_id)
    chat = await call.bot.get_chat(chat_id)
    admins = await chat.get_administrators()
    admins_id = [admin.user.id for admin in admins]
    if user_id not in admins_id:
        await call.answer('You are not an administrator!')
        return
    await Chat_db.del_domain_setting(chat_id)
    settings_chat = await Chat_db.get_settings_chat(chat_id)
    await call.message.edit_reply_markup(keyboard.settings_scan(lang, settings_chat))


@dp.callback_query_handler(lambda call: call.data == 'set_ip_address')
async def set_file_setting(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    lang = await Language_db.get_lang(chat_id)
    chat = await call.bot.get_chat(chat_id)
    admins = await chat.get_administrators()
    admins_id = [admin.user.id for admin in admins]
    if user_id not in admins_id:
        await call.answer('You are not an administrator!')
        return
    await Chat_db.set_ip_setting(chat_id)
    settings_chat = await Chat_db.get_settings_chat(chat_id)
    await call.message.edit_reply_markup(keyboard.settings_scan(lang, settings_chat))


@dp.callback_query_handler(lambda call: call.data == 'del_ip_address')
async def del_file_setting(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    lang = await Language_db.get_lang(chat_id)
    chat = await call.bot.get_chat(chat_id)
    admins = await chat.get_administrators()
    admins_id = [admin.user.id for admin in admins]
    if user_id not in admins_id:
        await call.answer('You are not an administrator!')
        return
    await Chat_db.del_ip_setting(chat_id)
    settings_chat = await Chat_db.get_settings_chat(chat_id)
    await call.message.edit_reply_markup(keyboard.settings_scan(lang, settings_chat))