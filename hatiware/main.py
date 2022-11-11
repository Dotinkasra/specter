from Source.env.config import Config

from discord.ext import commands
from dislash import InteractionClient
import discord

INITIAL_EXTENSIONS = [
    'Source.cogs.mute_notification',
    'Source.cogs.image_catcher',
    'Source.cogs.chat_voicevox'
]

config = Config()

intents = discord.Intents.all()
TOKEN = config.token
bot = commands.Bot(command_prefix='h!', intents = intents)
inter_client = InteractionClient(bot)
guilds = config.guilds

for cog in INITIAL_EXTENSIONS:
    bot.load_extension(cog)

bot.run(TOKEN)