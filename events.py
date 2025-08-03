import reservations
from reservations import reserve_channel
from datetime import timezone, timedelta

class Events:
    def __init__(self, bot, logger, event_text_channel):
        self.bot = bot
        self.logger = logger
        self.event_text_channel = event_text_channel

        @bot.event
        async def on_ready():
            for guild in bot.guilds:
                for event in await guild.fetch_scheduled_events():
                    if event.channel:
                        reserve_channel(
                            channel_id=event.channel.id,
                            start=event.start_time,
                            end=event.end_time,
                            event_id=event.id
                        )
            logger.info("Synchronized existing scheduled events.")
            logger.info("App ready!")

        @bot.event
        async def on_message(message):
            if message.author.bot:
                return
            
            channel_id = message.channel.id
            logger.info(f"Message found in channel ID: {channel_id}")

            channel = bot.get_channel(channel_id)
            await channel.send(f"Response to: {message.content}")
            logger.info(f"Sent message to channel: {channel_id}")

        @bot.event
        async def on_scheduled_event_create(event):
            logger.info(f"Scheduled event created: {event.name} (ID: {event.id})")
            if not event.channel:
                logger.warning("Event not tied to channel.")
                return
            
            start = event.start_time.replace(tzinfo=timezone.utc)
            # end = event.end_time.replace(tzinfo=timezone.utc)
            if event.end_time:
                end = event.end_time.replace(tzinfo=timezone.utc)
            else:
                # Default to 1 hour after start if end_time is missing
                end = start + timedelta(hours=1)

            reserve_channel(
                channel_id=event.channel.id,
                start=start,
                end=end,
                event_id=event.id
            )
            logger.info(f"Reserved channel {event.channel.id} for event {event.id}")

            channel = bot.get_channel(self.event_text_channel)
            await channel.send(f"A new event has been created: **{event.name}**\n{event.url}")
    
    def set_event_channel(self,channel_id):
        self.event_text_channel = channel_id
