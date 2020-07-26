import configparser as cfg
import json

import alpaca_trade_api as tradeapi
import requests

from keys import keys_class
from reply_texts import reply
from telebot import apihelper, handler_backends, types, util


class alpaca_bot(keys_class):
    def __init__(self, config):
        super().__init__(config)
        self.alpaca_api = tradeapi.REST(self.alpaca_api_id, self.alpaca_key, 'https://paper-api.alpaca.markets', api_version='v2')

    def get_balance_info(self, api):
        # Get our account information.
        account = api.get_account()

        # Check our current balance vs. our balance at the last market close
        balance_change = float(account.equity) - float(account.last_equity)
        return 'Today\'s portfolio balance change:{}'.format(balance_change)

    def get_position_list(self):
        positions = self.alpaca_api.list_positions()
        return positions

    def get_polygon_financial_statement(self, symbol, limit):
        params = {}
        params['limit'] = limit
        financial_statement = self.alpaca_api.polygon.get(path='/reference/financials/'+symbol, params=params, version='v2')
        return financial_statement

class telegram_chatbot(keys_class):

    def __init__(self, config):
        super().__init__(config)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url, timeout=3)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)
