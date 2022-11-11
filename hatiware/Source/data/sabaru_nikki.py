
from datetime import datetime
import sqlite3

class SabaruNikki():
    def __init__(self) -> None:
        self.dbname = 'Source/data/db/sabarunikki.db'
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()
        self.cur.execute(
            f'CREATE TABLE IF NOT EXISTS sabarunikki(id INTEGER PRIMARY KEY, price INTEGER NOT NULL, date DATETIME NOT NULL, description TEXT)'
        )
        self.conn.commit()
        self.__close()

    def __connect(self) -> None:
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def __close(self):
        self.conn.close()

    def set_price(self, price: int, date: datetime, description: str):
        self.__connect()
        self.cur.execute(
            'INSERT INTO sabarunikki(price, date, description) VALUES (?, ?, ?)',
            (price, date, description)
        )
        self.conn.commit()
        self.__close()

    def get_today_price(self, date: datetime):
        self.__connect()
        self.cur.execute(
            'SELECT * FROM sabarunikki WHERE date = ?',
            (date)
        )
        result: list = self.cur.fetchall()
        self.__close()
        return result

    def get_total_price(self):
        self.__connect()
        self.cur.execute(
            'SELECT sum(price) from sabarunikki'
        )
        result: list = self.cur.fetchone()
        if result:
            return int(result[0])
        return 0

    def get_price_list(self):
        self.__connect()
        self.cur.execute(
            'SELECT date, price, description from sabarunikki ORDER BY date DESC LIMIT 5'
        )
        return self.cur.fetchall()


