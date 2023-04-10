import discord, time
import requests, asyncio, os
from dotenv import load_dotenv

from discord import Client, Intents
from chatgpt import get_chat_gpt_response

intents = Intents.default()
intents.members = True
intents.messages = True
bot = discord.Bot(intents=discord.Intents.all())

load_dotenv()


@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')


@bot.command(description="Sends the bot's latency.", name="ping") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@bot.command(description="Defination Finder app", name="def")
async def defination(ctx, word : str):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'

    response = requests.get(url)
    res = response.json()

    try:
        list = res
        meanings = ''
        counter = 1

        for item in list:
            for meaning in item['meanings']:
                for definition in meaning['definitions']:
                    if counter <= 5:
                        meanings += f'{counter}. {definition["definition"]}\n'
                    counter += 1

        await ctx.respond(f'👉   {meanings}\n @ That\'s all I know, Enjoy 🍫 ')

    except IndexError:
        await ctx.respond('Not Found')
        return


@bot.command(description="Synonym Finder app", name="syn")
async def synonyms(ctx, word: str):

    if word == 'krystalina' or word == 'krystal':
        await message.reply('The most Beautiful thing in the world')
    else:
        url = f'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=dict.1.1.20220320T122645Z.2e793b96fb819f5d.2fb7439d47ea532e033a2c866b48b2fa3f4acb94&lang=en-en&text={word}'

        response = requests.get(url)
        res = response.json()
        try:
            list = res['def'][0]['tr']
        except IndexError:
            await ctx.respond('Not Found')
            return

        content = ''
        counter = 1

        for item in list:
            if counter <= 5:
                content += f'{counter}. {item["text"]}, '
            counter += 1

        content = content.rstrip(', ')
        await ctx.respond(f'👉   {content}\n That\'s all I know, Enjoy 🍫 ')


@bot.command(description="ChatGPT", name="chat")
async def chat(ctx, question : str):
    message = await ctx.channel.send(f"{ctx.author.mention} asked: {question}")
    await ctx.respond(f"I am processing your question. Please wait.")
    thread = await message.create_thread(name=f"{question}", auto_archive_duration=60)
    asyncio.create_task(get_chat_gpt_response(question, thread, ctx))


my_secret = os.getenv('DISCORD_SECRET')
bot.run(my_secret)


