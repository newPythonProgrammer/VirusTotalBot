import logging

import config
from bot import bot, dp, pyrogram_bot, scheduler
from aiogram.utils import executor
from database.token import Token
from database.proxy import Proxy
from database.client import User, Language
from database.chat import Chat
from virustotal.vt import VirusTotal
from handlers import admin
from handlers import client
import subprocess
import fake_useragent


User_agent = fake_useragent.UserAgent()
Token_db = Token()
Virus_total = VirusTotal()
Proxy_db = Proxy()
Chat_db = Chat()
Language_db = Language()
User_db = User()



async def update_stat_token():
    tokens = await Token_db.get_all_tokens()
    for token in tokens:
        stat = await Virus_total.get_stat_token(token)
        await Token_db.update_stat(token, stat['mouth'], stat['day'], stat['hour'])
async def reset_hour_quota_token():
    await Token_db.reset_hour_request()
    proxies = await Proxy_db.get_all_proxy()
    url = 'https://virustotal.com/ui/files/d0d6077e6e48ed221acfb0a22f5aeed8868d8339915ef93cfebbcbb2cb9f8362'

    headers = {
        "User-Agent": User_agent.random,
        "X-Tool": "vt-ui-main",
        "X-VT-Anti-Abuse-Header": await Virus_total.random_header_id(),
        "Accept-Ianguage": "en-US,en;q=0.9,es;q=0.8",
    }
    for proxy_id, proxy in proxies:
        check = await Virus_total.send_aio_get_request(url, proxy, headers)
        if check:
            await Proxy_db.active_proxy(proxy)
        else:
            await Proxy_db.disactive_proxy(proxy)

async def reset_day_quota_token():
    await Token_db.reset_day_request()

async def reset_mouth_quota_token():
    await Token_db.reset_mouth_request()
async def backup():
    users = await User_db.backup_users()
    text = ''
    for user_id, username, date, active in users:
        text += f'{user_id} | {username} | {date} | {active}\n'
    with open('users.txt', 'w', encoding='utf-8') as file:
        file.write(text)

    language = await Language_db.backup_language()
    text = ''
    for chat_id, lang in language:
        text += f'{chat_id} | {lang}\n'

    with open('language.txt', 'w') as file:
        file.write(text)

    chats = await Chat_db.backup_chat()
    text = ''
    for chat_id, title, members, username in chats:
        text += f'{chat_id} | {title} | {members} | {username}\n'

    with open('chats.txt', 'w') as file:
        file.write(text)

    for admin in config.ADMINS:
        try:
            await bot.send_document(admin, open('users.txt', 'rb'))
            await bot.send_document(admin, open('language.txt', 'rb'))
            await bot.send_document(admin, open('chats.txt', 'rb'))
        except:
            pass

async def del_files():
    logging.info('MAIN del_files')
    subprocess.run(["find",'files/' , "-type", "f", "-mmin", "+60", "-exec", "rm", "{}", ";"])
def schedule_job():
    scheduler.add_job(update_stat_token, 'interval', minutes=5)
    scheduler.add_job(reset_hour_quota_token, 'interval', hours=1)
    scheduler.add_job(reset_day_quota_token, 'cron', hour=2, minute=1)
    scheduler.add_job(reset_mouth_quota_token, 'cron', day=1, hour=2, minute=1)
    scheduler.add_job(backup, 'cron', day_of_week='fri', hour=12)
    scheduler.add_job(del_files, 'interval', minutes=1)
async def main(_):#Функция выполняется при запуске
    schedule_job()
    try:
        await bot.send_message(5344024150, 'Бот запущен!')
    except:
        pass

pyrogram_bot.start()
scheduler.start()
executor.start_polling(dp, on_startup=main, skip_updates=True)


