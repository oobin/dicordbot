import os

import discord
from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()
    intents = discord.Intents.all()
    bot = discord.Client(command_prefix="!", intents=intents)
    ai_client = OpenAI()
    dev_mode = os.getenv("DEV_MODE")

    @bot.event
    async def on_ready():
        print(f"{bot.user} has connected to Discord.")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if bot.user in message.mentions:
            response = ai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message.content}],
                max_tokens=256,
                temperature=0.5,
                frequency_penalty=0,
                presence_penalty=0,
            )

            await message.channel.send(response.choices[0].message.content)

    if dev_mode:
        bot.run(os.getenv("DISCORD_DEV_TOKEN"))  # type: ignore
    else:
        bot.run(os.getenv("DISCORD_TOKEN"))  # type: ignore


if __name__ == "__main__":
    main()
