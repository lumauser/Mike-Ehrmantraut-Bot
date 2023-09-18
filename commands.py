import discord
from discord.ext import commands
from discord import app_commands
import random
from discord import Embed
import requests

def setup_commands(bot: commands.Bot):
    @bot.tree.command(name="hello", description="Says `Hello`")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Hey {interaction.user.mention}!",
            ephemeral=False)

    @bot.tree.command(name="say", description="Tell me something to say")
    @app_commands.describe(say="What should I say?")
    async def say(interaction: discord.Interaction, say: str):
        user_mention = f"<@{interaction.user.id}>"
        await interaction.response.send_message(
            f"{user_mention} said: '{say}'")
      
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

            await interaction.response.send_message("Bot messages cleared! (Ephemeral messages will not be removed)",
                                                    ephemeral=True)
        else:
            await interaction.response.send_message("No bot messages to clear. (Ephemeral messages will not be removed)",
                                                    ephemeral=True)
    @bot.tree.command(name="f", description="F to pay respects 🫡")
    async def f(interaction: discord.Interaction):
      user_mention = f"<@{interaction.user.id}>"
      embed = discord.Embed(description=f"{user_mention} has paid their respects 🫡\n :regional_indicator_f: Use /f to pay respects")
      await interaction.response.send_message(embed=embed)
    
    @bot.tree.command(name="weather", description="Get weather information for a city")
    @app_commands.describe(city="Enter a city name")
    async def weather(interaction: discord.Interaction, city: str):
      city = city.title()

      base_url = 'https://api.openweathermap.org/data/2.5/weather'
      API_KEY = '3ba4e0181d9cd2210a137bb648ee4fc5'

      params = {
          'q': city,      
          'appid': API_KEY,
          'units': 'metric',
      }

      response = requests.get(base_url, params=params)
      data = response.json()

      if response.status_code == 200:
          weather_desc = data['weather'][0]['description']
          temperature_celsius = data['main']['temp']
          temperature_fahrenheit = (temperature_celsius * 9/5) + 32
          humidity = data['main']['humidity']

          weather_emoji = {
              'clear sky': '☀️',
              'few clouds': '🌤️',
              'scattered clouds': '🌥️',
              'broken clouds': '☁️',
              'shower rain': '🌦️',
              'rain': '🌧️',
              'thunderstorm': '⛈️',
              'snow': '❄️',
              'mist': '🌫️',
              'overcast clouds': '🌁'
          }

          emoji = weather_emoji.get(weather_desc.lower(), '🤷‍♀️')

          embed = discord.Embed(
            title=f"Weather in {city}  🌡️",
            description=f"**Condition:** {weather_desc.capitalize()} {emoji}\n"
                        f"**Temperature:** {temperature_celsius}°C / {temperature_fahrenheit}°F\n"
                        f"**Humidity:** {humidity}%\n"
                        f"Misspelled Cities will not work\n"
                        f"Weather data provided by OpenWeatherMapAPI",
            color=discord.Color.blue()
        )

          await interaction.response.send_message(embed=embed)
      else:
          await interaction.response.send_message("Unable to fetch weather information for that city.", ephemeral=True) 