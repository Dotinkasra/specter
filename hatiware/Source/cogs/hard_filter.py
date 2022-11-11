from discord.ext import commands
from datetime import datetime, timezone
from Source.module.sub_commands import subcommands

class HardFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : HardFilter')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.created_at >= datetime(
            year=2021, month=11, day=1, hour=0, minute=0, microsecond=0, 
            tzinfo=timezone.utc
        ):
            await member.kick()
        subcommands.send_webhook({"value1" : f"{member.name}さんが参加しました。"})

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await member.guild.guild.get_channel(
            930213770737909791
        ).send(
            f'{member.name}さんが退出しました'
        )
            
def setup(bot):
    return bot.add_cog(HardFilter(bot))