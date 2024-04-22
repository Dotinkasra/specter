from Source.env.config import Config
from discord.ext import commands
import discord, asyncio

config = Config()
intents = discord.Intents.all()
TOKEN = config.token
guilds = config.guilds
bot = commands.Bot(command_prefix='h!', intents = intents, activity = discord.Game("臨兵闘者皆陣烈在前！！"))

async def main():
    INITIAL_EXTENSIONS = [
        'Source.cogs.voicechannel_log',
        'Source.cogs.get_userinfo',
        'Source.cogs.auto_ban',
    ]

    for cog in INITIAL_EXTENSIONS:
        await bot.load_extension(cog)
    
    await bot.start(TOKEN)


asyncio.run(main())