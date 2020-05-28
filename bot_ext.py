import urllib
import os
import discord
import random as random_module # 명령어랑 겹쳐서 땜빵..
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('DISCORD_BOT_TOKEN') # 공개된 코드에 토큰을 노출하면 안 됨
# .env 파일에 DISCORD_BOT_TOKEN=토큰입력

bot = commands.Bot(command_prefix='!')  # 명령어 prefix 지정

@bot.event
async def on_ready(): # 봇 실행 시 동작
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("bot이 실행중입니다"))
    print("실행 성공")
    print(bot.user.name)
    print(bot.user.id)

# startswith 대신 discord.ext의 commands 사용
@bot.command()
async def hello(ctx): 
    await ctx.send("Hello, world!") 

@bot.command()
async def 안녕(ctx): 
    await ctx.send("Hello, world!") 
        
@bot.command()
async def echo(ctx, *, content:str):
    await ctx.send(content)

@bot.command()
async def random(ctx, start, end):
    randnum = random_module.randint(start, end)
    await ctx.send("Result is {}".format(randnum))


@bot.command()
async def 랜덤(ctx, start, end):
    randnum = random_module.randint(start, end)
    await ctx.send("Result is {}".format(randnum))

@bot.command()
async def 날씨(ctx):
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
        
    # inline = True는 한줄에 다 나타내는 것
    embed.add_field(name='현재상태', value=description, inline=False)
    embed.add_field(name='현재온도', value=current_temp + '˚C', inline=False)
    embed.add_field(name='최고온도', value=max_temp + 'C', inline=True)
    embed.add_field(name='최저온도', value=min_temp + 'C', inline=True)
    embed.add_field(name='미세먼지/초미세먼지', value=merge_dust, inline=False)

    await ctx.send(embed=embed)

bot.run(token)
