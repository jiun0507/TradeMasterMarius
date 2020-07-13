from bot import telegram_chatbot
import json
import requests
from reply_texts import (
    reply,
    button_text,
)


class message_handler:
    def __init__(self, bot):
        self.bot = bot
        
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
                    reply_markup = None
                    update_id = item["update_id"]
                    try:
                        message = str(item["message"]["text"])
                    except:
                        message = None
                    from_ = item["message"]["from"]["id"]
                    telegram_id = from_
                    message = self.bot.get_account_info(api=self.bot.alpaca_api)
                    
                    self.bot.send_full_message(self.bot.token, message, from_, reply_markup=reply_markup)
                    updates = self.bot.get_updates(offset=update_id)
        except (requests.exceptions.Timeout, ValueError):
            if telegram_id == -1:
                message = reply.no_work.value
            else:
                message = reply.sleep.value
            options = []
            options.append(button_text.wake_up.value)

            urls = []
            urls.append(self.bot.wake_up_url)
            inline_reply_markup = self.bot.get_inline_reply_markup_with_urls(options=options,urls=urls)
            self.bot.send_full_message(self.bot.token, message, self.bot.bot_id, reply_markup=inline_reply_markup)
            return response

        return response
