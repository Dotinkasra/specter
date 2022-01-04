import subprocess, requests
from Source.env.config import Config

class subcommands():
    config = Config()

    @classmethod
    def notification_mac(self, 
                        title: str = "Default", 
                        message: str = "", 
                        content_image: str = None, 
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