from Source.env.config import Config
from discord.ext import commands
from dislash import slash_command, Option, OptionType, SelectMenu, SelectOption, OptionChoice
import re
config = Config()
admin = config.admin
guild_ids = config.guilds

class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.flag = False

    @slash_command(
        name="yaha",
        description = "フゥン…",
        options = [
            Option('ura', '……', OptionType.STRING),
        ],
        guild_ids = guild_ids
    )
    async def yaha(self, inter, ura):
        if ura is None:
            return
        if ura not in ['+', '＋', '-', '−', '÷', '/', '×', 'x', '*']:
            return
        replace_ura = re.split('[+＋-−÷/×x*]', ura)
        print(replace_ura)
        '''
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
        )'''


def setup(bot):
    return bot.add_cog(Calc(bot))