import requests
import os
import discord
from discord.ext import commands

# Create a new bot instance
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix="!", intents=intents)

# Event for when the bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

# Event for handling messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print("message received")

    data = {
        "input": {
        "name": "John",
        "message": "Hello"
        }
    }
    
    print("data created")
    
    headers = {"Authorization":"Basic clfkgvelr03h4xf1ac0zl2cd5"}
    
    response = requests.post("https://dashboard.scale.com/spellbook/api/v2/deploy/yc63dn6", json=data, headers=headers)
    
    print("request posted")
    
    await message.channel.send(str(response))
    
    print("message sent")

    await bot.process_commands(message)

TOKEN = os.getenv("BOT_API_TOKEN")

# Run the bot
bot.run(TOKEN)