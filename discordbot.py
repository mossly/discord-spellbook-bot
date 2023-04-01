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
async def send_request(message_content, reply_to, SCALE_AUTH_TOKEN, SCALE_AUTH_URL):
    data = {
        "input": {
            "previous_response": str(reply_to),
            "user_message": str(message_content).lower()
        }
    }

    headers = {"Authorization": "Basic "+SCALE_AUTH_TOKEN}

    response = requests.post(
        SCALE_AUTH_URL,
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
        await message.add_reaction('👀')
        
        reply_to = None
        if message.reference and message.reference.cached_message.author == bot.user:
            # User is replying to a bot message
            reply_to = message.reference.cached_message.content
        
        if message.content.endswith("-c"):
            SCALEAUTHTOKEN = os.getenv("SCALE_AUTH_TOKEN_MODE_C")
            SCALEAUTHURL = os.getenv("SCALE_AUTH_URL_MODE_C")
        else:
            SCALEAUTHTOKEN = os.getenv("SCALE_AUTH_TOKEN")
            SCALEAUTHURL = os.getenv("SCALE_AUTH_URL")
        
        async with message.channel.typing():
            response = await send_request(message.content, reply_to, SCALEAUTHTOKEN, SCALEAUTHURL)
            
            if response.status_code == 200:
                await message.reply(embed=discord.Embed(title="", description="response.json()['output'].strip()", color=0x32A956))
            else:
                await message.reply(f'x_x \n sorry {message.author.mention} ~ my brain is fried ~ try again later...')

BOTAPITOKEN  = os.getenv("BOT_API_TOKEN")

# Run the bot
bot.run(BOTAPITOKEN)
