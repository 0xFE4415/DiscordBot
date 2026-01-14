import time
import unicodedata
from pathlib import Path

import discord
from discord.ext import commands
from rapidfuzz import fuzz, process

IMAGE_PATH = "meme.png"  # hardcoded image

intents = discord.Intents.default()
intents.message_content = True  # sees message content

bot = commands.Bot(command_prefix="!", intents=intents)

LAST_SENT: dict[int, float] = {}
RATE_LIMIT_SECONDS = 3


def normalize_text(text: str) -> str:
    cyrillic_to_human_letter_map = {
        "а": "a",
        "А": "A",
        "в": "b",
        "В": "B",
        "е": "e",
        "Е": "E",
        "к": "k",
        "К": "K",
        "м": "m",
        "М": "M",
        "н": "h",
        "Н": "H",
        "о": "o",
        "О": "O",
        "р": "p",
        "Р": "P",
        "с": "c",
        "С": "C",
        "т": "t",
        "Т": "T",
        "у": "y",
        "У": "Y",
        "х": "x",
        "Х": "X",
        "і": "i",
        "І": "I",
        "α": "a",
        "ο": "o",
        "ρ": "p",
        "ν": "v",
        "и": "n",
        "µ": "u",
        "¡": "i",
        "+": "t",
        "|": "i",
    }

    translation_table = str.maketrans(cyrillic_to_human_letter_map)
    text = text.translate(translation_table)

    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def is_autism_variant(text: str) -> bool:

    normalized = normalize_text(text)

    cleaned = "".join(c for c in normalized if c.isalpha()).lower()
    if len(cleaned) < 5:
        return False
    targets = ["autism", "autyzm", "autistic", "lubiepociagi"]

    result = process.extractOne(cleaned, targets, scorer=fuzz.partial_ratio)
    return result is not None and result[1] >= 92


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
