from bot import (
    telegram_chatbot,
    alpaca_bot,
)
import json
import requests
from reply_texts import (
    reply,
    button_text,
)
from fmp_client import FMPClient

class listen_view:
    def __init__(self):
        self.bot = telegram_chatbot(".config.cfg")
        self.alpaca = alpaca_bot(".config.cfg")
    def input_message(self):
            update_id = None
            telegram_id = -1
            response = ''

            try:
                updates = self.bot.get_updates(offset=update_id)
                updates = updates["result"]
                if updates:
                    for item in updates:
                        update_id = item["update_id"]
                        try:
                            message = str(item["message"]["text"])
                        except ValueError:
                            raise ValueError
                        from_ = item["message"]["from"]["id"]
                        telegram_id = from_
                        positions = self.handle_message(message)
                        for position in positions:
                            res = self.alpaca.get_polygon_financial_statement(symbol=position, limit=1)
                            self.bot.send_message(res['results'][0], self.bot.bot_id)
                        updates = self.bot.get_updates(offset=update_id)
            except (requests.exceptions.Timeout, ValueError):
                if telegram_id == -1:
                    response = reply.no_work.value
                else:
                    response = reply.sleep.value
                self.bot.send_message(response, self.bot.bot_id)
                return response

            return response

    def handle_message(self, message):
        positions = self.alpaca.get_position_list()
        response = []
        for position in positions:
            print(position.symbol)
            response.append(position.symbol)
        return response