import requests, threading

import requests, asyncio
import os
from dotenv import load_dotenv


load_dotenv()
secret = os.getenv("GPT_SECRET")


def run_gpt(question):
    url = "https://api.openai.com/v1/chat/completions"

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "temperature": 0.7
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {secret}'
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    response = response.json()
    print(response)
    if(response['choices'][0]['message']['content']):
        return response['choices'][0]['message']['content']
    return "Sorry! Our server is too busy. Try Again After Sometime."


async def send_message(thread, data, ctx):
    await thread.send(f"Hey {ctx.author.mention},\n\n{data}")


class GetResponse:
    def __init__(self, question, thread, ctx):
        self.question = question
        self.thread = thread
        self.ctx = ctx

    async def run(self):
        response = run_gpt(self.question)
        await send_message(self.thread, response, self.ctx)
        


async def get_chat_gpt_response(question, thread, ctx):
    chat_gpt = GetResponse(question, thread, ctx)
    asyncio.create_task(chat_gpt.run())