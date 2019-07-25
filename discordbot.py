from __future__ import unicode_literals
import discord
import logging
import ffmpeg
import mp3
import time
import asyncio
import youtube_dl
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
discord.opus.load_opus
client = commands.Bot(command_prefix='.')
client.remove_command('help')

token = 'NjAwMTUzMzE5NjEyMDg4Mzgw.XS6VMg.3gXzU6td4ecizeDqHdsjMsh62bM'

#loggingsetup
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#deflist

async def next_song():
    music_list=[]
    with open('queue.txt','r') as queue:
        for line in queue:
            music_list.append(line)
    with open('queue.txt','w+') as queue:
        for i in range(1,len(music_list)):
            queue.write(music_list[i])
    

def musician():
    with open('queue.txt','r') as queue:
        url = queue.readline()
        
        try:
            ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': "audio"+ '.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception:
            return False
    return True

#events

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_member_join(member):
    print('%s joined a guild'%(member))

@client.event    
async def on_member_remove(member):
    print('%s left a guild'%(member))

@client.event
async def on_disconnect():
    print('Bot has disconnected')

#commands
#help
@client.command(aliases=["помощь"])
async def help(ctx):
    embed = discord.Embed(title="ProjectBOT", description="Музыкальный Бот", colour=0xeee657)
    embed.add_field(name=".добавить", value="Добавляет музыку в очередь(музыка должна быть ссылкой на youtube-клип)", inline=False)
    embed.add_field(name=".старт;.начать;.проигрывать", value="Воспроизводит музыку из очереди", inline=False)
    embed.add_field(name=".помощь", value="Вызывает это сообщение", inline=False)

    await ctx.send(embed=embed)
#add_to_queue
@client.command(pass_context=True,aliases=["добавить"])
async def add_to_queue(ctx,url):
    with open('queue.txt','a+') as queue:
        queue.write(url+'\n')
#join_voice
@client.command(pass_context=True,aliases=["вход","войти","включить"])
async def join_voice(ctx):
    global vc
    voicechannel = discord.utils.get(ctx.guild.channels, name='voice_channel')
    vc = await voicechannel.connect()
#music_play
@client.command(pass_context=True,aliases=["старт","начать","проигрывать"])
async def music_play(ctx):
    while True:
        if musician():
            player = vc.play(source=discord.FFmpegPCMAudio('audio.mp3'),after = None)
            while vc.is_playing() == True:
                await asyncio.sleep(2)
            await next_song()
            await asyncio.sleep(5)
        else:
            try:
                await next_song()
                if musician():
                    pass
                else:
                    raise Exception
            except Exception:
                break
    await ctx.send("Музыка закончилась")

client.run(token)