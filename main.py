# Imports
import discord
from discord.ext import commands

import json

import os
from music_cog import MusicCog

# Protecting token
if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": ""}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

print(configData["Token"])
token = configData["Token"]

# Inicializando bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

ffmpeg_options = {"options": "-vn"}
songs = []


@bot.event
async def on_ready():
    print("Bom dia!")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commandos atualizados")
    except Exception as e:
        print(e)

    # Create an instance of MusicCog and pass the bot instance to it
    music_cog = MusicCog(bot)
    # Add the MusicCog instance to the bot
    await bot.add_cog(music_cog)


# Roda o bot
bot.run(token)

