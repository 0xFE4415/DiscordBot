import time
from pathlib import Path

import discord
from discord.ext import commands

from text_checks import is_autism_variant

IMAGE_PATH = "meme.png"
LAST_SENT: dict[int, float] = {}
RATE_LIMIT_SECONDS = 3

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user} — ready.")


@bot.event
async def on_message(message: discord.Message) -> None:
    ch_id = message.channel.id
    now = time.time()
    last = LAST_SENT.get(ch_id, 0)

    if message.author.bot:
        return

    if now - last < RATE_LIMIT_SECONDS:
        return

    # Check autism in messages
    if is_autism_variant(message.content):
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
            if getattr(message.reference.resolved, "author", None) == bot.user:
                return

        LAST_SENT[ch_id] = now
        try:
            await message.reply(file=discord.File(IMAGE_PATH))
            print(f"Sent image to channel {ch_id}")
        except Exception as e:
            print("Failed to send image:", e)

    await bot.process_commands(message)


def main() -> None:
    token = Path("token").read_text().strip()
    bot.run(token)
