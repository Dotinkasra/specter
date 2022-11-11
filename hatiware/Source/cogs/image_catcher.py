from tkinter import Image
from discord.ext import commands
from Source.env.config import Config
from Source.module.sub_commands import subcommands
from Source.data.image_catch_log import ImageCatchLog
import requests, datetime

db = ImageCatchLog()

class ImageCatcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : ImageCatcher')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.attachments is None:
            return

        for a in message.attachments:
            self.save_img(
                name = a.filename, 
                url = a.url
            )
            db.set_contents(
                filename=a.filename,
                url = a.url,
                author = message.author.name,
                date = datetime.datetime.now()
            )

    def save_img(self, name: str, url: str):
        with open(f'Source/data/img/{name}', "wb") as f:
            f.write(requests.get(url).content)

def setup(bot):
    return bot.add_cog(ImageCatcher(bot))