import discord
from discord.ext import commands
from discord import app_commands
import random
from discord import Embed

def setup_commands(bot: commands.Bot):
    @bot.tree.command(name="hello", description="Says `Hello`")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Hey {interaction.user.mention}!",
            ephemeral=True)

    @bot.tree.command(name="say", description="Tell me something to say")
    @app_commands.describe(arg="What should I say?")
    async def say(interaction: discord.Interaction, arg: str):
        await interaction.response.send_message(
            f"{interaction.user.name} said: '{arg}'")

    @bot.tree.command(name="coinflip", description="Flip a coin")
    async def coinflip(interaction: discord.Interaction):
        outcome = random.choice(["Heads 🪙", "Tails 🪙"])

        embed = discord.Embed(title="Coin Flip Result:", color=discord.Color.blue())
        embed.add_field(name="Outcome:", value=outcome, inline=False)

        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="clear", description="Clears bot messages from this bot")
    async def clear(interaction: discord.Interaction):
        bot_messages = []

        async for message in interaction.channel.history(limit=None):
            if message.author == bot.user:
                bot_messages.append(message)

        if bot_messages:
            for message in bot_messages:
                await message.delete()

            await interaction.response.send_message("Bot messages cleared! (Ephemeral messages will not be removed)",
                                                    ephemeral=True)
        else:
            await interaction.response.send_message("No bot messages to clear. (Ephemeral messages will not be removed)",
                                                    ephemeral=True)