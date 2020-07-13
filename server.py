import json

import requests
from bot import telegram_chatbot
from handler import message_handler


bot = telegram_chatbot(".config.cfg")
initial_handler = message_handler(bot)

def lambda_handler(event=None, context=None):
    initial_handler.handle_message()
    
lambda_handler()
