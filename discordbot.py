import discord
from discord.ext import commands

# Create a new bot instance
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix="!", intents=intents)

# Load your bot token from a file or an environment variable
with open("bot_token.txt", "r") as file:
    TOKEN = file.read().strip()

# Event for when the bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

# Event for handling messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "hello":
        response = "Hello!"
        await message.channel.send(response)

    await bot.process_commands(message)

# Run the bot
bot.run(BOT_API_TOKEN)