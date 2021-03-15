import configparser as cfg

import alpaca_trade_api as tradeapi

config = ".config.cfg"


class Accountant:
    def __init__(self):
        self.alpaca_api_id = self.read_key_from_config_file(config, "alpaca_api_id")
        self.alpaca_key = self.read_key_from_config_file(config, "alpaca_key")

    def read_key_from_config_file(self, config, key):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get("creds", key)
