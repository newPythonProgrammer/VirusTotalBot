import asyncio
import aiomysql
import config

'''
CREATE TABLE IF NOT EXISTS user(
Id DECIMAL(13, 0),
Username TEXT,
Date_join DATE,
Active BOOL);

CREATE TABLE IF NOT EXISTS language(
Id DECIMAL(17, 0),
Lang TEXT);

'''


class User:
    async def add_user(self, user_id, username):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT * FROM user WHERE Id = %s''', (user_id,))
        check = await cursor.fetchone()
        if not bool(check):
            await cursor.execute('''INSERT INTO user VALUES(%s, %s, CURRENT_DATE(), 1)''', (user_id, username))
            await connect.commit()
        connect.close()

    async def get_all_user(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT ID FROM user''')
        result = await cursor.fetchall()

        user_ids = [int(row[0]) for row in result]
        connect.close()
        return user_ids


    async def get_all_users(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Id FROM user''')
        users_list = await cursor.fetchall()
        users_list = [int(i[0]) for i in users_list]
        connect.close()
        return users_list

    async def set_active_user(self, user_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE user SET Active = 1 WHERE Id = %s''', (user_id,))
        await connect.commit()
        connect.close()

    async def set_disactive_user(self, user_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE user SET Active = 0 WHERE Id = %s''', (user_id,))
        await connect.commit()
        connect.close()

    async def stat_text(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT COUNT(Id) as count FROM user WHERE DATEDIFF(CURRENT_DATE(), Date_join)<=1''')
        day_users = await cursor.fetchone()
        await cursor.execute('''SELECT COUNT(Id) as count FROM user WHERE DATEDIFF(CURRENT_DATE(), Date_join)<=7''')
        week_users = await cursor.fetchone()
        await cursor.execute('''SELECT COUNT(Id) as count FROM user WHERE DATEDIFF(CURRENT_DATE(), Date_join)<=30''')
        moth_users = await cursor.fetchone()

        await cursor.execute('''SELECT COUNT(Id) as count FROM user''')
        all_users = await cursor.fetchone()
        await cursor.execute('''SELECT COUNT(Id) as count FROM user WHERE Active = 1''')
        active_users = await cursor.fetchone()
        await cursor.execute('''SELECT COUNT(Id) as count FROM user WHERE Active = 0''')
        disactive_users = await cursor.fetchone()
        return f'👥 Пользователи\n' \
               f'├ Всего: {all_users[0]}\n' \
               f'├ Живые: {active_users[0]}\n' \
               f'└ Мёртвые: {disactive_users[0]}\n\n' \
               f'📈 Динамика\n' \
               f'├ За день: +{day_users[0]}\n' \
               f'├ За неделю: +{week_users[0]}\n' \
               f'└ За месяц: +{moth_users[0]}\n'

    async def backup_users(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT * FROM user''')
        data = await cursor.fetchall()
        connect.close()
        return data

class Language:
    async def add_language(self, chat_id, language):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT * FROM language WHERE Id = %s''', (chat_id,))
        check = await cursor.fetchone()
        if not check:
            await cursor.execute('''INSERT INTO language VALUES(%s, %s)''', (chat_id, language))
            await connect.commit()
        connect.close()

    async def get_lang(self, chat_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Lang FROM language WHERE Id = %s''', (chat_id,))
        lang = await cursor.fetchone()
        connect.close()
        try:
            return lang[0]
        except:
            return 'eng'

    async def update_lang(self, chat_id, language):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE language SET Lang = %s WHERE Id = %s''', (language, chat_id))
        await connect.commit()
        connect.close()

    async def stat_text(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT COUNT(Lang) as count FROM language WHERE Id NOT LIKE "-%"''')
        all_count = await cursor.fetchone()
        all_count = all_count[0]
        await cursor.execute('''SELECT COUNT(Lang) as count FROM language WHERE Lang = "ru" AND Id NOT LIKE "-%"''')
        ru_count = await cursor.fetchone()
        ru_count = ru_count[0]
        await cursor.execute('''SELECT COUNT(Lang) as count FROM language WHERE Lang = "eng" AND Id NOT LIKE "-%"''')
        eng_count = await cursor.fetchone()
        eng_count = eng_count[0]
        await cursor.execute('''SELECT COUNT(Lang) as count FROM language WHERE Lang = "ukr" AND Id NOT LIKE "-%"''')
        ua_count = await cursor.fetchone()
        ua_count = ua_count[0]
        await cursor.execute('''SELECT COUNT(Lang) as count FROM language WHERE Lang = "deut" AND Id NOT LIKE "-%"''')
        deut_count = await cursor.fetchone()
        deut_count = deut_count[0]
        await cursor.execute('''SELECT COUNT(Lang) as count FROM language WHERE Lang = "esp" AND Id NOT LIKE "-%"''')
        esp_count = await cursor.fetchone()
        esp_count = esp_count[0]
        await cursor.execute('''SELECT COUNT(Lang) as count FROM language WHERE Lang = "fren" AND Id NOT LIKE "-%"''')
        fren_count = await cursor.fetchone()
        fren_count = fren_count[0]
        await cursor.execute('''SELECT COUNT(Lang) as count FROM language WHERE Lang = "ital" AND Id NOT LIKE "-%"''')
        ital_count = await cursor.fetchone()
        ital_count = ital_count[0]

        text = f'🇷🇺 - {ru_count} - {round(ru_count/all_count*100, 1)}%\n' \
               f'🇬🇧 - {eng_count} - {round(eng_count/all_count*100, 1)}%\n' \
               f'🇺🇦 - {ua_count} - {round(ua_count/all_count*100, 1)}%\n' \
               f'🇩🇪 - {deut_count} - {round(deut_count/all_count*100, 1)}%\n' \
               f'🇪🇸 - {esp_count} - {round(esp_count/all_count*100, 1)}%\n' \
               f'🇫🇷 - {fren_count} - {round(fren_count/all_count*100, 1)}%\n' \
               f'🇮🇹 - {ital_count} - {round(ital_count / all_count * 100, 1)}%\n'
        return text

    async def backup_language(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT * FROM language''')
        data = await cursor.fetchall()
        connect.close()
        return data
