import logging

def setup_logger():
    logger = logging.getLogger("event_planner")
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')

    # file_handler = logging.FileHandler(filename='event_planner.log', encoding='utf-8', mode='w')
    # file_handler.setFormatter(formatter)
    # file_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)

    # logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    discord_logger = logging.getLogger("discord")
    discord_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    discord_handler.setFormatter(formatter)
    discord_handler.setLevel(logging.DEBUG)
    discord_logger.addHandler(discord_handler)
    logger.addHandler(discord_handler)