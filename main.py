import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv


load_dotenv(".env")
token = os.getenv("bot-token")

client = commands.Bot(command_prefix= "$", intents = discord.Intents.all())

@client.event
async def on_ready():
    print("UDP is online.")


async def load():
    await client.load_extension("cogs.unix_commands")

async def main():
    async with client:
        await load()
        await client.start(token)


asyncio.run(main())
