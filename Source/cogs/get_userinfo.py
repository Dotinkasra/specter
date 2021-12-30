from discord import guild
from Source.env.config import Config
from discord.ext import commands
from dislash import slash_command, ActionRow, Button, ButtonStyle, Option, OptionType
import discord

config = Config()
guild_ids = config.guilds
class GetUserinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : GetUserinfo')

    @slash_command(
        name="createdatid_",
        description = "ユーザIDの作成日を見る",
        options = [
            Option('userid', 'ユーザIDを入力', OptionType.STRING),
        ],
        guild_ids = guild_ids
    )
    async def createdatid_(self, inter, userid = None):
        if userid is None:
            return
        user = await self.bot.fetch_user(userid)
        bunner_color = 0x00ff00 if user.accent_colour is None else user.accent_colour.value
        embed = discord.Embed(
                            title = "ユーザについて", #タイトル
                            color = bunner_color, # 色
                            description = str(user), # 説明文 
                            )
        embed.set_thumbnail(url = user.display_avatar.url)
        embed.add_field(name = "作成日", value = user.created_at.strftime('%Y年%m月%d日 %H時%M分'))
        #embed.add_field(name = "メール認証", value = user.verified)

        await inter.respond(
            embed = embed,
            ephemeral = False 
        )

def setup(bot):
    bot.add_cog(GetUserinfo(bot))