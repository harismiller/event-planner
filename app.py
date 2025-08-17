import os
from dotenv import load_dotenv
from datetime import timezone, timedelta

from setup_logging import setup_logger
setup_logger()
import logging

import discord
from discord.ext import tasks,commands

# from reservations import ensure_reservation_file_exists, load_reservations
from reservations import Reservation

## Load environment file
load_dotenv()
app_id = int(os.getenv("APP_ID"))
discord_token = os.getenv("DISCORD_TOKEN")
public_key = os.getenv("PUBLIC_KEY")

event_text_channel = int(os.getenv("EVENT_TEXT_CHANNEL"))

## Setup logging
logger = logging.getLogger("event_planner")

logger.debug("Starting bot...")

## Reservation setup
res = Reservation()
res.ensure_reservation_file_exists()
res.load_reservations()

## App setup
description = '''App to handle event scheduling.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

logger.debug("Setup commands...")

bot = commands.Bot(command_prefix='/', description=description, intents=intents)

logger.debug("Setup events...")
@bot.event
async def on_ready():
    for guild in bot.guilds:
        for event in await guild.fetch_scheduled_events():
            if not res.is_reservation_loaded(event.id):
                logger.debug(f"Loading reservation for event {event.name}, {event.id}")
                res.reserve_channel(
                    channel_id=event.channel.id,
                    name=event.name,
                    start=event.start_time,
                    event_id=event.id
                )
    logger.info("Synchronized existing scheduled events.")
    logger.info("App ready!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    channel_id = message.channel.id
    logger.debug(f"Message found in channel ID: {channel_id}")

    channel = bot.get_channel(channel_id)
    await channel.send(f"Response to: {message.content}")
    logger.debug(f"Sent message to channel: {channel_id}")

@bot.event
async def on_scheduled_event_create(event):
    logger.info(f"Scheduled event created: {event.name} (ID: {event.id})")
    if not event.channel:
        logger.warning("Event not tied to channel.")
        return
    
    start = event.start_time.replace(tzinfo=timezone.utc)

    res.reserve_channel(
        channel_id=event.channel.id,
        name=event.name,
        start=start,
        event_id=event.id
    )
    logger.info(f"Reserved channel {event.channel.id} for event {event.id}")

    channel = bot.get_channel(event_text_channel)
    await channel.send(f"A new event has been created: **{event.name}**\n{event.url}")

logger.info("Running bot...")
bot.run(discord_token)