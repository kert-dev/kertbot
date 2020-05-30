import urllib
import os
import discord
import random as random_module
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('DISCORD_BOT_TOKEN')  # Hide token in public
# DISCORD_BOT_TOKEN= 'Write Your Token' to .env file

bot = commands.Bot(command_prefix='!')  # set command prefix


@bot.event
async def on_ready():
    game = discord.Game("KERT_BOT")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("Logged as")
    print(bot.user.name)
    print(bot.user.id)


# use commands() of discord.ext instead of startswith()
@bot.command()
async def hello(ctx):
    await ctx.send("Hello, world!")


@bot.command()
async def 안녕(ctx):
    await ctx.send("Hello, world!")


@bot.command()
async def echo(ctx, *, content: str):
    await ctx.send(content)


@bot.command(name='random')
async def _random(ctx, start, end):
    randnum = random_module.randint(start, end)
    await ctx.send("Result is {}".format(randnum))


@bot.command()
async def 랜덤(ctx, start, end):
    randnum = random_module.randint(start, end)
    await ctx.send("Result is {}".format(randnum))


@bot.command(description="경북대 날씨 제공")
async def 날씨(ctx): # From Naver weather
    enc_location = urllib.parse.quote('대구광역시 북구 산격3동 날씨')
    url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=' + enc_location
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    data1 = soup.find('div', {'class': 'weather_box'})
    current_temp = data1.find('span', {'class': 'todaytemp'}).text
    max_temp = data1.find('span', {'class': 'max'}).text
    min_temp = data1.find('span', {'class': 'min'}).text
    description = data1.find('p', {'class': 'cast_txt'}).text
    data2 = data1.findAll('dd')
    pm25 = data2[0].find('span', {'class': 'num'}).text
    pm10 = data2[1].find('span', {'class': 'num'}).text
    merge_dust = str(pm25) + ',' + str(pm10)
    embed = discord.Embed(
        title='경북대 날씨 정보',
        description='산격3동 날씨 정보 제공',
        colour=discord.Colour.gold()
    )

    embed.add_field(name='현재상태', value=description, inline=False)
    embed.add_field(name='현재온도', value=current_temp + '˚C', inline=False)
    embed.add_field(name='최고온도', value=max_temp + 'C', inline=True)
    embed.add_field(name='최저온도', value=min_temp + 'C', inline=True)
    embed.add_field(name='미세먼지/초미세먼지', value=merge_dust, inline=False)

    await ctx.send(embed=embed)


bot.run(token)
