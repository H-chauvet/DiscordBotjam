from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

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

@bot.command(pass_context=True)
@bot.event
async def on_member_join(ctx, member):
    print(f'{member} has joined a server ! Welcome to this new dog :)')
    await ctx.send(f"Hello {member}! Welcome with your family ! PETS :D")

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


bot.run(os.getenv("TOKEN"))
