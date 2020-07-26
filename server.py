import json

import requests
from bot import telegram_chatbot
from handler import listen_view



initial_handler = listen_view()

def lambda_handler(event=None, context=None):
    initial_handler.input_message()

lambda_handler()
