from bot import telegram_chatbot
import json
import requests
from reply_texts import (
    reply,
    button_text,
)
from fmp_client import FMPClient

class message_handler:
    def __init__(self, bot):
        self.bot = bot
        self.fmp_client = FMPClient(self.bot.fmp_api_key)

    def handle_message(self):
        update_id = None
        telegram_id = -1
        response = {
            "statusCode": 200,
            "body": json.dumps({"message": 'ok'})
        }
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
                    if message == 'fmp':
                        tickers=['GOOG']
                        res = self.fmp_client.company_valuation.income_statement(tickers)

                    message = self.bot.get_balance_info(api=self.bot.alpaca_api)
                    self.bot.send_message(message, self.bot.bot_id)
                    updates = self.bot.get_updates(offset=update_id)
        except (requests.exceptions.Timeout, ValueError):
            if telegram_id == -1:
                message = reply.no_work.value
            else:
                message = reply.sleep.value

            self.bot.send_message(message, self.bot.bot_id)
            return response

        return response
