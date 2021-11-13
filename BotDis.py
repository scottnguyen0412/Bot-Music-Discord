import discord
import os
from discord import player
from discord import guild
from discord import channel
from discord import voice_client
from discord import message
from discord.client import Client
from discord.enums import Status
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
import emoji
from youtube_dl import YoutubeDL
from emoji import emojize
import youtube_dl
from discord.voice_client import VoiceClient
from random import choice
import asyncio
#load_dotenv()
client = commands.Bot(command_prefix='-')  # prefix our commands with '~'
players = {}
#welcome new member
#@client.event 
#async def Welcome(memeber):
#   print(emojize(f'{memeber}Hii! Have a nice day :thumbs_up'))
# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in

#bot join channel
@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

# command to play sound from a youtube URL
@client.command(name='play', help='This command play to music')
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('Bot is playing')
# check if the bot is already playing
    else:
        await ctx.send("Bot is already playing")
        return

# command to resume voice if it is paused
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')

# command to pause voice if it is playing
@client.command(name='pause', help='This command to pause music')
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')

# command to stop voice
@client.command(name ='stop', help ='this is used to stop music')
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        await ctx.send('Stopping...')

# command to clear channel messages
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages have been cleared")

#chatbot
@client.command()
async def Hii(ctx):
    await ctx.send(emojize('Hello dudee :smiling_face:'))

@client.event  # check if bot is ready
async def on_ready():
    print('-------------')
    print('Bot is online')
    print('-------------')

#check Room Ping ms 
@client.command()
async def ping(ctx):
    await ctx.send(f'Ping of Room {round(client.latency * 1000)}ms')
client.run('Your token discord here')
