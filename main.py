import discord
from discord import app_commands
from discord.ext import commands
from discord import Embed
from dotenv import load_dotenv
import os
import random
from webserver import keep_alive

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


@bot.tree.command(name="hello", description="Says `Hello`")
async def hello(interaction: discord.Interaction):
  await interaction.response.send_message(
      f"Hey {interaction.user.mention}! This is a slash command!",
      ephemeral=True)


# True = only seen by user
@bot.tree.command(name="say", description="Tell me something to say")
@app_commands.describe(arg="What should I say?")
async def say(interaction: discord.Interaction, arg: str):
  await interaction.response.send_message(
      f"{interaction.user.name} said: '{arg}'")


@bot.tree.command(name="coinflip", description="Flip a coin")
async def coinflip(interaction: discord.Interaction):
  outcome = random.choice(["Heads 🪙", "Tails 🪙"])

  embed = Embed(title="Coin Flip Result:", color=discord.Color.blue())
  embed.add_field(name="Outcome:", value=outcome, inline=False)

  await interaction.response.send_message(embed=embed)

#Implement a only mod/admin feature
@bot.tree.command(name="clear",
                  description="Clears bot messages from this bot")
async def clear(interaction: discord.Interaction):
  bot_messages = []

  async for message in interaction.channel.history(limit=None):
    if message.author == bot.user:
      bot_messages.append(message)

  if bot_messages:
    await interaction.channel.delete_messages(bot_messages)
    await interaction.response.send_message("Bot messages cleared!",
                                            ephemeral=True)
  else:
    await interaction.response.send_message("No bot messages to clear.",
                                            ephemeral=True)


keep_alive()
bot.run(BOT_TOKEN)
