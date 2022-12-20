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
async def on_member_join(member):
    channel = bot.get_channel(1054397805533343746)
    await channel.send(f"Bienvenue a {member.mention} sur le serveur !\nN'hésitez pas à soutenir la spa: https://soutenir.la-spa.fr/extraordinaireP/~mon-don")

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
    await ctx.channel.send("Very cute picture of a dolphin", file=discord.File('assets/dolphin.png'))
    await playy(ctx, 'https://www.youtube.com/watch?v=MGSTRJmN2VQ')

@bot.command(name="waf")
async def waf(ctx):
    await ctx.channel.send(f"Good boy {ctx.author.name} !")

@bot.command(name="shutup")
async def shutup(ctx, arg):
    if arg == "flipper":
        await ctx.channel.send("ok bye", file=discord.File('assets/flipper.jpg'))
    elif arg == "doggy":
        await ctx.channel.send("ok waf", file=discord.File('assets/dog.jpeg'))

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

async def playy(ctx, url):
    print("play")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        play_song(client, musics[ctx.guild], video)

@bot.command(name="play")
async def play(ctx):
    await playy(ctx, 'https://www.youtube.com/watch?v=WFf_tt4xZFA')

@bot.command(name="stop")
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []


@bot.command(name="cat")
async def cat(ctx):
    await ctx.channel.send("Very cute picture of a cat", file=discord.File('assets/cat.jpg'))

@bot.command(name="redpanda")
async def redpanda(ctx):
    await ctx.channel.send("Very cute picture of a red panda", file=discord.File('assets/pandaroux.jpg'))

@bot.command(name="unicorn")
async def unicorn(ctx):
    await ctx.channel.send("Very cute picture of a unicorn", file=discord.File('assets/unicorn.jpg'))
    await playy(ctx, 'https://www.youtube.com/watch?v=wscODUIkvjA')


@bot.command(name="dragon")
async def dragon(ctx):
    await ctx.channel.send("Very cute picture of a dragon", file=discord.File('assets/dragon.jpg'))
    await playy(ctx, 'https://www.youtube.com/watch?v=Y2Qo2VBC2iA')

bot.run(os.getenv("TOKEN"))
