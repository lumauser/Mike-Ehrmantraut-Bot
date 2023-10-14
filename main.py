import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from webserver import keep_alive
import os
from commands import setup_commands

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is up and ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

setup_commands(bot)  # Set up commands using the function from commands.py

keep_alive()
bot.run(BOT_TOKEN)