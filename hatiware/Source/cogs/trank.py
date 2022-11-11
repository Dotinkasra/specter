from Source.env.config import Config
from discord.ext import commands
from dislash import slash_command, Option, OptionType, SelectMenu, SelectOption

config = Config()
admin = config.admin
guild_ids = config.guilds

class Data():
    def __init__(self, max) -> None:
        self._deck = list(range(1, max + 1))

    def get_deck(self) -> list:
        return self._deck

    def trash(self, num) -> None:
        self._deck.remove(num)

    def search(self, num) -> bool:
        return num in self._deck

class Trank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.flag = False

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : Trank')
    
    @slash_command(
    name="trank",
    description = "1~入力された数字(最大100)までを管理します",
    guild_ids = guild_ids
    )
    async def trank(self, inter):

        self.deck = Data(max)
        self.flag = True

        await inter.respond(f"起動しました\n{self.deck.get_deck()}")

    @trank.sub_command()
    async def trash(inter):
        await inter.replay(f"trash")
    
    @slash_command(
    name="_trank",
    description = "1~入力された数字(最大100)までを管理します",
    options = [
        Option('max', '数字を入力', OptionType.INTEGER),
    ],
    guild_ids = guild_ids
    )
    async def createdatid_(self, inter, max = None):
        if max is None:
            return
        if max > 100:
            max = 100

        self.deck = Data(max)
        self.flag = True

        await inter.respond(f"起動しました\n{self.deck.get_deck()}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.flag:
            return
        if message.author.bot:
            return
        if not message.content == "trank":
            return

        msg = await message.channel.send(
            "This message has a select menu!",
            components=[
                SelectMenu(
                    custom_id="test",
                    placeholder="Choose up to 2 options",
                    max_values=2,
                    options=[
                        SelectOption("カードを捨てます", "value 1"),
                        SelectOption("Option 2", "value 2"),
                        SelectOption("Option 3", "value 3")
                    ]
                )
            ]
        )
        def check(inter):
            # inter is instance of MessageInteraction
            # read more about it in "Objects and methods" section
            if not inter.author == message.author:
                return
        # Wait for a menu click under the message you've just sent
        inter = await msg.wait_for_dropdown(check)
        # Tell which options you received
        labels = [option.label for option in inter.select_menu.selected_options]
        await inter.reply(f"Your choices: {', '.join(labels)}")

def setup(bot):
    return bot.add_cog(Trank(bot))