import aiomysql
import config

'''
CREATE TABLE IF NOT EXISTS proxy(
Id INT PRIMARY KEY AUTO_INCREMENT,
Proxy TEXT,
Status TINYINT);
'''

class Proxy:
    async def add_proxy(self, proxy:str):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''INSERT INTO proxy(Proxy, Status) VALUES(%s, 1)''', (proxy, ))
        await connect.commit()
        connect.close()

    async def get_all_proxy(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Id, Proxy FROM proxy''')
        data = await cursor.fetchall()
        connect.close()
        return data

    async def del_proxy(self, proxy_id:int):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''DELETE FROM proxy WHERE Id = %s''', (proxy_id,))
        await connect.commit()
        connect.close()

    async def del_all_proxy(self, ):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''DELETE FROM proxy''')
        await connect.commit()
        connect.close()

    async def get_random_proxy(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Proxy FROM proxy WHERE Status=1 ORDER BY RAND() LIMIT 1''')
        proxy = await cursor.fetchone()
        connect.close()
        return proxy[0]

    async def disactive_proxy(self, proxy):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE proxy SET Status = 0 WHERE Proxy = %s''', (proxy,))
        await connect.commit()
        connect.close()

    async def active_proxy(self, proxy):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE proxy SET Status = 1 WHERE Proxy = %s''', (proxy,))
        await connect.commit()
        connect.close()


    async def activate_all_proxy(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE proxy SET Status = 1''')
        await connect.commit()
        connect.close()

    async def get_status_proxy(self, proxy):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Status FROM proxy WHERE Proxy = %s''', (proxy,))
        status = await cursor.fetchone()
        return status[0]
