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

# Event for sending Scale.AI Spellbook API requests
async def send_request(message_content):
    data = {
        "input": {
            "input": str(message_content).lower()
        }
    }

    headers = {"Authorization": "Basic clfkgvelr03h4xf1ac0zl2cd5"}

    response = requests.post(
        "https://dashboard.scale.com/spellbook/api/v2/deploy/yc63dn6",
        json=data,
        headers=headers
    )

    return response

# Event for handling messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:

        await message.channel.send(f'Hi {message.author.mention} \n'+ send_request(message.content).json()['output'].strip())
        
    if message.reference and message.reference.resolved.author == bot.user:
    
        await message.channel.send(send_request(message.content).json()['output'].strip())

TOKEN = os.getenv("BOT_API_TOKEN")

# Run the bot
bot.run(TOKEN)