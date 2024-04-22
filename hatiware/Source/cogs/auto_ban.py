import re
import discord

from discord.ext import commands
from discord import Embed
from datetime import datetime, timezone
from Source.data.banlist import BanListDataBase
from datetime import timedelta, timezone, datetime
from Source.module.sub_commands import subcommands

japan_timezone = timezone(timedelta(hours=+9), 'Asia/Tokyo')

class AutoBAN(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = BanListDataBase()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : AutoBAN')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.db.is_included_banlist(member.id): 
            print(member.name)
            await self.wrap_kick(member)
            return
        
        notification_channel = 1176360809123819570
        embed = Embed(
            title = "ようこそ……",
            description = f"{member.mention}({member.global_name}) さんが入室しました",
            color = 0x0000FF,
            timestamp = datetime.now(japan_timezone)
        ).set_image(
            url = member.display_avatar.url
        )
        print("sousin!")
        await self.bot.get_channel(notification_channel).send(
            embed = embed,
            view = self.WelcomeNoticeButton(timeout = 180, user = member),
        )

    class WelcomeNoticeButton(discord.ui.View):
        def __init__(self, *, timeout: float | None = 180, user: discord.User):
            super().__init__(timeout=timeout)
            self.target = user

        @discord.ui.button(label="ようこそ", style = discord.ButtonStyle.success)
        async def welcome(self, interaction: discord.Interaction, button: discord.ui.Button):
            embed = Embed(
                title = "ようこそ👺",
                description = f"{interaction.user.mention}に挨拶しましょう",
                color = 0xFFFF00,
                timestamp=datetime.now(japan_timezone)
            ).set_thumbnail(
                url = interaction.user.display_avatar.url
            ) if subcommands.is_dorakasu(interaction.user) else Embed (
                title = "ようこそ😆",
                description = f"{interaction.user.mention}さんが挨拶しました",
                color = 0xF0F0F0,
                timestamp=datetime.now(japan_timezone)
            ).set_thumbnail(
                url = "https://media.istockphoto.com/id/492684225/ja/%E3%83%99%E3%82%AF%E3%82%BF%E3%83%BC/%E6%9C%80%E5%88%9D%E3%81%AE%E4%BD%9C%E6%88%90.jpg?s=612x612&w=0&k=20&c=jJqjlSvdam9F_bWPKpZgaBZWEuWYN-u4etboYY97PGI="
            ) 
            await interaction.channel.send(f"{self.target.mention}", embed=embed)
            await interaction.response.send_message("")
        
        @discord.ui.button(label = "帰れ！", style = discord.ButtonStyle.gray)
        async def gohome(self,  interaction: discord.Interaction, button: discord.ui.Button):
            embed = Embed(
                title = "帰れ！🖕🏻",
                description = f"{interaction.user.mention}が怒りました",
                color = 0xFFFF00,
                timestamp=datetime.now(japan_timezone)
            ).set_thumbnail(
                url = "https://img.freepik.com/premium-photo/greek-god-poseidon-portrait_106024-777.jpg"
            ) if subcommands.is_dorakasu(interaction.user) else Embed (
                title = "帰れ！🖕🏻",
                description = f"{interaction.user.mention}さんが侮辱しました",
                color = 0xFF0000,
                timestamp=datetime.now(japan_timezone)
            ).set_thumbnail(
                url = interaction.user.display_avatar.url
            )
            await interaction.channel.send(f"{self.target.mention}", embed=embed)
            await interaction.response.send_message("")

    class AutoBanButton(discord.ui.View):
        def __init__(self, *, timeout: float | None = 180):
            super().__init__(timeout=timeout)


    @commands.Cog.listener()
    async def on_message(self, message):
        async def is_troll(message) -> bool:
            if message.author.bot:
                return False
            if message.author.guild_permissions.administrator:
                return False
            if not message.mention_everyone:
                return False
            if not re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', message.content):
                return False
            return True
        
        if await is_troll(message):
            await message.author.edit(
                nick = "馬鹿",
                timed_out_until = datetime.now(japan_timezone) + timedelta(hours=1)
            )
            embed = Embed(
                title = "臨兵闘者皆陣烈在前！！🤞😤🤌",
                description = f"{message.author.mention}退散！！",
                color = 0xFFF000,
                timestamp = datetime.now(japan_timezone)
            ).set_thumbnail(
                url = message.author.display_avatar.url,
            ).add_field(
                name = "悪霊NO",
                value = f"{message.author.id}",
            ).add_field(
                name = "悪霊名",
                value = f"{message.author.name}",
            )

            await  message.channel.send(embed = embed)
            await message.delete()
            return

    async def wrap_kick(self, member):
        embed = Embed(
            title = "🧙🏿‍♂️破アアアアアアアア！！",
            description = f"{member.mention} を除霊しました。",
            color = 0xFF0000,
            timestamp = datetime.now(japan_timezone),
        ).set_thumbnail(
            url = member.display_avatar.url
        )

        logging_channel = 1227878442616225818
        await self.bot.get_channel(logging_channel).send(embed = embed)
        await member.send(embed = embed)
        await member.kick()

async def setup(bot):
    await bot.add_cog(AutoBAN(bot))