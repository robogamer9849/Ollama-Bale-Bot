import ollama
import asyncio
import logging
from bale import *
import re
from pathlib import Path

list = ''


models_INT= len(ollama.list()['models'])
uModel = 'gemma:2b'
for i in range(0, models_INT):
   list = list + '\n' + str(i + 1) + '.' +  ollama.list()['models'][i]['name']

model_options = {

}

for i in range(0, models_INT):
    model_options['/' + ollama.list()['models'][i]['name']] = ollama.list()['models'][i]['name']

logger = logging.getLogger()
logging.basicConfig(filename=Path(__file__).parent.resolve()/'OllamaBotLogs.log'
                    , filemode='w', level=logging.INFO, format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

client = Bot(token="your token here")

@client.event
async def on_ready():
    print(client.user, "is Ready!")
    logger.info(f'bot is online!\n')

    

@client.event
async def on_message(message: Message):
    
    if message.content == '/start' :
        await message.reply('this is an ai assistant\n just type something to get answers with AI!')
        logger.info(f'"{message.author}" started the bot\n')

    elif message.content == '/help' :
        await message.reply('/list_models: list available models\n/"modelname": set the model to use\n/model: see what model you are using\n')
        logger.info(f'"{message.author}" asked for help!\n')
        

    elif message.content == '/list_models':
            await message.reply(list)
            logger.info(f'"{message.author}" listed models!\n')

    elif message.content in model_options:
        global uModel
        uModel = model_options[message.content]
        await message.reply(f"Model set to {uModel}")
        logger.info(f'"{message.author}" changed model to "{uModel}"\n')

    elif message.content == '/model' :
         await message.reply(f"Your current model is {uModel}")
         logger.info(f'"{message.author}" chacked the current model\n')

    else:
        question = message.content
        logger.info(f'"{message.author}" asked: "{question}" from model: "{uModel}"')
        try:
            response = ollama.chat(model=uModel, messages=[
                {
                'role': 'user',
                'content': question,},
                ])
            logger.info(f'"{uModel}" answered to "{message.author}" question\n')
            await message.reply(response['message']['content'])

        except ollama.ResponseError as e:
            logger.error(f'error while answering {message.author.username}: {e.error}')
            await message.reply(f'Error: {e.error}')

client.run()
