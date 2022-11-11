
from datetime import datetime
import sqlite3

class ImageCatchLog():
    def __init__(self) -> None:
        self.dbname = 'Source/data/db/image_log.db'
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()
        self.cur.execute(
            f'CREATE TABLE IF NOT EXISTS image_log(id INTEGER PRIMARY KEY, filename TEXT NOT NULL, url TEXT NOT NULL, author TEXT NOT NULL, date DATETIME NOT NULL)'
        )
        self.conn.commit()
        self.__close()

    def __connect(self) -> None:
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def __close(self):
        self.conn.close()

    def set_contents(self, filename: str, url: str, author: str, date: datetime):
        self.__connect()
        self.cur.execute(
            'INSERT INTO image_log(filename, url, author, date) VALUES (?, ?, ?, ?)',
            (filename, url, author, date)
        )
        self.conn.commit()
        self.__close()
