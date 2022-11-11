import configparser
import os

class Config():
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(path, 'UTF-8')

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

    @property
    def ifttt_event(self) -> str:
        return str(self.config['IFTTT']['EVENT'])

    @property
    def ifttt_key(self) -> str:
        return str(self.config['IFTTT']['KEY'])

    @property
    def ubernikki(self) -> str:
        return str(self.config['CHANNEL']['UBERNIKKI'])

    @property
    def speaker(self) -> dict:
        return dict(self.config['SPEAKER'])