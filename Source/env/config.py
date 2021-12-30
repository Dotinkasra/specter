import configparser
import os

class Config():
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(path, 'UTF-8')
        print(self.config.sections())

    @property
    def token(self) -> str:
        return str(self.config['TOKEN']['TOKEN'])

    @property
    def guilds(self) -> list[int]:
        return list(map(int, self.config['GUILDS'].values()))

    @property
    def admin(self) -> list[int]:
        return list(map(int, self.config['ADMIN'].values()))

    @property
    def notification(self) -> list[int]:
        return list(map(int, self.config['NOTIFICATION'].values()))