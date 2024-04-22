import sqlite3

class BanListDataBase():
    def __init__(self) -> None:
        self.dbname = 'Source/data/db/banlist.db'
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()
        self.cur.execute(
            f'CREATE TABLE IF NOT EXISTS BANLIST (USER_ID INTEGER PRIMARY KEY, EXPLAIN TEXT NULL, SCREEN_ID TEXT NULL)'
        )
        self.conn.commit()
        self.__close() 

    def __connect(self) -> None:
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def __close(self):
        self.conn.close()

    def is_included_banlist(self, user_id: int) -> bool:
        self.__connect()
        sql = f'SELECT USER_ID FROM BANLIST WHERE USER_ID = ?'
        param = (user_id,)
        self.cur.execute(sql, param)
        result: list = self.cur.fetchall()
        self.__close()

        if result and len(result) > 0:
            return True
        return False

