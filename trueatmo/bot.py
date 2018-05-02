# import sys
import time
# import threading
# import random
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
# from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
# from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
import requests
from bs4 import BeautifulSoup
import bs4, requests
message_with_inline_keyboard = None

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)
    # update['message']['chat']['first_name']
    if content_type != 'text':
        return
    command = msg['text'].lower()


    def search_meteo(text):
        response = requests.post('http://meteo.ua/ua/search-forecast-by-city-name', data={'name': text})
        b = bs4.BeautifulSoup(response.text, "html.parser")
        p3 = b.select('.main_cont p a')
        hrefs = p3[0]['href']
        print(hrefs)
        return hrefs

        hrefs = search_meteo(text=text)
        s = requests.get('http://meteo.ua{}'.format(hrefs))
        b = bs4.BeautifulSoup(s.text, "html.parser")
        p3 = b.select('.wi_now')
        tempnow = p3[0].getText()
        print(tempnow)

        p3 = b.select('.wiw_power')
        windnow = p3[0].getText()
        print(windnow)

        p3 = b.select('.wi_right')
        day = p3[0].getText()
        print(day)

        p3 = b.select('.wwt_tmps')
        minmaxdoba = p3[0].getText()
        print(minmaxdoba)
        bot.sendMessage(chat_id, 'message')
    if command == '/start' :

        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🗓️ current weather 🗓️'), KeyboardButton(text='📅 weekly weather 📅',)],
        [KeyboardButton(text='🔧 settings 🔧')],
        ])
        bot.sendMessage(chat_id, '*HI!*', reply_markup=markup, parse_mode='Markdown')
    # elif command != '/start' or '🗓️ current weather 🗓️' or '📅 weekly weather 📅' or '🔧 settings 🔧' or '📌 last location 📌' or '🌐 languages 🌐' or '📝 units 📝' or '🔙 back 🔙' or '⏰ alerts ⏰' or 'celsium(°C)' or 'fahrenheit(°F)' or '❌ cancel ❌' or '🏴󠁧󠁢󠁥󠁮󠁧󠁿 english 🏴󠁧󠁢󠁥󠁮󠁧󠁿' or '🇺🇦 українська 🇺🇦' or '🇩🇪 deutsch 🇩🇪' or '🇷🇺 русский 🇷🇺':
    #     def search_meteo(text):
    #         response = requests.post('http://meteo.ua/ua/search-forecast-by-city-name', data={'name': text})
    #         b = bs4.BeautifulSoup(response.text, "html.parser")
    #         p3 = b.select('.main_cont p a')
    #         hrefs = p3[0]['href']
    #         print(hrefs)
    #         return hrefs
    #
    #     hrefs = search_meteo(text=text)
    #     s = requests.get('http://meteo.ua{}'.format(hrefs))
    #     b = bs4.BeautifulSoup(s.text, "html.parser")
    #     p3 = b.select('.wi_now')
    #     tempnow = p3[0].getText()
    #     print(tempnow)
    #
    #     p3 = b.select('.wiw_power')
    #     windnow = p3[0].getText()
    #     print(windnow)
    #
    #     p3 = b.select('.wi_right')
    #     day = p3[0].getText()
    #     print(day)
    #
    #     p3 = b.select('.wwt_tmps')
    #     minmaxdoba = p3[0].getText()
    #     print(minmaxdoba)
    #     bot.sendMessage(chat_id,'message')
    elif command == '🗓️ current weather 🗓️':
        text = msg['text'].lower()

        def search_meteo(text):
            response = requests.post('http://meteo.ua/ua/search-forecast-by-city-name', data={'name': text})
            # with open('test.html', 'w') as file:
            #     file.write(response.text)
            b = bs4.BeautifulSoup(response.text, "html.parser")
            p3 = b.select('.main_cont p a')
            if not p3:
                return response.text
            hrefs = p3[0]['href']
            print(hrefs)
            return hrefs

        data = search_meteo(text=text)
        if data.startswith('http'):
            data = requests.get('http://meteo.ua{}'.format(data))
            data = data.text
        b = bs4.BeautifulSoup(data, "html.parser")
        p3 = b.select('.wi_now')
        tempnow = p3[0].getText()
        print(tempnow)
        p3 = b.select('.wiw_power')
        windnow = p3[0].getText()
        print(windnow)
        p3 = b.select('.wi_right')
        day = p3[0].getText()
        print(day)
        p3 = b.select('.wwt_tmps')
        minmaxdoba = p3[0].getText()
        print(minmaxdoba)
        bot.sendMessage(chat_id, tempnow, parse_mode='Markdown')
    elif command == '📌 last location 📌':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='🗓️ current weather 🗓️'), KeyboardButton(text='📅 weekly weather 📅', )],
            [KeyboardButton(text='🔧 settings 🔧')],
        ])
        s = requests.get('http://meteo.ua/ua/44/lvov')
        b = bs4.BeautifulSoup(s.text, "html.parser")

        p3 = b.select('.wi_now')
        tempnow = p3[0].getText()
        print(tempnow)

        p4 = b.select('.wiw_power')
        windnow = p4[0].getText()

        weather_now = tempnow + 'Wind:' + windnow

        bot.sendMessage(chat_id,weather_now, reply_markup=markup)
    elif command == '📅 weekly weather 📅':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='📌 last location 📌')],[ KeyboardButton(text='➕ new Location ➕')],
        [KeyboardButton(text='🗺️ my location 🗺️', request_location=True)],[KeyboardButton(text='🔙 back 🔙')]
        ])
        bot.sendMessage(chat_id, '*Choose location*', reply_markup=markup, parse_mode='Markdown')
    elif command == '🗺️ my location 🗺️':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='📌 last location 📌')],[ KeyboardButton(text='➕ new Location ➕')],
        [KeyboardButton(text='🗺️ my location 🗺️', request_location=True)],[KeyboardButton(text='🔙 back 🔙')]
        ])
        bot.sendMessage(chat_id, '*Choose location*', reply_markup=markup, parse_mode='Markdown')
    elif command == '🔧 settings 🔧':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🌐 languages 🌐'), KeyboardButton(text='📝 units 📝')],
        [KeyboardButton(text='⏰ alerts ⏰'), KeyboardButton(text='🔙 back 🔙')]
        ])
        bot.sendMessage(chat_id, '*Set up your bot*', reply_markup=markup, parse_mode='Markdown')
    elif command == '🔙 back 🔙':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🗓️ current weather 🗓️'), KeyboardButton(text='📅 weekly weather 📅',)],
        [KeyboardButton(text='🔧 settings 🔧')],
        ])
        bot.sendMessage(chat_id, '*you returned back*', reply_markup=markup, parse_mode='Markdown')
    elif command == '📝 units 📝':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='celsium(°C)'), KeyboardButton(text='fahrenheit(°F)', )],
        [KeyboardButton(text='❌ cancel ❌')],
        ])
        bot.sendMessage(chat_id, '*Choose Celsium or Fahrenheit*', reply_markup=markup, parse_mode='Markdown')
    elif command == '❌ cancel ❌':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🌐 languages 🌐'), KeyboardButton(text='📝 units 📝')],
        [KeyboardButton(text='⏰ alerts ⏰'), KeyboardButton(text='🔙 back 🔙')]
        ])
        bot.sendMessage(chat_id, '*Set up your bot*', reply_markup=markup, parse_mode='Markdown')
    if command == 'celsium(°c)':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🗓️ current weather 🗓️'), KeyboardButton(text='📅 weekly weather 📅',)],
        [KeyboardButton(text='🔧 settings 🔧')],
        ])
        bot.sendMessage(chat_id, '*Units now are metric(celsium)*', reply_markup=markup, parse_mode='Markdown')
    if command == 'fahrenheit(°f)':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🗓️ current weather 🗓️'), KeyboardButton(text='📅 weekly weather 📅',)],
        [KeyboardButton(text='🔧 settings 🔧')],
        ])
        bot.sendMessage(chat_id, '*Units now are imperial(fahrenheit)*', reply_markup=markup, parse_mode='Markdown')
    if command == '🌐 languages 🌐':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🏴󠁧󠁢󠁥󠁮󠁧󠁿 english 🏴󠁧󠁢󠁥󠁮󠁧󠁿'), KeyboardButton(text='🇩🇪 deutsch 🇩🇪',)],
        [KeyboardButton(text='🇺🇦 українська 🇺🇦'), KeyboardButton(text='🇷🇺 русский 🇷🇺',)],
        ])
        bot.sendMessage(chat_id, '*Units now are imperial(fahrenheit)*', reply_markup=markup, parse_mode='Markdown')
    if command == '🏴󠁧󠁢󠁥󠁮󠁧󠁿 english 🏴':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🗓️ current weather 🗓️'), KeyboardButton(text='📅 weekly weather 📅', )],
        [KeyboardButton(text='🔧 settings 🔧')],
        ])
        bot.sendMessage(chat_id, '*Your language changed to English*', reply_markup=markup, parse_mode='Markdown')

        #ukrainian section

    if command == '🇺🇦 українська 🇺🇦':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🗓️ поточна погода 🗓️'), KeyboardButton(text='📅 тижнева погода 📅', )],
        [KeyboardButton(text='🔧 налаштування 🔧')],
        ])
        bot.sendMessage(chat_id, '*Ваша мова була змінена на Українську*', reply_markup=markup, parse_mode='Markdown')
    elif command == '🗓️ поточна погода 🗓️':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='📌 останнє місце 📌')],[ KeyboardButton(text='➕ нове місце ➕')],
        [KeyboardButton(text='🗺️ моє місце 🗺️', request_location=True)],[KeyboardButton(text='🔙 назад 🔙')]
        ])
        bot.sendMessage(chat_id, '*Виберіть місцезнаходження*', reply_markup=markup, parse_mode='Markdown')
    elif command == '📅 тижнева погода 📅':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='📌 останнє місце 📌')],[ KeyboardButton(text='➕ нове місце ➕')],
        [KeyboardButton(text='🗺️ моє місце 🗺️', request_location=True)],[KeyboardButton(text='🔙 назад 🔙')]
        ])
        bot.sendMessage(chat_id, '*Виберіть місцезнаходження*', reply_markup=markup, parse_mode='Markdown')
    elif command == '🔧 налаштування 🔧':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🌐 мови 🌐'), KeyboardButton(text='📝 одиниці 📝')],
        [KeyboardButton(text='⏰ сповіщення ⏰'), KeyboardButton(text='🔙 назад 🔙')]
        ])
        bot.sendMessage(chat_id, '*Налаштуйте свого бота*', reply_markup=markup, parse_mode='Markdown')
    elif command == '🔙 назад 🔙':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🗓️ поточна погода 🗓️'), KeyboardButton(text='📅 тижнева погода 📅',)],
        [KeyboardButton(text='🔧 налаштування 🔧')],
        ])
        bot.sendMessage(chat_id, '*Ви повернулися назад*', reply_markup=markup, parse_mode='Markdown')
    elif command == '📝 одиниці 📝':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='цельсії(°C)'), KeyboardButton(text='фаренгейти(°F)', )],
        [KeyboardButton(text='❌ відмінити ❌')],
        ])
        bot.sendMessage(chat_id, '*Виберіть одиниці виміру*', reply_markup=markup, parse_mode='Markdown')
    elif command == '❌ відмінити ❌':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🌐 мови 🌐'), KeyboardButton(text='📝 одиниці 📝')],
        [KeyboardButton(text='⏰ сповіщення ⏰'), KeyboardButton(text='🔙 назад 🔙')]
        ])
        bot.sendMessage(chat_id, '*налаштуйте свого бота*', reply_markup=markup, parse_mode='Markdown')
    if command == 'цельсії(°c)':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🗓️ поточна погода 🗓️'), KeyboardButton(text='📅 тижнева погода 📅',)],
        [KeyboardButton(text='🔧 налаштування 🔧')],
        ])
        bot.sendMessage(chat_id, '*Одиниці виміру були змінені на цельсії*', reply_markup=markup, parse_mode='Markdown')
    if command == 'фаренгейти(°f)':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🗓️ поточна погода 🗓️'), KeyboardButton(text='📅 тижнева погода 📅',)],
        [KeyboardButton(text='🔧 налаштування 🔧')],
        ])
        bot.sendMessage(chat_id, '*Одиниці виміру були змінені на фаренгейти*', reply_markup=markup, parse_mode='Markdown')
    if command == '🌐 мови 🌐':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🏴󠁧󠁢󠁥󠁮󠁧󠁿 english 🏴󠁧󠁢󠁥󠁮󠁧󠁿'), KeyboardButton(text='🇩🇪 deutsch 🇩🇪',)],
        [KeyboardButton(text='🇺🇦 українська 🇺🇦'), KeyboardButton(text='🇷🇺 русский 🇷🇺',)],
        ])
        bot.sendMessage(chat_id, '*Виберіть мову*', reply_markup=markup,
parse_mode='Markdown')
# TOKEN = '577877864:AAEh1MKE62KPntQjSuEtH53sDYJDes3oYyM' newskit token

TOKEN = "597420522:AAHdU-Cy7B6U_wQ5UQBjLp1TsmlSeyr2aY8"
bot = telepot.Bot(TOKEN)

answerer = telepot.helper.Answerer(bot)
MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()

print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)


