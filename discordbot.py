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
        start_time = time.time()
        temp_message = await message.reply(embed=discord.Embed(title="", description="...generating reply...", color=0xFDDA0D).set_footer(text=""))
        
        reply_to = None
        if message.reference and message.reference.cached_message.author == bot.user:
            # User is replying to a bot message
            reply_to = message.reference.cached_message.content
        
        if message.content.endswith("-c"):
            SCALEAUTHTOKEN = os.getenv("SCALE_AUTH_TOKEN_MODE_C")
            SCALEAUTHURL = os.getenv("SCALE_AUTH_URL_MODE_C")
            replyMode = "GPT-4 'Creative Writing Assistant'"
        elif message.content.endswith("-t"):
            SCALEAUTHTOKEN = os.getenv("SCALE_AUTH_TOKEN_MODE_T")
            SCALEAUTHURL = os.getenv("SCALE_AUTH_URL_MODE_T")
            replyMode = "GPT-3.5 Turbo 'Concise Assistant'"
        else:
            SCALEAUTHTOKEN = os.getenv("SCALE_AUTH_TOKEN")
            SCALEAUTHURL = os.getenv("SCALE_AUTH_URL")
            replyMode = "GPT-4 'Concise Assistant'"
        
        async with message.channel.typing():
            response = await send_request(message.content, reply_to, SCALEAUTHTOKEN, SCALEAUTHURL)
            await temp_message.delete()
            
            if response.status_code == 200:
                await message.reply(embed=discord.Embed(title="", description=response.json()['output'].strip(), color=0x32a956).set_footer(text=replyMode).set_footer(text=f'generated in {round(time.time() - start_time, 2)} seconds')
            else:
                await message.reply(embed=discord.Embed(title="ERROR", description="x_x", color=0xDC143C).set_footer(text="message failed to send..."))

BOTAPITOKEN  = os.getenv("BOT_API_TOKEN")

# Run the bot
bot.run(BOTAPITOKEN)
