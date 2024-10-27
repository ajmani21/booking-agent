import traceback
import chainlit as cl
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from prompts import prompt
from tools import (
    general_availability_checker,
    avilability_checker,
    appointment_booker,
)
from dotenv import load_dotenv
from datetime import date
import asyncio


load_dotenv()

llm = OpenAI(model="gpt-4o", request_timeout=30.0)

tools = [general_availability_checker, avilability_checker, appointment_booker]

agent = ReActAgent.from_tools(
    tools,
    llm=llm,
    max_iterations=20,
    verbose=True,
    context=prompt.format(
        today_date=date.today().strftime("%Y-%m-%d"),
        weekday=date.today().strftime("%A"),
    ),
)


@cl.on_message
async def main(message):
    retries = 0

    while retries < 3:
        try:
            user_input = message.content
            result = await asyncio.to_thread(agent.chat, user_input)
            await cl.Message(content=result).send()
            break
        except Exception as e:
            print(traceback.format_exc())
            retries += 1
            await cl.Message(content=f"Error occurred, retry #{retries}: {e}").send()

    if retries >= 3:
        await cl.Message(
            content="Unable to process your request. Please try again later."
        ).send()
