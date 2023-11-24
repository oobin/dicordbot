import os
from dotenv import load_dotenv
import discord
import openai


def main():
    load_dotenv()
    bot = discord.Client(command_prefix="!", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f"{bot.user.name} has connected to Discord.")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if bot.user in message.mentions:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message.content}],
                max_tokens=256,
                temperature=0.2,
                frequency_penalty=0,
                presence_penalty=0,
            )

            content = response.choices[0].message.content
            chunk_size = 2000
            chunks = [
                content[i : i + chunk_size] for i in range(0, len(content), chunk_size)
            ]

            for chunk in chunks:
                await message.channel.send(chunk)

    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
