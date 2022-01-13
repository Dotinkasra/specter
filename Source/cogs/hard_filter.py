from discord.ext import commands
from datetime import datetime, timezone

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
            
def setup(bot):
    return bot.add_cog(HardFilter(bot))