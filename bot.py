import os
import sys
import asyncio
import platform
import discord
from discord.ext import commands


operating_system = platform.system()
BOT_TOKEN = os.environ.get("DOJO_BOT_REVAMPED")

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix = '-', intents = intents)


# Function to load cogs
async def load_cogs():
    await bot.load_extension('voice_channels_cog')
    print("- voice_channels_cog")
    await bot.load_extension('music_cog')
    print("- music_cog")


# Initialization
@bot.event
async def on_ready():
    print("\n=====================================================")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"Running on {operating_system} using {os.environ['YT_SERVICE']}")
    print("-----------------------------------------------------")
    print("Loaded Cogs:")
    # Call function to add cogs
    await load_cogs()
    print("=====================================================")

if len(sys.argv)==2:
    if sys.argv[1].upper() == 'YTDL':
        os.environ['YT_SERVICE'] = 'YTDL'
    else:
        os.environ['YT_SERVICE'] = 'PYTUBE'
else:
    os.environ['YT_SERVICE'] = 'PYTUBE'


bot.run(BOT_TOKEN)