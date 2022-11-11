from discord.ext import commands
from Source.env.config import Config
from Source.module.sub_commands import subcommands

config = Config()
admin = config.admin
notification = config.notification

class MsgNotification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : MsgNotification')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.channel.id == "957191422937817088":
            return 
            
        await message.guild.get_channel(
                957191422937817088
            ).send(
                f'{message.author.name}\n{message.content}'
            )
        if message.attachments is not None:
            for a in message.attachments:
                await message.guild.get_channel(
                        957191422937817088
                    ).send(
                        f'{a.url}'
                    )

def setup(bot):
    return bot.add_cog(MsgNotification(bot))