from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
import asyncio

import youtube_dl
musics = {}
ytdl = youtube_dl.YoutubeDL()


load_dotenv(dotenv_path="config")

intents = discord.Intents.all()
prefix = "!"
bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.event
async def on_ready():
    print("Le bot est prêt !")

@bot.event
async def on_message(message):
    if message.content == "???":
        await message.channel.send("????")
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):

    latency = bot.latency
    await ctx.send(latency)

@bot.command()
async def echo(ctx, *, content:str):
    await ctx.send(content)

@bot.command(name="dolphin")
async def dolphin(ctx):
    await ctx.channel.send("Very cute picture of a dolphin", file=discord.File('dolphin.png'))

@bot.command(name="waf")
async def waf(ctx):
    await ctx.channel.send(f"Good boy {ctx.author.name} !")

@bot.command(name="shutup")
async def shutup(ctx, arg):
    if arg == "flipper":
        await ctx.channel.send("ok bye", file=discord.File('flipper.jpg'))
    elif arg == "doggy":
        await ctx.channel.send("ok waf", file=discord.File('dog.jpeg'))

def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)

class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command(name="play")
async def play(ctx):
    print("play")
    url = 'https://www.youtube.com/watch?v=WFf_tt4xZFA'
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"Je lance : {video.url}")
        play_song(client, musics[ctx.guild], video)

@bot.command(name="stop")
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []


@bot.command(name="cat")
async def dolphin(ctx):
    await ctx.channel.send("Very cute picture of a cat", file=discord.File('cat.jpg'))

@bot.command(name="redpanda")
async def dolphin(ctx):
    await ctx.channel.send("Very cute picture of a red panda", file=discord.File('pandaroux.jpg'))

bot.run(os.getenv("TOKEN"))
