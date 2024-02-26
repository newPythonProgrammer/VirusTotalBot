import aiomysql
import config


'''
CREATE TABLE IF NOT EXISTS chat(
Id DECIMAL(17, 0),
Title TEXT,
Members INT,
Username TEXT,
File_status BOOL,
Domain_status BOOL,
IP_status BOOL)
'''

class Chat:
    async def add_chat(self, chat_id, title, members, username):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''INSERT INTO chat VALUES(%s, %s, %s, %s, 1, 0, 0)''', (chat_id, title, members, username))
        await connect.commit()
        connect.close()

    async def check_chat(self, chat_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT * FROM chat WHERE Id = %s''', (chat_id,))
        result = await cursor.fetchone()
        connect.close()
        return bool(result)

    async def edit_member(self, chat_id, members):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE chat SET Members = %s WHERE Id = %s''', (members, chat_id))
        await connect.commit()
        connect.close()

    async def get_chat_stat(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT SUM(Members) as member FROM chat''')
        members = await cursor.fetchone()
        await cursor.execute('''SELECT COUNT(Id) as count FROM chat''')
        count = await cursor.fetchone()
        return f'Кол-во чатов: {count[0]}\n' \
               f'Участников в них: {members[0]}'

    async def get_settings_chat(self, chat_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT File_status, Domain_status, IP_status FROM chat WHERE Id = %s''', (chat_id,))
        result = await cursor.fetchone()
        connect.close()
        return {'file_status': result[0], 'domain_status': result[1], 'ip_status': result[2]}


    async def set_file_setting(self, chat_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE chat SET File_status = 1 WHERE Id = %s''', (chat_id, ))
        await connect.commit()
        connect.close()

    async def del_file_setting(self, chat_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE chat SET File_status = 0 WHERE Id = %s''', (chat_id, ))
        await connect.commit()
        connect.close()

    async def set_domain_setting(self, chat_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE chat SET Domain_status = 1 WHERE Id = %s''', (chat_id, ))
        await connect.commit()
        connect.close()

    async def del_domain_setting(self, chat_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE chat SET Domain_status = 0 WHERE Id = %s''', (chat_id, ))
        await connect.commit()
        connect.close()

    async def set_ip_setting(self, chat_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE chat SET IP_status = 1 WHERE Id = %s''', (chat_id, ))
        await connect.commit()
        connect.close()

    async def del_ip_setting(self, chat_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE chat SET IP_status = 0 WHERE Id = %s''', (chat_id, ))
        await connect.commit()
        connect.close()

    async def backup_chat(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Id, Title, Members, Username FROM chat''')
        data = await cursor.fetchall()
        connect.close()
        return data