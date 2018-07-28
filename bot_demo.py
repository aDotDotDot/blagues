#!/usr/bin/python3
# coding: utf8
import discord
import asyncio
import random
import re
import json
import sys
import subprocess
from parser import Blagues
# Token
with open("token.json", "r") as f : token = json.loads(f.read())
prefixe = "µ"
client = discord.Client()
blagues = Blagues()
@client.event
async def on_ready():
    print("Bot ready")

@client.event
async def on_message(message):  # Dès qu'il y a un message
    global blagues
    if message.content.startswith(prefixe + "blague"):
        try:            
            for ligne in blagues.get_random()["content"]:
                await client.send_message(message.channel, ligne)
        except Exception as ex:
            await client.send_message(message.channel, "```python\n" + str(ex) + "\n```")
    elif message.content.startswith(prefixe + "total"):
        try:
            await client.send_message(message.channel, "Je dispose de " + str(blagues.get_total()) + " blagues !")
        except Exception as ex:
            await client.send_message(message.channel, "```python\n" + str(ex) + "\n```")

client.run(token['token'])