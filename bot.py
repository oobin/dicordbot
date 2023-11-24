import os
from dotenv import load_dotenv
import discord
from discord.ext import commands


def main():
    load_dotenv()
    client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
    
    @client.event
    async def on_ready():
        print(f"{client.user.name} has connected to Discord.")

    @client.command()
    async def ping(ctx):
        await ctx.send("Pong!")

    client.run(os.getenv("DISCORD_TOKEN"))

if __name__ == '__main__':
    main()