import configparser as cfg

class keys_class:
    def __init__(self, config):
        self.token = self.read_key_from_config_file(config, 'token')
        self.domain = self.read_key_from_config_file(config,'domain')

        self.base = "{}{}/".format(self.domain, self.token)

        self.alpaca_api_id = self.read_key_from_config_file(config, 'alpaca_api_id')
        self.alpaca_key = self.read_key_from_config_file(config, 'alpaca_key')

        self.bot_id = self.read_key_from_config_file(config, 'bot_id')
        self.wake_up_url = self.read_key_from_config_file(config, 'wake_up_url')
        self.alpaca_paper_url = self.read_key_from_config_file(config, 'alpaca_paper_url')
        self.fmp_api_key = self.read_key_from_config_file(config, 'fmp_api_key')


    def read_key_from_config_file(self, config, key):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', key)