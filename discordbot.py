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
    # Check if the message was sent by the bot itself
    if message.author == bot.user:
        return

    if '@MS-DOS-LY' in message.content:

        response = await send_request(message.content)
        
        if response.status_code == 200:
            await message.channel.send(f'Hi {message.author.mention} \n'+ response.json()['output'].strip())
        else:
            await message.channel.send(f'Sorry {message.author.mention}, something went wrong.')    
        
    if message.reference and message.reference.resolved.author == bot.user:
    
        response = await send_request(message.content)
        
        if response.status_code == 200:
            await message.channel.send(response.json()['output'].strip())
        else:
            await message.channel.send(f'Sorry {message.author.mention}, something went wrong.') 

TOKEN = os.getenv("BOT_API_TOKEN")

# Run the bot
bot.run(TOKEN)