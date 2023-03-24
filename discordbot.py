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
async def send_request(message_content, reply_to):
    data = {
        "input": {
            "previous_response": str(reply_to),
            "user_message": str(message_content).lower()
        }
    }

    SCALEAUTHTOKEN = os.getenv("SCALE_AUTH_TOKEN")
    SCALEAUTHURL = os.getenv("SCALE_AUTH_URL")

    headers = {"Authorization": "Basic "+SCALEAUTHTOKEN}

    response = requests.post(
        SCALEAUTHURL,
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

    if bot.user in message.mentions:
    
        reply_to = None
        if message.reference and message.reference.cached_message.author == bot.user:
            # User is replying to a bot message
            reply_to = message.reference.cached_message.content
        
        response = await send_request(message.content, reply_to=reply_to)
        
        if response.status_code == 200:
            await message.reply(response.json()['output'].strip())
        else:
            await message.reply(f'x_x sorry {message.author.mention}, something went wrong.')

BOTAPITOKEN  = os.getenv("BOT_API_TOKEN")

# Run the bot
bot.run(BOTAPITOKEN)