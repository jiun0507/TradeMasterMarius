import requests
import json
import configparser as cfg

from telebot import (
    apihelper,
    handler_backends,
    types,
    util,
)
from reply_texts import reply
import alpaca_trade_api as tradeapi



class alpaca_bot:
    def get_balance_info(self, api):
        # Get our account information.
        account = api.get_account()

        # Check our current balance vs. our balance at the last market close
        balance_change = float(account.equity) - float(account.last_equity)
        return 'Today\'s portfolio balance change:{}'.format(balance_change)

    def get_polygon_financial_statement(self, api, symbol, limit):
        params = {}
        params['limit'] = limit
        financial_statement = api.polygon.get(path='/reference/financials/'+symbol, params=params, version='v2')
        return financial_statement

class telegram_chatbot(alpaca_bot):

    def __init__(self, config):
        super().__init__()
        self.token = self.read_key_from_config_file(config, 'token')
        self.alpaca_api_id = self.read_key_from_config_file(config, 'alpaca_api_id')
        self.alpaca_key = self.read_key_from_config_file(config, 'alpaca_key')

        self.bot_id = self.read_key_from_config_file(config, 'bot_id')
        self.wake_up_url = self.read_key_from_config_file(config, 'wake_up_url')
        self.domain = self.read_key_from_config_file(config, 'domain')
        self.base = "{}{}/".format(self.domain, self.token)
        self.alpaca_paper_url = self.read_key_from_config_file(config, 'alpaca_paper_url')
        self.alpaca_api = tradeapi.REST(self.alpaca_api_id, self.alpaca_key, 'https://paper-api.alpaca.markets', api_version='v2')
        self.fmp_api_key = self.read_key_from_config_file(config, 'fmp_api_key')

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

    def read_key_from_config_file(self, config, key):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', key)


