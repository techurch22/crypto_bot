from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from pycoingecko import CoinGeckoAPI
import re
from .settings import ex_key

updater = Updater(ex_key)
cg = CoinGeckoAPI()

def started(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Привет, я бот который подскажет актуальный '
                                                   'курс крипты. Для того, чтобы узнать курс укажи '
                                                   'необходимую крипту и целевую валюту через слеш, '
                                                   'например - bitcoin/usd, или - ethereum/rub ')

def crypto_func(update, context):
    chat = update.effective_chat
    text = update.to_dict()

    if re.fullmatch(r'^[a-zA-Z]+/[a-zA-Z]+$', text['message']['text']):
        coin_name = text['message']['text'].lower().split('/')
        temp = cg.get_price(ids=coin_name[0], vs_currencies=coin_name[1])
        if len(temp) != 0:
            for ident in temp.keys():
                for fiat in temp[ident]:
                    value = temp[ident][fiat]
            mess = (f'Выбранная криптовалюта : {str(ident).capitalize()}\n'
                    f'Стоимость : {value} {str(fiat).upper()}')
            context.bot.send_message(chat_id=chat.id, text=mess)

        else:
            context.bot.send_message(chat_id=chat.id, text='В базе отсутствует эта валюта')

    else:
        context.bot.send_message(chat_id=chat.id, text='Неверный формат запроса')


updater.dispatcher.add_handler(CommandHandler('start', started))
updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), crypto_func))

updater.start_polling()
updater.idle()
