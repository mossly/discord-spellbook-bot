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
            reply_to = encode_caesar_cipher(message.reference.cached_message.content)
        
        async with message.channel.typing():
            response = await send_request(encode_caesar_cipher(message.content), reply_to=reply_to)

            if response.status_code == 200:
                await message.add_reaction('👀')
                await message.reply(decode_caesar_cipher(response.json()['output'].strip()))
            else:
                await message.add_reaction('👀')
                await message.reply(f'x_x \n sorry {message.author.mention} ~ my brain is fried ~ try again later...')
                
async def encode_caesar_cipher(text, shift=3):
    result = ""

    for char in text:
        if char.isalpha():
            shift_amount = 65 if char.isupper() else 97
            result += chr(((ord(char) - shift_amount + shift) % 26) + shift_amount)
        else:
            result += char

    return result

async def decode_caesar_cipher(text, shift=3):
    return encode_caesar_cipher(text, -shift)
                
BOTAPITOKEN  = os.getenv("BOT_API_TOKEN")

# Run the bot
bot.run(BOTAPITOKEN)
