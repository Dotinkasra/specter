from Source.env.config import Config

from discord.ext import commands
from dislash import InteractionClient
import discord

INITIAL_EXTENSIONS = [
    'Source.cogs.Calc',
]

config = Config()

intents = discord.Intents.all()
TOKEN = config.token
bot = commands.Bot(command_prefix='u!', intents = intents)
inter_client = InteractionClient(bot)
guilds = config.guilds

for cog in INITIAL_EXTENSIONS:
    bot.load_extension(cog)

bot.run(TOKEN)