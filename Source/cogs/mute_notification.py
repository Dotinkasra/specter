import subprocess
import requests
from discord.ext import commands
from Source.env.config import Config
from Source.module.sub_commands import subcommands

config = Config()
admin = config.admin
notification = config.notification

class MuteNotification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : MuteNotification')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        #通知対象のメンバーではない場合、処理を終了
        if member.id not in notification:
            return
        title = message = None
        display_avatar = member.display_avatar.url
        if before.channel is None and after.channel is not None:
            title = f"{member.display_name} (#{after.channel.name}, {after.channel.category})"
            message = "通話に参加しました"

        if before.channel is not None and after.channel is None:
            title = f"{member.display_name} (#{before.channel.name}, {before.channel.category})"
            message = "通話を切断しました"

        if not before.self_mute and after.self_mute:
            title = f"{member.display_name} (#{before.channel.name}, {before.channel.category})"
            message = "ミュートしました"
        
        if before.self_mute and not after.self_mute:
            title = f"{member.display_name} (#{after.channel.name}, {before.channel.category})"
            message = "ミュート解除しました"

        if title is None or message is None:
            return

        subcommands.send_webhook({"value1" : f"{title}, {message}"})
        subcommands.notification_mac(title = title, message = message, content_image = display_avatar)

def setup(bot):
    return bot.add_cog(MuteNotification(bot))