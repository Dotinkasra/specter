import subprocess
from discord import message
from discord.ext import commands
from Source.env.config import Config
from subprocess import PIPE

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
        
        display_avatar = member.display_avatar.url
        if before.channel is None and after.channel is not None:
            title = "参加通知"
            message = member.display_name + "さんが" + after.channel.name + "に参加しました"

        if before.channel is not None and after.channel is None:
            title = "切断通知"
            message = member.display_name + "さんが通話を切断しました"

        if not before.self_mute and after.self_mute:
            title = "ミュート通知"
            message = member.display_name + "さんがミュートになりました"
        
        if before.self_mute and not after.self_mute:
            title = "ミュート解除通知"
            message = member.display_name + "さんがミュートを解除しました"
        subprocess.run(["terminal-notifier", "-title", title, "-message", message, "-contentImage", display_avatar, "-sender", "com.hnc.Discord"])

def setup(bot):
    return bot.add_cog(MuteNotification(bot))