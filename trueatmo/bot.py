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
import json
message_with_inline_keyboard = None


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg)
    # response = requests.get('127.0.0.1:8001/person/{}'.format(msg['from']['id']))
    # update['message']['chat']['first_name']
    if content_type != 'text':
        bot.sendMessage(chat_id, "*Sorry, bot can't understand your message 😢😢*", parse_mode='Markdown')
        return
    command = msg['text'].lower()

    # location = 'location from db'
    # last_location_current = '📌 ' + location + ' 🗓️'
    # last_location_weekly = '📌 ' + location + ' 📅️'
    # text = 'lvov'

    # text = msg['text'].lower()
    # bot.sendMessage(462005869, '*Write your location!*', parse_mode='Markdown')



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

    # data = search_meteo(text=text)
    # if data.startswith('http'):
    #     data = requests.get('http://meteo.ua{}'.format(data))
    #     data = data.text
    # b = bs4.BeautifulSoup(data, "html.parser")
    # p3 = b.select('.wi_now')
    # tempnow = p3[0].getText()
    # print(tempnow)
    # p3 = b.select('.wiw_power')
    # windnow = p3[0].getText()
    # print(windnow)
    # p3 = b.select('.wi_right')
    # day = p3[0].getText()
    # print(day)
    # p3 = b.select('.wwt_tmps')
    # minmaxdoba = p3[0].getText()
    # print(minmaxdoba)

    if command == '/start' :
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🗓️ current weather 🗓️'), KeyboardButton(text='📅 weekly weather 📅',)],
        [KeyboardButton(text='🔧 settings 🔧')],
        ])
        # bot.sendMessage(chat_id, "", parse_mode='HTML')
        bot.sendMessage(chat_id, '*HI!*', reply_markup=markup, parse_mode='Markdown')
    elif msg['text'].startswith('/location'):
        r_get = requests.get('http://127.0.0.1:8002/person?telegram_id={}'.format(msg['from']['id']))
        response = r_get.json()
        response = json.loads(response)
        location = msg['text'].replace('/location','').lower()
        location = location.strip()
        data = {'locations': location, 'id': msg['from']['id'], 'user_tag': msg['from']['username'],'telegram_id': msg['from']['id']}
        r_put = requests.put('http://127.0.0.1:8002/person/', data=data)
        # r_post_data = r_put.json()
        # response = json.loads(response)
        r_put(locations='location', user_tag=msg['from']['username'], telegram_id=msg['from']['id'])
        bot.sendMessage(chat_id,location)
    elif command == '🗓️ current weather 🗓️':
        r_get = requests.get('http://127.0.0.1:8002/person?telegram_id={}'.format(msg['from']['id']))
        response = r_get.json()
        response = json.loads(response)
        print(response)
        if not response['is_error']:
            if not response['data']:
                data = {'user_tag':msg['from']['username'],'telegram_id':msg['from']['id']}
                r_post = requests.post('http://127.0.0.1:8002/person',data = data)
                # print(r_post)
                r_post_data = r_post.json()
                r_post_data = json.loads(r_post_data)
                print(r_post_data)
                user_id = r_post_data['id']
                if r_post_data['locations'] == None:
                    bot.sendMessage(chat_id, '*Write "/location (your location)" !*', parse_mode='Markdown')
    # if oldMessage_text == '🗓️ current weather 🗓️':
    #     bot.sendMessage(chat_id, msg['text'])
    #     if r_get data = {'locations' : null}:
    #             bot.sendMessage(chat_id, 'Write location')
    #             r_put(locations=(msg['text']), user_tag=msg['from']['username'], telegram_id=msg['from']['id'])
    #     else :
    #         pass
    #     if r_get data{'locations' = str}:
    #         #замість str потрібно якось перевірити що в 'locations' лежить стрінга
    #         markup = ReplyKeyboardMarkup(keyboard=[
    #             [KeyboardButton(text='🗓️ current weather 🗓️'), KeyboardButton(text='📅 weekly weather 📅', )],
    #             [KeyboardButton(text='🔧 settings 🔧')],
    #         ])
    #         location = data{'locations'}
    #         dataa = search_meteo(text=location)
    #         if dataa.startswith('http'):
    #             dataa = requests.get('http://meteo.ua{}'.format(dataa))
    #             dataa = dataa.location
    #         b = bs4.BeautifulSoup(dataa, "html.parser")
    #         p3 = b.select('.wi_now')
    #         tempnow = p3[0].getText()
    #         p3 = b.select('.wiw_power')
    #         windnow = p3[0].getText()
    #         # tempnow = '\t'.join(tempnow.split())
    #         # windnow = windnow + '\t'
    #         weather_now = tempnow + windnow
    #         bot.sendMessage(chat_id, weather_now, reply_markup=markup)
    # elif command == '➕ new location 🗓️':
    #     markup = ReplyKeyboardMarkup(keyboard=[
    #         [KeyboardButton(text='🗓️ ️show weather 🗓️')]
    #     ])
    #     bot.sendMessage(chat_id,'Write your city', reply_markup=markup)
    # elif command == last_location_current:
    #     markup = ReplyKeyboardMarkup(keyboard=[
    #         [KeyboardButton(text='🗓️ current weather 🗓️'), KeyboardButton(text='📅 weekly weather 📅', )],
    #         [KeyboardButton(text='🔧 settings 🔧')],
    #     ])
    #     # location це локація яка записана в базу даних
    #     location= 'lvov'
    #     data = search_meteo(text=location)
    #     if data.startswith('http'):
    #         data = requests.get('http://meteo.ua{}'.format(data))
    #         data = data.location
    #     b = bs4.BeautifulSoup(data, "html.parser")
    #     p3 = b.select('.wi_now')
    #     tempnow = p3[0].getText()
    #     print(tempnow)
    #     p3 = b.select('.wiw_power')
    #     windnow = p3[0].getText()
    #     print(windnow)
    #     p3 = b.select('.wi_right')
    #     day = p3[0].getText()
    #     print(day)
    #     p3 = b.select('.wwt_tmps')
    #     minmaxdoba = p3[0].getText()
    #     print(minmaxdoba)
    #     # minmaxdoba = '\t'.join(minmaxdoba.split())
    #     tempnow = '\t'.join(tempnow.split())
    #     windnow= windnow+'\t'
    #     weather_now= tempnow+ windnow+ minmaxdoba
    #     bot.sendMessage(chat_id,weather_now, reply_markup=markup)
    # elif command == '📅 weekly weather 📅':
    #     markup = ReplyKeyboardMarkup(keyboard=[
    #     [KeyboardButton(text=last_location_weekly), KeyboardButton(text='➕ new location 📅')],[KeyboardButton(text='🔙 back 🔙')]
    #     ])
    #     bot.sendMessage(chat_id, '*Choose location*', reply_markup=markup, parse_mode='Markdown')
    elif command == '➕ new location 📅':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='🗓️ ️show weather 🗓️')]
        ])
        bot.sendMessage(chat_id,'Write your city', reply_markup=markup)
    # elif command == last_location_weekly:
    #     markup = ReplyKeyboardMarkup(keyboard=[
    #         [KeyboardButton(text='🗓️ current weather 🗓️'), KeyboardButton(text='📅 weekly weather 📅', )],
    #         [KeyboardButton(text='🔧 settings 🔧')],
    #     ])
        # location це локація яка записана в базу даних
        location = 'lvov'
        data = search_meteo(text=location)
        if data.startswith('http'):
            data = requests.get('http://meteo.ua{}'.format(data))
            data = data.location
        b = bs4.BeautifulSoup(data, "html.parser")
        p3 = b.select('.wi_right')
        day = p3[0].getText()
        print(day)
        p3 = b.select('.wwt_tmps')
        minmaxdoba = p3[0].getText()
        print(minmaxdoba)
        weather_weekly = "Сьогодні:" + minmaxdoba + day
        bot.sendMessage(chat_id, weather_weekly, reply_markup=markup)

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
TOKEN = "587773115:AAHmGKQ1y5UZLmKRrmLznBSu6EN6UYtCz48"
bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)
MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()

print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)


