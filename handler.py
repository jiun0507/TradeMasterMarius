import configparser as cfg
import json
from abc import (
    abstractclassmethod,
    ABC,
)

import requests

from reply_texts import button_text, reply
from telebot import apihelper, handler_backends, types, util


class TelegramInterface:
    def __init__(self, config):
        self.token = self.read_key_from_config_file(config, 'token')
        self.chat_id = self.read_key_from_config_file(config, 'bot_id')
        self.wake_up_url = self.read_key_from_config_file(config, 'wake_up_url')
        self.domain = self.read_key_from_config_file(config, 'domain')
        self.base = "{}{}/".format(self.domain, self.token)


    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url, timeout=3)
        print(url)
        return json.loads(r.content)


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

    def send_full_message(
            self, text, chat_id=None, token=None,
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
        payload = {'chat_id': str(self.chat_id), 'text': text}
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
        return apihelper._make_request(self.token, method_url, params=payload, method='post')


    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def read_key_from_config_file(self, config, key):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', key)


    def gather_messages(self):
        sent_messages = []
        update_id = None

        try:
            updates = self.get_updates(offset=update_id)
            updates = updates["result"]

            if updates:
                for item in updates:
                    # reply_markup = None
                    update_id = item["update_id"]
                    try:
                        message = str(item["message"]["text"])
                    except:
                        message = None
                    # from_ = item["message"]["from"]["id"]
                    sent_messages.append(message)
                    # self.send_full_message(self.token, message, from_, reply_markup=reply_markup)
                    updates = self.get_updates(offset=update_id)

        except (requests.exceptions.Timeout, ValueError):
            return sent_messages

        return sent_messages

class BaseView(ABC):
    def __init__(self, use_case):
        self.use_case = use_case

    @abstractclassmethod
    def get(self):
        pass


class AlpacaView(BaseView):
    def get(self):
        return self.use_case.get()

    def get_financial_statement(self):
        return self.use_case.get_financial_statement()

    def get_polygon_ticker_symbols(self):
        return self.use_case.get_ticker_symbols()

