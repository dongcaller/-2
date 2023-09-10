import discord
import asyncio
import pytz
import datetime
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

TICKET_MESSAGE_ID = 1150373146336186378  # 티켓 생성용 임베드 메시지의 ID를 입력하세요.
CATEGORY_ID = 1150071294352691291  # 티켓 카테고리의 ID 입력

@bot.event
async def on_ready():
    print("헬로 리버레이션 관리봇이 실행됩니다.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("문의는 티켓 열어주세요"))
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == TICKET_MESSAGE_ID and str(payload.emoji) == "🎫":
        guild = bot.get_guild(payload.guild_id)
        
        if guild:
            category = discord.utils.get(guild.categories, id=CATEGORY_ID)
            
            if category:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    payload.member: discord.PermissionOverwrite(read_messages=True)
                }
                
                ticket_channel = await category.create_text_channel(name=f"ticket-{payload.member.id}", overwrites=overwrites)
                
                await ticket_channel.send(f"{payload.member.mention}, 티켓이 생성되었습니다. 문의 내용을 작성해주세요.")

@bot.command()
@commands.has_role('Admin')  # 'Admin' 역할이 있는 사용자만 이 명령어를 사용할 수 있습니다.
async def close(ctx):
    if "ticket-" in ctx.channel.name:  # 채널 이름에 'ticket-'이 포함되어 있는지 확인합니다.
        await ctx.send("티켓이 종료되었습니다. 5초 후에 이 채널은 삭제됩니다.")
        await asyncio.sleep(5)  # 메시지가 전송된 후, 5초 동안 대기합니다.
        await ctx.channel.delete()  # 현재 채널을 삭제합니다.
    else:
        await ctx.send("이 명령어는 티켓 채널에서만 사용할 수 있습니다.")


# 봇 토큰 입력 (실제로 사용하는 것으로 교체하세요.)
token = "MTE1MDAxNTgyNjgyMTM4NjI0MA.G5Fi3b.j9tktBy_wR-bL38XuDRA0hNyV1Trp4dFzpf4gE"
bot.run(token)