from discord.ext import commands
import discord

intents = discord.Intents.all()
prefix = "!"
bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.event
async def on_ready():
    print("Le bot est prêt !")

@bot.event
async def on_message(message):
    if message.content == "Christmas":
        await message.channel.send("Tree :D")
    if message.content == "Santa":
        await message.channel.send("Claus :D")
    await bot.process_commands(message)


@bot.command()
async def ping(ctx):

    latency = bot.latency
    await ctx.send(latency)

@bot.command()
async def echo(ctx, *, content:str):
    await ctx.send(content)


bot.run('')