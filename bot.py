import urllib
import os
import discord
import random
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

token = os.getenv('DISCORD_BOT_TOKEN') # 공개된 코드에 토큰을 노출하면 안 됨
# .env 파일에 DISCORD_BOT_TOKEN=토큰입력


@client.event
async def on_ready(): # 봇 실행 시 동작
    await client.change_presence(status=discord.Status.online, activity=discord.Game("bot이 실행중입니다"))
    print("실행 성공")
    print(client.user.name)
    print(client.user.id)


@client.event
async def on_message(message): # 메시지를 받을 시 동작
    if message.author.bot:  # 봇이 보낸 내용은 무시
        return
    
    # message.content에 message의 모든 내용이 담김
    if message.content == '!hello' or message.content == '!안녕':
        await message.channel.send("Hello world!")

    if message.content == '!echo':
        content = message.content.split()[1:]
        await message.channel.send(content)
    
    # startswith로 명령어 구분
    if message.content.startswith('!random') or message.content.startswith('!랜덤'):
        _range = message.content.split(" ")
        try:
            start = int(_range[1])
            end = int(_range[2])
        except IndexError:
            await message.channel.send("Usage: !random(랜덤) start_num end_num")
        else:
            randnum = random.randint(start, end)
            await message.channel.send("Result is {}".format(randnum))

    if message.content == '!날씨':
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

        await message.channel.send(embed=embed)

client.run(token)
