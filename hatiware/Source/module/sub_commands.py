import subprocess, requests
from Source.env.config import Config
import socket
import pickle
import discord

class subcommands():
    config = Config()

    @classmethod
    def notification_mac(self, title: str = "Default", 
                        message: str = "", content_image: str = None, 
                        sender: str = "com.hnc.Discord") -> None:
        cmd: dict = ["terminal-notifier", "-title", title, "-message", message, "-sender", sender]
        if content_image:
            cmd += ["-contentImage", content_image]
        subprocess.run(cmd)

    @classmethod
    def send_webhook(self, payload: dict) -> None:
        url: str = f'https://maker.ifttt.com/trigger/{self.config.ifttt_event}/json/with/key/{self.config.ifttt_key}'
        headers: dict = {'Content-Type': "application/json"}
        requests.post(url, json = payload, headers = headers)

    @classmethod
    def send_notification_by_socket(self, title: str = "Default", 
                                    message: str = "", content_image: str = None, 
                                    sender: str = "com.hnc.Discord") -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(("192.168.11.76", 14444))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            s.send(pickle.dumps({
                "type" : "cmd",
                "title": title,
                "message": message,
                "sender": content_image,
                "contentimage": content_image,
                "sender": sender
            }))
        except Exception as e:
            print(e)
            return

    @classmethod
    def send_wav_by_socket(self, wav_obj) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(("192.168.11.76", 14444))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            s.send(pickle.dumps({
                "type" : "wave",
                "content" : wav_obj
            }))
        except Exception as e:
            print(e)
            return
        
    @classmethod
    def is_dorakasu(self, user: discord.User):
        if user.id == 701781200288743434:
            return True
        return False
