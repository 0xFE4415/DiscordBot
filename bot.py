import discord
from discord.ext import commands
import time

# read token from file
with open("token", "r") as f:
    TOKEN = f.read().strip()

IMAGE_PATH = "meme.png"  # hardcoded image

intents = discord.Intents.default()
intents.messages = True  # enough for mentions

bot = commands.Bot(command_prefix="!", intents=intents)

LAST_SENT = {}
RATE_LIMIT_SECONDS = 5

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} — ready.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Check if bot is mentioned, or @everyone/@here
    if bot.user in message.mentions or message.mention_everyone:
        ch_id = message.channel.id
        now = time.time()
        last = LAST_SENT.get(ch_id, 0)
        if now - last < RATE_LIMIT_SECONDS:
            return
        LAST_SENT[ch_id] = now

        try:
            await message.channel.send(file=discord.File(IMAGE_PATH))
            print(f"Sent image to channel {ch_id}")
        except Exception as e:
            print("Failed to send image:", e)

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
