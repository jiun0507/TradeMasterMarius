from alpaca_use_case import AlpacaUseCase
from handler import (TelegramInterface,
                     AlpacaView)
from alpaca_repository import AlpacaRepository
import json
from desktop import LandingWindow

print("started")
LandingWindow()

# def lambda_handler(event=None, context=None):
    # telegram = TelegramInterface(".config.cfg")
    # requests = telegram.gather_messages()

    # for request in requests:
    #     messages = []
    #     if request == 'Alpa':
    #         result = AlpacaView(AlpacaUseCase(AlpacaRepository())).get()
    #         messages.append(result)
    #     if request == 'FS':
    #         result = AlpacaView(AlpacaUseCase(AlpacaRepository())).get_financial_statement()
    #         messages.append(json.dumps(result))
    #     if request == 'tickers':
    #         result = AlpacaView(AlpacaUseCase(AlpacaRepository())).get_polygon_ticker_symbols()
    #         messages.append(json.dumps(result))
    #     for message in messages:
    #         telegram.send_full_message(text=message)
# lambda_handler()