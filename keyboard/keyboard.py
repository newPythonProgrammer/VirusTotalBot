from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup
import config
from bot import username
def admin_panel():
    menu = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text='Рассылка по всем юзерам', callback_data='spam')
    btn2 = InlineKeyboardButton(text='Добавить токен', callback_data='add_token')
    btn3 = InlineKeyboardButton(text='Удалить токен', callback_data='del_token')
    btn4 = InlineKeyboardButton(text='Получить все токены', callback_data='get_tokens')
    btn5 = InlineKeyboardButton(text='Добавить прокси', callback_data='add_proxy')
    btn6 = InlineKeyboardButton(text='Получить все прокси', callback_data='get_proxy')
    btn7 = InlineKeyboardButton(text='Удалить прокси', callback_data='del_proxy')
    btn8 = InlineKeyboardButton(text='Получить все чаты', callback_data='get_all_chats')
    btn9 = InlineKeyboardButton(text='Назад', callback_data='main_menu')
    menu.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
    return menu


def select_lang():
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text='🇬🇧English', callback_data='eng')
    btn2 = InlineKeyboardButton(text='🇷🇺Русский', callback_data='ru')
    btn3 = InlineKeyboardButton(text='🇺🇦Український', callback_data='ukr')
    btn4 = InlineKeyboardButton(text='🇩🇪Deutsch', callback_data='deut')
    btn5 = InlineKeyboardButton(text='🇪🇸Español', callback_data='esp')
    btn6 = InlineKeyboardButton(text='🇫🇷Français', callback_data='fren')
    btn7 = InlineKeyboardButton(text='🇮🇹Italiano', callback_data='ital')
    menu.add(btn1)
    menu.add(btn2, btn3)
    menu.add(btn4, btn5)
    menu.add(btn6, btn7)
    return menu

def main_menu(lang):
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text=config.TEXTS['add_chat_btn'][lang], url=f'http://t.me/{username}?startgroup=true')
    btn2 = InlineKeyboardButton(text=config.TEXTS['lang_btn'][lang], callback_data='choice_lang')
    btn3 = InlineKeyboardButton(text=config.TEXTS['info_btn'][lang], callback_data='info')
    menu.add(btn1)
    menu.add(btn2, btn3)
    return menu

def main_menu_chat(lang):
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text=config.TEXTS['add_chat_btn'][lang], url=f'http://t.me/{username}?startgroup=true')
    btn2 = InlineKeyboardButton(text=config.TEXTS['lang_btn'][lang], callback_data='choice_lang')
    btn3 = InlineKeyboardButton(text=config.TEXTS['info_btn'][lang], callback_data='info')
    btn4 = InlineKeyboardButton(text=config.TEXTS['settings_btn'][lang], callback_data='settings')
    menu.add(btn1)
    menu.add(btn2, btn3)
    menu.add(btn4)
    return menu

def settings_scan(lang, data):
    menu = InlineKeyboardMarkup()


    btn1 = InlineKeyboardButton(text=config.TEXTS['settings_menu']['file'][lang], callback_data='set_file') if not data['file_status'] else InlineKeyboardButton(text=f"{config.TEXTS['settings_menu']['file'][lang]}✅", callback_data='del_file')
    btn2 = InlineKeyboardButton(text=config.TEXTS['settings_menu']['domain'][lang], callback_data='set_domain') if not data['domain_status'] else InlineKeyboardButton(text=f"{config.TEXTS['settings_menu']['domain'][lang]}✅", callback_data='del_domain')
    btn3 = InlineKeyboardButton(text=config.TEXTS['settings_menu']['ip_address'][lang], callback_data='set_ip_address') if not data['ip_status'] else InlineKeyboardButton(text=f"{config.TEXTS['settings_menu']['ip_address'][lang]}✅", callback_data='del_ip_address')
    btn4 = InlineKeyboardButton(text=config.TEXTS['back_btn'][lang], callback_data='main_menu')
    menu.add(btn1, btn2, btn3, btn4)
    return menu
def back_btn(lang):
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text=config.TEXTS['back_btn'][lang], callback_data='main_menu')
    menu.add(btn1)
    return menu

def main_scan_btn(lang, scan_id):
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text=config.TEXTS['scan_file_texts']['detection'][lang], callback_data=f'detection_{scan_id}')
    btn2 = InlineKeyboardButton(text=config.TEXTS['scan_file_texts']['signature'][lang], callback_data=f'signature_{scan_id}')
    btn3 = InlineKeyboardButton(text=config.TEXTS['scan_file_texts']['close'][lang], callback_data=f'close')
    menu.add(btn1, btn2)
    menu.add(btn3)
    return menu

def back_scan_manu(lang, scan_id):
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text=config.TEXTS['scan_file_texts']['back'][lang], callback_data=f'back_file_{scan_id}')
    menu.add(btn1)
    return menu


def main_scan_ip(lang, scan_id):
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text=config.TEXTS['scan_file_texts']['detection'][lang],
                                callback_data=f'ip_detection_{scan_id}')
    btn2 = InlineKeyboardButton(text=config.TEXTS['scan_file_texts']['signature'][lang],
                                callback_data=f'ip_signature_{scan_id}')

    btn3 = InlineKeyboardButton(text=config.TEXTS['whois_btn'][lang],
                                callback_data=f'ip_whois_{scan_id}')
    btn4 = InlineKeyboardButton(text=config.TEXTS['scan_file_texts']['close'][lang], callback_data=f'close')
    menu.add(btn1, btn2)
    menu.add(btn3)
    menu.add(btn4)
    return menu

def back_ip_address(lang, scan_id):
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text=config.TEXTS['scan_file_texts']['back'][lang],
                                callback_data=f'back_ip_{scan_id}')
    menu.add(btn1)
    return menu

def main_scan_domain(lang, scan_id):
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text=config.TEXTS['scan_file_texts']['detection'][lang],
                                callback_data=f'domain_detection_{scan_id}')
    btn2 = InlineKeyboardButton(text=config.TEXTS['scan_file_texts']['signature'][lang],
                                callback_data=f'domain_signature_{scan_id}')
    btn3 = InlineKeyboardButton(text=config.TEXTS['whois_btn'][lang],
                                callback_data=f'domain_whois_{scan_id}')
    btn4 = InlineKeyboardButton(text=config.TEXTS['scan_file_texts']['close'][lang], callback_data=f'close')
    menu.add(btn1, btn2)
    menu.add(btn3)
    menu.add(btn4)
    return menu

def back_domain(lang, scan_id):
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text=config.TEXTS['scan_file_texts']['back'][lang],
                                callback_data=f'back_domain_{scan_id}')
    menu.add(btn1)
    return menu

def scan_file(lang):
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text=config.TEXTS['find_file_btn'][lang], callback_data='scan_chat_file')
    menu.add(btn1)
    return menu
