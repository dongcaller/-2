import discord
import asyncio
import pytz
import datetime
from discord.ext import commands

token = 'MTE1MDAxMDY1NjAzNzI3MzY4MA.GD7cBi.FEELOadmPZVLEZ3g38S-UU6bMur1yjDqxi4fA0'
client = bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@client.event
async def on_ready():
    print("헬로 리버레이션 관리봇이 실행됩니다.")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("헬로 리버레이션 관리"))

@client.event
async def on_message(message):
    if message.content.startswith ("!청소"):
        if message.author.guild_permissions.administrator:
            amount = message.content[4:]
            await message.delete()
            await message.channel.purge(limit=int(amount))

            embed = discord.Embed(title="메시지 삭제 알림", description="최근 디스코드 채팅 {}개가\n관리자 {}님의 요청으로 인해 정상 삭제 조치 되었습니다".format(amount, message.author), color=0x000000)
            embed.set_footer(text="담당 관리자 : {}".format(message.author), icon_url="https://cdn.discordapp.com/attachments/1043109494802096149/1150020891741270127/result.png%22")
            await message.channel.send(embed=embed)

        else:
            await message.delete()
            await message.channel.send("{}, 당신은 명령어를 사용할 수 있는 권한이 없습니다".format(message.author.mention))

    if message.content.startswith ("!공지"):
        notice = message.content[4:]
        channel_id = 979582104243433543
        channel = client.get_channel(channel_id)

        embed = discord.Embed(title="공지사항", description="공지사항 내용은 항상 숙지 해주시기 바랍니다\n――――――――――――――――――――――――――――\n\n{}\n\n――――――――――――――――――――――――――――".format(notice), color=0x00ff00)
        embed.set_footer(text="담당 관리자 : {}".format(message.author))
        await channel.send("@everyone", embed=embed)


client.run(token)