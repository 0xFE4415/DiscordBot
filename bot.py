import discord
from discord.ext import commands
import time
import re

# read token from file
with open("token", "r") as f:
    TOKEN = f.read().strip()

IMAGE_PATH = "meme.png"  # hardcoded image

intents = discord.Intents.default()
intents.message_content = True  # sees message content

bot = commands.Bot(command_prefix="!", intents=intents)

LAST_SENT = {}
RATE_LIMIT_SECONDS = 3

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} — ready.")

@bot.event
async def on_message(message):
    ch_id = message.channel.id
    now = time.time()
    last = LAST_SENT.get(ch_id, 0)

    if message.author.bot:
        return
    
    if now - last < RATE_LIMIT_SECONDS:
        return

    # Check autism in messages
    if re.search(r"(autis\w*|autyz\w*)", message.content, re.IGNORECASE):
        LAST_SENT[ch_id] = now
        try:
            await message.reply("Czy ktoś powiedział: autyzm??😳😳")
            print(f"Sent response to channel {ch_id}")
        except Exception as e:
            print("Failed to send:", e)
        
    # Check mentions
    if bot.user in message.mentions or message.mention_everyone:
        
        # Ignore replies to the bot's messages
        if message.reference and message.reference.resolved:
            if message.reference.resolved.author == bot.user:
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
