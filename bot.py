##
## EPITECH PROJECT, 2022
## DiscordBotjam
## File description:
## Create a BOT on the theme of ???
##

from discord import *

@client.event

async def on_message(message):
    if (message.content == "Christmas"):
        print("Tree !")