import aiomysql
import config
import ast

'''
CREATE TABLE IF NOT EXISTS scan(
Hash TEXT,
Result JSON)
'''

class Scan:

    async def add_scan(self, hash, result):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''INSERT INTO scan VALUES(%s, %s)''', (hash, str(result)))
        await connect.commit()
        connect.close()


    async def get_result(self, hash):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Result FROM scan WHERE hash = %s''', (hash))
        result = await cursor.fetchone()
        connect.close()
        try:
            return ast.literal_eval(result[0])
        except:
            return False
