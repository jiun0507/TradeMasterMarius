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

payload = {
  "homeMobileCountryCode": '450',
  "homeMobileNetworkCode": '03',
  "radioType": "gsm",
  "carrier": "SKT",
  "considerIp": "true",
  "cellTowers": [
  ],
  "wifiAccessPoints": [
  ]
}

class alpaca_bot:
    def get_account_info(self, api):
        # Get our account information.
        account = api.get_account()

        # Check our current balance vs. our balance at the last market close
        balance_change = float(account.equity) - float(account.last_equity)
        return 'Today\'s portfolio balance change:{}'.format(balance_change)


class github_bot:
    def get_github(self, token):
        headers = {'Authorization': token}

        res = requests.get("https://api.github.com/user", headers=headers)

        data = json.loads(res.content)

        res = requests.get(data['repos_url'], headers=headers)

        github_data = json.loads(res.content)
        repo_num = len(github_data)
        names = ''
        for repo in github_data:
            names += repo['name'] + '\n'
        result = 'You have {} repos. \nThey are : \n{}.'.format(repo_num, names[:-1])
        return result

class jira_bot:
 
    def get_jira_tickets(self, key, domain):
        headers = {
            'Authorization': key,
            'Content-Type': 'application/json',
        }
        params = (
            ('jql', 'assignee=bob'),
        )
        res = requests.get(domain, headers=headers, params=params)
        jira_tickets = json.loads(res.content)
        ticket_num = len(jira_tickets)
        print("There are {} of tickets assigned to bob.".format(ticket_num))
        message = ""
        for jira_ticket in jira_tickets['issues']:
            if jira_ticket['fields']['status']['name'] not in ['Done', 'Backlog']:
                ticket = '{}: {} status {}\n'.format(jira_ticket['key'], jira_ticket['fields']['summary'], jira_ticket['fields']['status']['name'])
                message += ticket
        return message

    def get_reply_markup(self, options, parse_mode=None):
        markup = types.ReplyKeyboardMarkup()
        for option in options:
            item = types.KeyboardButton(option)
            markup.row(item)
        return markup


    def get_inline_reply_markup_with_urls(self, options, urls, parse_mode=None):
        markup = types.InlineKeyboardMarkup()
        for (option, url) in zip(options, urls):
            item = types.InlineKeyboardButton(text=option, url=url)
            markup.add(item)
        return markup


class google_map_bot:
    def get_location(self, key, url):
        params = (
            ('key={}'.format(key))
        )
        res = requests.post(url, params=params)
        data = json.loads(res.content)
        message = "You are at lattitude = {}, longtitude = {}".format(data['location']['lat'], data['location']['lng'])
        return message


class telegram_chatbot(github_bot, jira_bot, google_map_bot, alpaca_bot):

    def __init__(self, config):
        super().__init__()
        self.token = self.read_key_from_config_file(config, 'token')
        self.github_token =  self.read_key_from_config_file(config, 'github_token')
        self.google_map_key =  self.read_key_from_config_file(config, 'google_map_key')
        self.youjin_token = self.read_key_from_config_file(config, 'youjin_token')
        self.jira_authorization = self.read_key_from_config_file(config, 'jira_authorization')
        self.alpaca_api_id = self.read_key_from_config_file(config, 'alpaca_api_id')
        self.alpaca_key = self.read_key_from_config_file(config, 'alpaca_key')

        self.bot_id = self.read_key_from_config_file(config, 'bot_id')
        self.wake_up_url = self.read_key_from_config_file(config, 'wake_up_url')
        self.domain = self.read_key_from_config_file(config, 'domain')
        self.geolocation_url = self.read_key_from_config_file(config, 'geolocation_url')
        self.jira_domain = self.read_key_from_config_file(config, 'jira_domain')
        self.base = "{}{}/".format(self.domain, self.token)
        self.base2 = "{}{}/".format(self.domain, self.youjin_token)

        self.alpaca_api = tradeapi.REST(        
            self.alpaca_api_id,
            self.alpaca_key,
            'https://paper-api.alpaca.markets',
            api_version='v2',
        )

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url, timeout=3)
        return json.loads(r.content)


    def send_full_message(
            self, token, text, chat_id,
            disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
            parse_mode=None, disable_notification=None, timeout=None):
        """
        Use this method to send text messages. On success, the sent Message is returned.
        :param token:
        :param chat_id:
        :param text:
        :param disable_web_page_preview:
        :param reply_to_message_id:
        :param reply_markup:
        :param parse_mode:
        :param disable_notification:
        :param timeout:
        :return:
        """
        method_url = r"sendMessage"
        payload = {'chat_id': str(chat_id), 'text': text}
        if disable_web_page_preview is not None:
            payload['disable_web_page_preview'] = disable_web_page_preview
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = apihelper._convert_markup(reply_markup)
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if timeout:
            payload['connect-timeout'] = timeout
        return apihelper._make_request(token, method_url, params=payload, method='post')


    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def read_key_from_config_file(self, config, key):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', key)


