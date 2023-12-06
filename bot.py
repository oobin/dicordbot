import os
import time

import discord
from dotenv import load_dotenv
from openai import OpenAI

# ChatGPT options
MAX_TOKENS = 512
TEMPERATURE = 0.5
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0

# limits how long the prompt can be
MAX_CONTEXT_QUESTIONS = 5
INSTRUCTIONS = "you are a german sassy panzer woman"


def split_by_n(seq, n):
    """A generator to divide a sequence into chunks of n units."""
    while seq:
        yield seq[:n]
        seq = seq[n:]


def main():
    load_dotenv()
    intents = discord.Intents.all()
    bot = discord.Client(command_prefix="!", intents=intents)
    ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    conversation = [{"role": "system", "content": INSTRUCTIONS}]

    @bot.event
    async def on_ready():
        print(f"{bot.user} has connected to Discord.")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if bot.user in message.mentions:
            async with message.channel.typing():
                if len(conversation) >= MAX_CONTEXT_QUESTIONS + 1:
                    conversation.pop(1)
                message_content = message.content.lstrip("<@0123456789> ")
                conversation.append({"role": "user", "content": message_content})
                response = ai_client.chat.completions.create(
                    model="gpt-4-1106-preview",
                    messages=conversation,
                    max_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE,
                    frequency_penalty=FREQUENCY_PENALTY,
                    presence_penalty=PRESENCE_PENALTY,
                )

                chatgpt_response = response.choices[0].message.content
                response_list = list(split_by_n(chatgpt_response, 2000))

                for entry in response_list:
                    await message.channel.send(entry)
                    time.sleep(1)

                if len(conversation) >= MAX_CONTEXT_QUESTIONS + 1:
                    conversation.pop(1)
                conversation.append(
                    {
                        "role": response.choices[0].message.role,
                        "content": response.choices[0].message.content,
                    }
                )

    if os.getenv("DEV_MODE"):
        bot.run(os.getenv("DISCORD_DEV_TOKEN"))  # type: ignore
    else:
        bot.run(os.getenv("DISCORD_TOKEN"))  # type: ignore


if __name__ == "__main__":
    main()
