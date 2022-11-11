from sys import path
from urllib import request
import pyocr, requests, re, os, discord
from re import S
from PIL import Image
from discord.ext import commands, tasks
from dislash import slash_command, Option, OptionType
from datetime import datetime, timezone, date
from Source.env.config import Config
from Source.data.sabaru_nikki import SabaruNikki

# OCRエンジンを取得
engines = pyocr.get_available_tools()
engine = engines[0]

config = Config()
db = SabaruNikki()
# 対応言語取得
langs = engine.get_available_languages()

class Sabaru(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.master_flg = True
        self.now = datetime.now().strftime('%H:%M')
        self.loop.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : Sabaru')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        #通知対象のメンバーではない場合、処理を終了
        if member.id != 903536005087395841:
            return

        if before.channel is None and after.channel is not None:

            if db.get_total_price() < 10000:
                await member.guild.get_channel(928716168699715614).send(
                    f'{member.mention} コラーーッ！　稼いでないのに入っちゃダメ〜〜〜！'
                )
                await member.edit(mute = True)
            else:
                await member.edit(mute = False)

    def get_today(self):
        return date.today()

    @slash_command(
        name="teihenn",
        description = "サーバルさんの稼いだ金額を確認します",
        guild_ids = config.guilds
    )
    async def teihenn(self, inter):
        total = db.get_total_price()
        if total < 0:
            await inter.send(str(format(total, ',')) + '円のマイナスだって〜〜〜〜！！')
        elif total < 12000:
            await inter.send(str(format(total, ',')) + '円……！これじゃ通話できないね……')
        elif total <= 24000:
            await inter.send(str(format(total, ',')) + '円溜まった……ッ！でも通話したら消えちゃうね〜……')
        else:
            await inter.send(str(format(total, ',')) + '円もある〜〜！！')

    @slash_command(
        name="teihenn5",
        description = "直近5日間の収支を表示します",
        guild_ids = config.guilds
    )
    async def teihenn5(self, inter):
        price_5days = db.get_price_list()
        embed = discord.Embed(
                    title = "サーバル貯金箱", #タイトル
                    color = 0xffd700
                    )
        embed.add_field(name = "【収支】", value = f'{self.get_today()} 現在', inline = False)

        print(type(price_5days))
        for price in price_5days:
            embed.add_field(name = f'{price[0]} ： {str(format(price[1], ","))}', value = price[2], inline = False)

        await inter.respond(
            embed = embed,
            ephemeral = False 
        )

    @slash_command(
        name="muda",
        description = "使用したお金を貯金から減らします",
        options = [
            Option('price', '金額', OptionType.INTEGER),
            Option('desc', '使用用途', OptionType.STRING)
        ],
        guild_ids = config.guilds
    )
    async def teihenn5(self, inter, price: int, desc: str = None):
        if price is None:
            return
        if price < 0:
            price *= -1

        db.set_price(
            price * -1, 
            self.get_today(),
            desc if desc is not None else ''
        )

        embed = discord.Embed(
            title = "使っちゃった！！", #タイトル
            description = 'お金が減ったよ〜〜〜……',
            color = 0xdc143c
        )
        embed.add_field(name = str(format(db.get_total_price(), ","))+'円', value = '現在の貯金額', inline = False)

        await inter.respond(
            embed = embed,
            ephemeral = False 
        )

    @tasks.loop(seconds = 60)
    async def loop(self):
        if self.now == '12:00':
            db.set_price(-10000, self.get_today(), '通話代')
            self.now = '12:01'
        else:
            self.now = datetime.now().strftime('%H:%M')

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message.attachments)
        if message.author.bot \
            or not str(message.channel.id) == str(config.ubernikki) \
            or message.attachments is None or not len(message.attachments) == 1:

            return

        self.save_img(
            name = message.attachments[0].filename, 
            url = message.attachments[0].url
        )
        
        m = self.get_money(
            self.convert_white(message.attachments[0].filename)
            )
        if m is None:
            return
        db.set_price(m, self.get_today(), 'Uber')
        await message.channel.send(self.get_talk(m))

    def get_money(self, img: Image) -> int:
        # 画像の文字を読み込む
        builder = pyocr.builders.TextBuilder(tesseract_layout = 10)
        txt = engine.image_to_string(img, lang="eng", builder = builder) # 修正点：lang="eng" -> lang="jpn"
        en = [s for s in txt.split() if '¥' in s]
        test = [re.sub(r'\D', '', s) for s in en]
        test = [int(s) for s in list(filter(lambda a: a != '', test))]
        print(en)

        if test:
            self.today_price = max(test)
            return max(test)
        else:
            return None

    def convert_white(self, name: str) -> Image:
        original = Image.open(name).crop((110, 180, 726, 300)).convert('RGB')
        new_img = Image.new('RGB', original.size)
        border = 110
        for x in range(original.size[0]):
            for y in range(original.size[1]):
                r, g, b = original.getpixel((x, y))
                if r > border or g > border or b > border:
                    r = 255
                    g = 255
                    b = 255
                new_img.putpixel((x, y), (r, g, b))
        self.remove_img(name)
        return new_img
            
    def save_img(self, name: str, url: str):
        with open(name, "wb") as f:
            f.write(requests.get(url).content)
    
    def remove_img(self, name: str):
        os.remove(name)

    def get_img_name(self, url: str):
        return url[url.rfind('/') + 1]

    def get_talk(self, price: int):
        disp_price = str(format(price, ',')) + '円'
        if price <= 8000:
            return f'{disp_price}……！！「怠惰な擬態型が沖縄に幽閉されてた」…ってコト！？'
        elif price <= 10000:
            return f'エ〜〜〜ッ！！ {disp_price}しか稼げてないのォ！？'
        elif price <= 11000:
            return f'{disp_price}だとご飯…買えないね……。ずっと汁だから胃がちぢんじゃう〜…'
        elif price <= 11500:
            return f'確かに……{disp_price}だと正規雇用のほうがいいかも……。でもなんでか……Uberやめないでって気持ちもある……。心がふたつある〜〜'
        elif price <= 12000:
            return f'{disp_price}でもだいじょぶだよーッ'
        elif price <= 12300:
            return f'ワッワッ　お〜い！！　どッ…どうだった？　エッ……{disp_price}………。何回でも…ずっと応援するからね！！'
        elif price <= 12700:
            return f'{disp_price}しか稼いでないけど……なんとかなれーッ！！'
        elif price <= 13000:
            return f'報酬アップさせようよ‼'
        elif price <= 13300:
            return f'あ……これチップじゃない！！　オロナミンCのフタだッ'
        elif price <= 13700:
            return f'{disp_price}しか稼げないけど…あんまり困ることないねー'
        elif price <= 14000:
            return f'上位ランカーだッ……さっき聞こえたんだけど、配達件数ランキングの４位までに入ると武器に……「{disp_price}のマーク」入れてもらえるって！！'
        elif price <= 14300:
            return f'憧れるよねッ　仕事帰りの立ち食いそば！！　前もサラリーマンのあの姿見たことあって…同じように正規雇用になって立ち食いそば食べたいなって……'
        elif price <= 14700:
            return f'{disp_price}……って書いてあるッ……。あッ！！これ書いてあるんじゃないッ　「彫って」あるんだッ'
        elif price <= 15000:
            return f'{disp_price}でも焦んなくて大丈夫だよー'
        elif price <= 15300:
            return f'Uberで配達すると{disp_price}もらえるんだって……。でも……{disp_price}をもらっても…なんか…やな気持ちになるんだってッ。じわじわ…怖いよねッ'
        elif price <= 15700:
            return f'{disp_price}しか稼げないけど…あんまり困ることないねー'
        elif price <= 16000:
            return f'なんかッ…っフッ……フッ…ンフフッ…ごめんッ……笑っちゃって……ッ　ごめッ…フッフッ…フ　力（ちから）ッ…入らなくなるッッ　あはははははッッ'
        elif price <= 16300:
            return f'わゥッまた流れ星？　これって絶対……願い叶うやつじゃん！！{disp_price}貰えますように！！{disp_price}貰えますように！！{disp_price}貰えますように！！'
        elif price <= 20000:
            return f'ヤッター{disp_price}だネー！！'
        else:
            return f'稼ぎすぎです。'

def setup(bot):
    return bot.add_cog(Sabaru(bot))