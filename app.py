import os
from dotenv import load_dotenv

# import discord
# from discord.ext import commands

load_dotenv()
app_id = os.getenv("APP_ID")
discord_token = os.getenv("DISCORD_TOKEN")
public_key = os.getenv("PUBLIC_KEY")

# print(f"App ID: {app_id}")
# print(f"Discord Token: {discord_token}")
# print(f"Public Key: {public_key}")
