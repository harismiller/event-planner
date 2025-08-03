import os
from dotenv import load_dotenv
import logging

import discord
from discord.ext import tasks,commands

import events
from reservations import ensure_reservation_file_exists, load_reservations

## Load environment file
load_dotenv()
app_id = int(os.getenv("APP_ID"))
discord_token = os.getenv("DISCORD_TOKEN")
public_key = os.getenv("PUBLIC_KEY")

event_text_channel = int(os.getenv("EVENT_TEXT_CHANNEL"))

ensure_reservation_file_exists()
load_reservations()

## Setup logging
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info("Starting bot...")

## App setup

description = '''App to handle event scheduling.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', description=description, intents=intents)

_events = events.Events(bot,logger,event_text_channel)

bot.run(discord_token)
# print(f"App ID: {app_id}")
# print(f"Discord Token: {discord_token}")
# print(f"Public Key: {public_key}")
