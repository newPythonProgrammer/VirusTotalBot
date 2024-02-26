import asyncio
import hashlib
from typing import Union
import aiohttp
import requests
import logging
import config
from database.proxy import Proxy
from database.token import Token
from bot import bot
import random
import string
import fake_useragent

User_agent = fake_useragent.UserAgent()
Token_db = Token()
Proxy_db = Proxy()
logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


class VirusTotal:
    def random_header_id(self):
        return ("".join(random.choice(string.ascii_letters) for _ in range(59))) + "=="

    async def send_aio_get_request(self, url, proxy, headers, recursion_count=0):
        if recursion_count >= 5:
            return False
        logging.info(f'get_request {proxy} {url}')
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(url, headers=headers, proxy=proxy, timeout=10)
                json_data = await response.json()
                await session.close()
                if 'error' in json_data and json_data["error"]["code"] == "Quota exceeded":
                    proxy = await Proxy_db.get_random_proxy()
                    response = await session.get(url, headers=headers, proxy=proxy, timeout=10)
                    json_data = await response.json()
                    if 'error' in json_data and json_data["error"]["code"] == "Quota exceeded":  # Если все равно ошибка
                        await Token_db.disactive_token(headers['x-apikey'])  # Ставим что токен не активный
                        await session.close()
                        return False
                    else:
                        await Proxy_db.disactive_proxy(proxy)
                        for admin in config.ADMINS:
                            try:
                                await bot.send_message(admin, f'Прокси {proxy} установлен не активный статус Quota exceeded')
                            except:
                                pass

                if 'error' in json_data and  json_data["error"]["code"] == "RecaptchaRequiredError":
                    logging.warning('get_request RecaptchaRequiredError')
                    return False
                if 'error' in json_data and json_data["error"]["code"] == 'UserNotActiveError':
                    logging.warning(f'get_request DEL TOKEN {headers["x-apikey"]}')
                    for admin in config.ADMINS:
                        try:
                            await bot.send_message(admin, f'Токен {headers["x-apikey"]} удален, по причине бана аккаунта')
                        except:
                            pass
                    await Token_db.del_token(headers["x-apikey"])
                    return None
                logging.info(f'return get_request {proxy} {url}')
                return response

        except (aiohttp.client.ClientProxyConnectionError, aiohttp.client.ClientConnectionError, aiohttp.client.ClientHttpProxyError):
            if recursion_count < 2:
                return await self.send_aio_get_request(proxy, url, headers, recursion_count + 1)
            await Proxy_db.disactive_proxy(proxy)
            logging.info(f'get_request ProxyError {proxy}')
            for admin in config.ADMINS:
                try:
                    await bot.send_message(admin, f'Прокси {proxy} отлетел ProxyError')
                except Exception as e:
                    print(e)
            return False
        except Exception as e:
            error = 'get_request Line: ' + str(e.__traceback__.tb_lineno) + ' Error: ' + str(e) + ' Type: ' + type(
                e).__name__
            print(e)
            logging.error(error)
            return False

    async def send_aio_post_request(self, url, api_key, file_name):
        headers = {"x-apikey": api_key}
        logging.info(f'post_request {api_key} {file_name}')
        try:
            async with aiohttp.ClientSession() as session:
                with open(file_name, 'rb') as file:
                    response = await session.post(url, headers=headers, data={'file': file})
                    json_data = await response.json()
                    check = json_data.get('error')
                    if check:
                        if check.get('message') == 'Quota exceeded':  # Если запрос пишет расходована квота
                            # Проверяем еще раз
                            responce_check = await session.post(url, headers=headers, data={'file': file})
                            json_data_check = await responce_check.json()
                            check_data = json_data_check.get('error')
                            if check_data:  # Если все равно ошибка
                                await Token_db.disactive_token(api_key)  # Ставим что токен не активный
                                await session.close()
                                return False
                        elif check.get('message') == 'User is banned':
                            for admin in config.ADMINS:
                                try:
                                    await bot.send_message(admin, f'Токен {api_key} удален, по причине бана акканута')
                                except:
                                    pass
                            await Token_db.del_token(api_key)
                            return False
                    await session.close()
                    logging.info(f'return post_request {api_key} {file_name}')
                    return response

        except Exception as e:
            error = 'post_request Line: ' + str(e.__traceback__.tb_lineno) + ' Error: ' + str(e) + ' Type: ' + type(
                e).__name__
            logging.error(error)
            return False

    async def get_hash(self, file_name) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_name, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                sha256_hash.update(chunk)
        hash = sha256_hash.hexdigest()
        return hash

    async def check_hash(self, hash) -> Union[dict, bool]:
        result = await self.get_file(hash)
        if 'error' not in result.keys():
            return result
        return False

    async def scan_file(self, file_name, message, lang) -> Union[dict, bool]:
        logging.info(f'scan_file {file_name}')
        api_url = "https://www.virustotal.com/api/v3/files"
        api_key = await Token_db.get_random_token()
        response = await self.send_aio_post_request(api_url, api_key, file_name)
        counter = 0
        while not response and counter < 10:
            api_key = await Token_db.get_random_token()
            response = await self.send_aio_post_request(api_url, api_key, file_name)
            counter += 1
        data = await response.json()
        await message.edit_text(f'{config.TEXTS["scan_file_texts"]["download_completed"][lang]}\n'
                                f'<i>{config.TEXTS["scan_file_texts"]["load_virus_total_complited"][lang]}</i>\n'
                                f'<i>{config.TEXTS["scan_file_texts"]["analiz_file"][lang]}</i>', parse_mode='HTML')
        result = await self._get_analyse(data['data']['id'])
        logging.info('end get_analyse')
        try:
            a = result['error']
            return False
        except:
            return result

    async def scan_big_file(self, file_name, message, lang) -> Union[dict, bool]:
        logging.info(f'scan_big_file {file_name}')
        api_url = "https://www.virustotal.com/api/v3/files/upload_url"
        proxy = await Proxy_db.get_random_proxy()
        api_key = await Token_db.get_random_token()
        headers = {"x-apikey": api_key}
        response = await self.send_aio_get_request(api_url, proxy, headers)
        counter = 0
        while not response and counter < 10:
            proxy = await Proxy_db.get_random_proxy()
            api_key = await Token_db.get_random_token()
            response = await self.send_aio_get_request(api_url, proxy, headers)
            counter += 1

        data = await response.json()
        url = data['data']
        response = await self.send_aio_post_request(url, api_key, file_name)
        counter = 0
        while not response and counter < 10:
            api_key = await Token_db.get_random_token()
            response = await self.send_aio_post_request(url, api_key, file_name)
            counter += 1
        data = await response.json()
        await message.edit_text(f'{config.TEXTS["scan_file_texts"]["download_completed"][lang]}\n'
                                f'<i>{config.TEXTS["scan_file_texts"]["load_virus_total_complited"][lang]}</i>\n'
                                f'<i>{config.TEXTS["scan_file_texts"]["analiz_file"][lang]}</i>', parse_mode='HTML')

        result = await self._get_analyse(data['data']['id'])
        logging.info('end get_analyse')
        try:
            a = result['error']
            return False
        except:
            return result

    async def _get_analyse(self, scan_id) -> Union[dict, bool]:
        logging.info('get_analyse')
        proxy = await Proxy_db.get_random_proxy()

        api_url = f"https://www.virustotal.com/ui/analyses/{scan_id}"
        headers = {
            "User-Agent": User_agent.random,
            "X-Tool": "vt-ui-main",
            "X-VT-Anti-Abuse-Header": self.random_header_id(),
            "Accept-Ianguage": "en-US,en;q=0.9,es;q=0.8",
        }
        response = await self.send_aio_get_request(api_url, proxy, headers)
        counter = 0
        while not response and counter < 10:
            headers = {
                "User-Agent": User_agent.random,
                "X-Tool": "vt-ui-main",
                "X-VT-Anti-Abuse-Header": self.random_header_id(),
                "Accept-Ianguage": "en-US,en;q=0.9,es;q=0.8",
            }
            proxy = await Proxy_db.get_random_proxy()
            response = await self.send_aio_get_request(api_url, proxy, headers)
            counter += 1
        response = await response.json()
        while response['data']['attributes']['results'] == {}:
            response = await self.send_aio_get_request(api_url, proxy, headers)
            response = await response.json()
            try:
                a = response['error']
                return False
            except KeyError:
                pass
            await asyncio.sleep(10)
        return response

    async def get_file(self, hash) -> dict:
        logging.info('get_file')
        proxy = await Proxy_db.get_random_proxy()
        api_url = f'https://www.virustotal.com/ui/files/{hash}'
        headers = {
            "User-Agent": User_agent.random,
            "X-Tool": "vt-ui-main",
            "X-VT-Anti-Abuse-Header": self.random_header_id(),
            "Accept-Ianguage": "en-US,en;q=0.9,es;q=0.8",
        }
        response = await self.send_aio_get_request(api_url, proxy, headers)

        counter = 0
        while not response and counter < 10:
            headers = {
                "User-Agent": User_agent.random,
                "X-Tool": "vt-ui-main",
                "X-VT-Anti-Abuse-Header": self.random_header_id(),
                "Accept-Ianguage": "en-US,en;q=0.9,es;q=0.8",
            }
            proxy = await Proxy_db.get_random_proxy()
            response = await self.send_aio_get_request(api_url, proxy, headers)
            counter += 1
        response = await response.json()
        logging.info('end get_file')
        return response

    async def check_token(self, token) -> str:
        logging.info(f'check_token {token}')
        api_url = "https://www.virustotal.com/api/v3/files/upload_url"
        headers = {"x-apikey": token}
        async with aiohttp.ClientSession() as session:
            response = await session.get(api_url, headers=headers)
        data = await response.json()
        try:
            check = data['error']
            return str(check)
        except:
            return 'OK'

    async def get_stat_token(self, api_key) -> dict:
        logging.info(f'get_stat_token {api_key}')
        proxy = await Proxy_db.get_random_proxy()
        api_url = f"https://www.virustotal.com/api/v3/users/{api_key}/overall_quotas"
        headers = {"x-apikey": api_key}
        response = await self.send_aio_get_request(api_url, proxy, headers)
        data = await response.json()

        counter = 0
        if response == None:
            return {'mouth': 0,
                    'day': 0,
                    'hour': 0}
        while not response and counter < 10:
            proxy = await Proxy_db.get_random_proxy()
            response = await self.send_aio_get_request(api_url, proxy, headers)
            counter += 1
        response = await response.json()
        hour_limit = response['data']['api_requests_hourly']['user']['used']
        day_limit = response['data']['api_requests_daily']['user']['used']
        mouth_limit = response['data']['api_requests_monthly']['user']['used']
        return {'mouth': mouth_limit,
                'day': day_limit,
                'hour': hour_limit}

    async def scan_ip_address(self, ip_address) -> dict:
        logging.info(f'scan_ip_address {ip_address}')
        proxy = await Proxy_db.get_random_proxy()
        api_url = f"https://www.virustotal.com/ui/ip_addresses/{ip_address}"
        headers = {
            "User-Agent": User_agent.random,
            "X-Tool": "vt-ui-main",
            "X-VT-Anti-Abuse-Header": self.random_header_id(),
            "Accept-Ianguage": "en-US,en;q=0.9,es;q=0.8",
        }
        response = await self.send_aio_get_request(api_url, proxy, headers)
        counter = 0
        while not response and counter < 10:
            headers = {
                "User-Agent": User_agent.random,
                "X-Tool": "vt-ui-main",
                "X-VT-Anti-Abuse-Header": self.random_header_id(),
                "Accept-Ianguage": "en-US,en;q=0.9,es;q=0.8",
            }
            proxy = await Proxy_db.get_random_proxy()
            response = await self.send_aio_get_request(api_url, proxy, headers)
            counter += 1
        response = await response.json()
        return response

    async def scan_domain(self, domain) -> dict:
        logging.info(f'domain {domain}')
        proxy = await Proxy_db.get_random_proxy()
        api_url = f'https://www.virustotal.com/ui/domains/{domain}'
        headers = {
            "User-Agent": User_agent.random,
            "X-Tool": "vt-ui-main",
            "X-VT-Anti-Abuse-Header": self.random_header_id(),
            "Accept-Ianguage": "en-US,en;q=0.9,es;q=0.8",
        }
        response = await self.send_aio_get_request(api_url, proxy, headers)
        counter = 0
        while not response and counter < 10:
            headers = {
                "User-Agent": User_agent.random,
                "X-Tool": "vt-ui-main",
                "X-VT-Anti-Abuse-Header": self.random_header_id(),
                "Accept-Ianguage": "en-US,en;q=0.9,es;q=0.8",
            }
            proxy = await Proxy_db.get_random_proxy()
            response = await self.send_aio_get_request(api_url, proxy, headers)
            counter += 1
        response = await response.json()
        return response
