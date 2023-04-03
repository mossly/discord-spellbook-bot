import requests
import os
import time
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

async def send_request(message_author, message_content, reference_author, reference_message, SCALE_AUTH_TOKEN, SCALE_AUTH_URL):
    data = {
        "input": {
            "message_author": str(message_author).lower(),
            "reference_author": str(reference_author).lower(),
            "reference_mesage": str(reference_message).lower().replace("<@1088294375253082223>", ""),
            "message_content": str(message_content).lower().replace("<@1088294375253082223>", "")
        }
    }

    headers = {"Authorization": "Basic "+SCALE_AUTH_TOKEN}

    response = requests.post(
        SCALE_AUTH_URL,
        json=data,
        headers=headers
    )

    return response

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        start_time = time.time()
        temp_message = await message.reply(embed=discord.Embed(title="", description="...reading request...", color=0xFDDA0D).set_footer(text=""))
        
        reference_author = None
        reference_message = None
        if message.reference and message.reference.cached_message.author == bot.user:
            await temp_message.delete()
            temp_message = await message.reply(embed=discord.Embed(title="", description="...fetching bot reference...", color=0xFDDA0D).set_footer(text=""))
            reference_message = message.reference.cached_message.embeds[0].description
            reference_author = "MS-DOS-LY"
            
        elif message.reference:
            await temp_message.delete()
            temp_message = await message.reply(embed=discord.Embed(title="", description="...fetching user reference...", color=0xFDDA0D).set_footer(text=""))
            reference_message = message.reference.cached_message.content
            reference_author = message.reference.cached_message.author.name
            
        suffixes = {
            "-v": ("scale_auth_token_mode_v", "scale_auth_url_mode_v", "gpt-4 'verbose'")
            "-t": ("scale_auth_token_mode_t", "scale_auth_url_mode_t", "gpt-3.5 turbo 'concise'")
            "-c": ("scale_auth_token_mode_c", "scale_auth_url_mode_c", "gpt-4 'creative'"),
        }

        scaleauthtoken, scaleauthurl, replymode = suffixes.get(message.content[-2:], ("scale_auth_token", "scale_auth_url", "gpt-4 'concise'"))

        scaleauthtoken = os.getenv(scaleauthtoken)
        scaleauthurl = os.getenv(scaleauthurl)
        
        await temp_message.delete()
        temp_message = await message.reply(embed=discord.Embed(title="", description="...generating reply...", color=0xFDDA0D).set_footer(text=""))
        response = await send_request(message.author.name, message.content, reference_author, reference_message, SCALEAUTHTOKEN, SCALEAUTHURL)
        await temp_message.delete()

        if response.status_code == 200:
            await message.reply(embed=discord.Embed(title="", description=response.json()['output'].strip(), color=0x32a956).set_footer(text=f'{replyMode} | generated in {round(time.time() - start_time, 2)} seconds'))
        else:
            await message.reply(embed=discord.Embed(title="ERROR", description="x_x", color=0xDC143C).set_footer(text="message failed to send..."))

BOTAPITOKEN  = os.getenv("BOT_API_TOKEN")

bot.run(BOTAPITOKEN)
