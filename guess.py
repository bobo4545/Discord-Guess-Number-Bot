import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import asyncio
import random
import datetime

load_dotenv()
bot = commands.Bot(command_prefix='>', self_bot=True)

TARGET_USER_IDS = [860536596758396938, 795160064713293854, 985532746027925595] #只檢測這些使用者的訊息
TARGET_CHANNEL_IDS = [1139232670451236926, 1139213393434263665] #檢測是否有傳訊息
PROTECTED_CHANNEL_ID = 1139213393434263665 #連續猜測超過12次 通知
Guess_Channel_ID = 934035353793343530 #該伺服器猜數字頻道
Notify_Channel_ID = 1139213393434263665 #暫停猜數字功能20分鐘 通知

min_number = 1
max_number = 1001
current_guess = None
consecutive_count = 0
isStop = 0

@bot.event
async def on_ready():
    print('Bot logged in')

@bot.event
async def on_message(message):
    global min_number, max_number, current_guess, consecutive_count, isStop

    if message.channel.id == Guess_Channel_ID:  # 检查是否为目标频道ID
        consecutive_count = 0
        if isStop == 0:
            channel = bot.get_channel(Notify_Channel_ID) #通知頻道ID
            await channel.send("已暫停猜數字功能，將在 20 分鐘後恢復。")
        isStop = 1
        await asyncio.sleep(1200)  # 暂停程序 10 分钟（600 秒）
        isStop = 0
        channel = bot.get_channel(1139232670451236926) #設定要猜的機器人頻道ID
        await channel.send("您猜到了")
        return

    if message.channel.id in TARGET_CHANNEL_IDS and message.author.id in TARGET_USER_IDS:
        if isStop == 0:
            if "您猜到了" in message.content.lower():
                consecutive_count = 0
                current_guess = 500
                min_number = 1
                max_number = 1001
                await asyncio.sleep(2)
                await message.channel.send(f"SN!猜數字 {current_guess}")
            
            elif "大於" in message.content.lower():
                consecutive_count += 1
                if consecutive_count > 12:
                    channel = bot.get_channel(PROTECTED_CHANNEL_ID)
                    await channel.send("已連續猜測超過12次，強制停止循環。")
                    consecutive_count = 0
                    return
                await asyncio.sleep(1)
                max_number = current_guess
                current_guess = (min_number + max_number) // 2
                await message.channel.send(f"SN!猜數字 {current_guess}")
            
            elif "小於" in message.content.lower():
                consecutive_count += 1
                if consecutive_count > 12:
                    channel = bot.get_channel(PROTECTED_CHANNEL_ID)
                    await channel.send("已連續猜測超過12次，強制停止循環。")
                    consecutive_count = 0
                    return
                await asyncio.sleep(1)
                min_number = current_guess
                current_guess = (min_number + max_number) // 2
                await message.channel.send(f"SN!猜數字 {current_guess}")

TOKEN = os.getenv("Discord_TOKEN")
bot.run(TOKEN)
