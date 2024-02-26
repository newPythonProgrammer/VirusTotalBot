import aiomysql

import config

'''
CREATE TABLE IF NOT EXISTS token(
Token TEXT,
Hour_request INT DEFAULT 0,
Day_request INT DEFAULT 0,
Mouth_request INT DEFAULT 0);
'''


class Token:
    async def add_token(self, token):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''INSERT INTO token(Token) VALUES(%s)''', (token,))
        await connect.commit()
        connect.close()

    async def del_token(self, token):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''DELETE FROM token WHERE Token = %s''', (token,))
        await connect.commit()
        connect.close()

    async def get_all_tokens(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Token FROM token''')
        tokens = await cursor.fetchall()
        token_list = [i[0] for i in tokens]
        return token_list

    async def get_random_token(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Token FROM token WHERE Day_request<500 AND Hour_request<240 AND Mouth_request<15500 ORDER BY RAND() LIMIT 1''')
        token = await cursor.fetchone()
        connect.close()
        return token[0]

    async def disactive_token(self, token):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE token SET Day_request=500 WHERE Token = %s''', (token,))
        await connect.commit()
        connect.close()


    async def update_stat(self, token, mouth, day, hour):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE token SET Mouth_request = %s, Day_request=%s, Hour_request=%s WHERE Token = %s''', (mouth, day, hour, token))
        await connect.commit()
        connect.close()

    async def reset_hour_request(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE token SET Hour_request = 0''')
        await connect.commit()
        connect.close()

    async def reset_day_request(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE token SET Day_request = 0''')
        await connect.commit()
        connect.close()

    async def reset_mouth_request(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE token SET Mouth_request = 0''')
        await connect.commit()
        connect.close()

    async def get_stat_text(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT SUM(Hour_request) as sum FROM token''')
        hour_request = await cursor.fetchone()
        hour_request = hour_request[0]
        await cursor.execute('''SELECT SUM(Day_request) as sum FROM token''')
        day_request = await cursor.fetchone()
        day_request = day_request[0]
        await cursor.execute('''SELECT SUM(Mouth_request) as sum FROM token''')
        mouth_request = await cursor.fetchone()
        mouth_request = mouth_request[0]
        await cursor.execute('''SELECT COUNT(Token) as count FROM token''')
        count_token = await cursor.fetchone()
        count_token = count_token[0]
        text = f'Использование токенов\n\n' \
               f'За час: {hour_request}/{count_token*240}\n' \
               f'За день: {day_request}/{count_token*500}\n' \
               f'За месяц: {mouth_request}/{count_token*15500}'
        return text


