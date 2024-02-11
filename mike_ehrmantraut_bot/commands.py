"""Commands for Mike Ehrmantraut Bot"""

import random

import requests

from discord.ext import commands
from discord import app_commands
import discord

import string
import asyncio


def setup_commands(bot: commands.Bot):
    @bot.tree.command(name="hello", description="Says `Hello`")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Hey {interaction.user.mention}!", ephemeral=False
        )

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
            if message.author == bot.user and len(bot_messages) < 15:
                bot_messages.append(message)

        if bot_messages:
            for message in bot_messages:
                await message.delete()

            await interaction.response.send_message(
                "Bot messages cleared! (Ephemeral messages will not be removed)",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "No bot messages to clear. (Ephemeral messages will not be removed)",
                ephemeral=True,
            )

    @bot.tree.command(name="f", description="F to pay respects 🫡")
    async def f(interaction: discord.Interaction):
        user_mention = f"<@{interaction.user.id}>"
        embed = discord.Embed(
            description=f"{user_mention} has paid their respects 🫡\n :regional_indicator_f: Use /f to pay respects"
        )
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="weather", description="Get weather information for a city")
    @app_commands.describe(city="Enter a city name")
    async def weather(interaction: discord.Interaction, city: str):
        city = city.title()

        base_url = "https://api.openweathermap.org/data/2.5/weather"
        API_KEY = "3ba4e0181d9cd2210a137bb648ee4fc5"

        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric",
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_desc = data["weather"][0]["description"]
            temperature_celsius = data["main"]["temp"]
            temperature_fahrenheit = (temperature_celsius * 9 / 5) + 32
            humidity = data["main"]["humidity"]

            weather_emoji = {
                "clear sky": "☀️",
                "few clouds": "🌤️",
                "scattered clouds": "🌥️",
                "broken clouds": "☁️",
                "shower rain": "🌦️",
                "rain": "🌧️",
                "thunderstorm": "⛈️",
                "snow": "❄️",
                "mist": "🌫️",
                "overcast clouds": "🌁",
            }

            emoji = weather_emoji.get(weather_desc.lower(), "🤷‍♀️")

            embed = discord.Embed(
                title=f"Weather in {city}  🌡️",
                description=f"**Condition:** {weather_desc.capitalize()} {emoji}\n"
                f"**Temperature:** {temperature_celsius}°C / {temperature_fahrenheit}°F\n"
                f"**Humidity:** {humidity}%\n"
                f"Misspelled Cities will not work\n"
                f"Weather data provided by OpenWeatherMapAPI",
                color=discord.Color.blue(),
            )

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                "Unable to fetch weather information for that city.", ephemeral=True
            )

    @bot.tree.command(name="poll", description="Create a poll")
    @app_commands.describe(question="Enter the poll question")
    async def poll(interaction: discord.Interaction, question: str):
        await interaction.response.send_message("Creating a poll...", ephemeral=True)

        poll_message = await interaction.followup.send(
            f"### @everyone :bar_chart: {question}"
        )

        thumbs_up = "👍"
        thumbs_down = "👎"
        idk = "🤷‍♀️"
        await poll_message.add_reaction(thumbs_up)
        await poll_message.add_reaction(thumbs_down)
        await poll_message.add_reaction(idk)

        await interaction.response.delete()

    @bot.tree.command(name="ping", description="Check the bot's ping")
    async def ping(interaction: discord.Interaction):
        latency = bot.latency * 1000
        formatted_latency = "{:.2f}".format(latency)

        embed = discord.Embed(
            title="Pong! :ping_pong:",
            description=f"Bot's ping is {formatted_latency}ms",
            color=discord.Color.green(),
        )

        await interaction.response.send_message(embed=embed, ephemeral=False)

    @bot.tree.command(name="hex_game", description="Convert hex to ascii")
    async def hex_game(interaction: discord.Interaction):
        ascii_string = "".join(random.choice(string.ascii_lowercase) for _ in range(4))
        hex_string = ""

        for l in ascii_string:
            hex_string += l.encode("utf-8").hex() + " "

        hex_string = hex_string.strip()

        await interaction.response.send_message(
            f"What is the ASCII string for the following hex value: `{hex_string}`"
        )

        def check_guess(message):
            return message.content.lower() == ascii_string

        try:
            await bot.wait_for("message", check=check_guess, timeout=30)
        except asyncio.TimeoutError:
            await interaction.followup.send(
                "Time's up! You didn't guess the correct ASCII string."
            )
        else:
            await interaction.followup.send(
                f"Congratulations! You guessed the correct ASCII string: {ascii_string}"
            )
