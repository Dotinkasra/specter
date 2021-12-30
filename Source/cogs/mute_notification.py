from discord.ext import commands
from Source.env.config import Config
import discord

config = Config()
admin = config.admin
class MuteNotification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : MuteNotification')

def setup(bot):
    bot.add_cog(MuteNotification(bot))