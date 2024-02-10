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
    await bot.change_presence(activity=discord.Game(name="Helpin My Town"))
    print("Bot is up and ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    
    num_servers = len(bot.guilds)
    print(f"This bot is in {num_servers} servers!")
  
setup_commands(bot)

keep_alive()
bot.run(BOT_TOKEN)