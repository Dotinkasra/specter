from discord.ext import commands
from Source.env.config import Config
from Source.module.sub_commands import subcommands

config = Config()
speaker: dict = config.speaker

from io import BytesIO
from typing import Any

import discord
import json
import wave
import urllib.parse
import requests
import simpleaudio
import re

class VoiceBox():
    def __init__(self, domain = "0.0.0.0", port = "8050") -> None:
        self.domain = domain
        self.port = port

    def get_audio_query(self, text: str, speaker: int = 3) -> Any:
        try:
            text = urllib.parse.quote(text)
            url = f'http://{self.domain}:{self.port}/audio_query?text={text}&speaker={str(speaker)}'
            headers = {
                'accept': 'application/json'
            }
            response = requests.post(
                url,
                headers=headers
            )
            return response.json()
        except:
            return None

    def play_sound_from_synthesis(self, text: str, speaker: int = 3) -> None:
        response_body = self.get_audio_query(text, speaker)
        if response_body is None:
            return None

        url = f'http://{self.domain}:{self.port}/synthesis'

        header = {
            'accept': 'audio/wav',
            'Content-Type': 'application/json'
        }
        params = {
            'speaker': str(speaker)
        }
        try:
            response = requests.post(
                f'{url}',
                headers = header,
                params = params,
                data = json.dumps(response_body)
            )
        
            if not response.status_code == 200:
                return None
        except:
            return None

        with wave.open(BytesIO(response.content)) as bs:
            wav_obj = simpleaudio.WaveObject.from_wave_read(bs)
            play_obj = wav_obj.play()
            play_obj.wait_done()

class ChatVoicevox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vv = VoiceBox()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : ChatVoicevox')

    @commands.Cog.listener()
    async def on_message(self, message):
        dora = message.guild.get_member(701781200288743434)

        if dora.voice is None:
            return 

        if not message.channel.id == int(speaker['channel']):
            return
        
        msg = message.content if len(message.content) < 120 else message.content[:120] + "以下省略"
        msg = re.sub('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+.*', '。URL省略。', msg)

        for member in message.mentions:
            msg = msg.replace(f"@{member.id}", f"。メンション。あっと、{member.name}。")

        print(message.mentions)
        
        if str(message.author.id) in speaker:
            self.vv.play_sound_from_synthesis(msg, speaker[str(message.author.id)])
        else:
            self.vv.play_sound_from_synthesis(msg)

    def is_calling(self, guild_id: int, member_id: int) -> bool:
        guild = self.bot.get_guild(guild_id)
        member = guild.get_member(member_id)
        if member.voice is None:
            return False
        return True
        

def setup(bot):
    return bot.add_cog(ChatVoicevox(bot))