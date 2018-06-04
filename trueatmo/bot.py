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
from meteo import get_weather_meteo
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg)
    # response = requests.get('127.0.0.1:8001/person/{}'.format(msg['from']['id']))
    # update['message']['chat']['first_name']
    if content_type != 'text':
        bot.sendMessage(chat_id, "*Sorry, bot can't understand your message 😢😢*", parse_mode='Markdown')
        return
    command = msg['text']
    # command = msg['text'].lower()

    # location = 'location from db'
    # last_location_current = '📌 ' + location + ' 🗓️'
    # last_location_weekly = '📌 ' + location + ' 📅️'
    # text = 'lvov'

    # text = msg['text'].lower()
    # bot.sendMessage(462005869, '*Write your location!*', parse_mode='Markdown')

    # if content_type == 'text':
    #     bot.sendMessage(chat_id, '*Hacked by Ustym!*',  parse_mode='Markdown')

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
        [KeyboardButton(text='📆 Show Weather 📆')],
        [KeyboardButton(text='🔧 Settings 🔧')],
        ])
        # bot.sendMessage(chat_id, "", parse_mode='HTML')
        bot.sendMessage(chat_id, '*HI!*', reply_markup=markup, parse_mode='Markdown')
    elif command == '📆 Show Weather 📆':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🗓️ Current Weather 🗓️'), KeyboardButton(text='📅 Daily Weather 📅',)],
        [KeyboardButton(text='🔙 Back 🔙')],
        ])
        bot.sendMessage(chat_id, "Choose weather",reply_markup=markup, parse_mode='HTML')
    elif msg['text'].startswith('/location'):
        r_get = requests.get('http://127.0.0.1:8002/person?telegram_id={}'.format(msg['from']['id']))
        response = r_get.json()
        response = json.loads(response)
        location = msg['text'].replace('/location','').lower()
        location = location.strip()
        data = {'id':response['data']['id'],'user_tag': msg['from']['first_name'],'telegram_id': msg['from']['id']
                ,'locations': location }
        r_put = requests.put('http://127.0.0.1:8002/person',data=data)
        loc= 'Your location is now : ' +location
        bot.sendMessage(chat_id,loc)
    elif msg['text'].startswith('/l'):
        r_get = requests.get('http://127.0.0.1:8002/person?telegram_id={}'.format(msg['from']['id']))
        response = r_get.json()
        response = json.loads(response)
        location = msg['text'].replace('/l', '').lower()
        location = location.strip()
        data = {'id': response['data']['id'], 'user_tag': msg['from']['first_name'], 'telegram_id': msg['from']['id']
            ,'locations': location}
        r_put = requests.put('http://127.0.0.1:8002/person', data=data)
        loc= 'Your location is now : ' +location
        bot.sendMessage(chat_id,loc)
    elif command == '🗓️ Current Weather 🗓️':
        r_get = requests.get('http://127.0.0.1:8002/person?telegram_id={}'.format(msg['from']['id']))
        response = r_get.json()
        response = json.loads(response)
        print('response = {}'.format(response))
        if not response['is_error']:
            if not response['data']:
                data = {'user_tag':msg['from']['first_name'],'telegram_id':msg['from']['id']}
                r_post = requests.post('http://127.0.0.1:8002/person',data=data)
                # print(r_post)
                r_post_data = r_post.json()
                response = json.loads(r_post_data)
                # print(r_post_data)
                user_data = response['data']
            user_id = response['data']['id']
            if response['data']['locations'] == None:
                bot.sendMessage(chat_id, '*Write "/location (your location)" or "/l" to set default location !*', parse_mode='Markdown')

        # result= requests.get('http://127.0.0.1:8002/weather?city={}'.format(user_location))
        # result =json.loads(result.json())
        # user_location = response['data']['locations']

        result =get_weather_meteo(response['data']['locations'])
        now =result['Now']
        # print(now)
        # weather_now = now['statusnow'] +'\n' +now['tempnow'] + '\n' + 'Вітер : ' + now['windnow'] +'\n' +now['minmaxtempdays']
        # tempnow = now['tempnow'].replace('Сьогодні о ','')
        minmax1 = now['minmaxtempdays'].replace('мін.','мін. ')
        minmax = minmax1.replace('макс.','макс. ')
        split_index= now['tempnow'].find('+') if now['tempnow'].find('+') != -1 else now['tempnow'].find('-')
        time_now = now['tempnow'][:split_index]
        temp_now = now['tempnow'][split_index:]
        # weather_now = time_now+' : ' + '\n' + '🌡️ : ' + temp_now+ '💨 : ' + now['windnow'] +'\n' + '🌡️ : ' +minmax+ '\n'  +'☀ : ️'+now['statusnow']
        weather_now = time_now+' : ' '\n'+ '🏙️ : '+response['data']['locations']+ '\n'+'Стан : ️'+now['statusnow']+  '\n' + '🌡️ : ' + temp_now+ '\n'+'💨 : ' + now['windnow']
        bot.sendMessage(chat_id, weather_now, parse_mode='HTML')

    elif command =='📅 Daily Weather 📅':
        r_get = requests.get('http://127.0.0.1:8002/person?telegram_id={}'.format(msg['from']['id']))
        response = r_get.json()
        response = json.loads(response)
        # print('response = {}'.format(response))
        if not response['is_error']:
            if not response['data']:
                data = {'user_tag':msg['from']['first_name'],'telegram_id':msg['from']['id']}
                r_post = requests.post('http://127.0.0.1:8002/person',data=data)
                # print(r_post)
                r_post_data = r_post.json()
                response = json.loads(r_post_data)
                # print(r_post_data)
                user_data = response['data']
            user_id = response['data']['id']
            try:
                location = response['data']['locations']
            except KeyError:
                print(True)
                bot.sendMessage(chat_id, '*Write "/location (your location)" or "/l" to set default location !*',
                                parse_mode='Markdown')
                location= None
                return

        if not location:
            return

        result =get_weather_meteo(response['data']['locations'])
        weather_d =result["ForAllDay"]
        # weather_days= weather_d['days'] + weather_d['wind']
        # weather_day = 'Today'+'🏙️ : '+response['data']['locations']
        weather_list = result['ForAllDay']
        # for weather_d in weather_list:
        #     weather_d['wind']
        # print(weather_d['humidity'])
        print(weather_list)
        night = weather_list[0]
        morning= weather_list[1]
        day=weather_list[2]
        evening = weather_list[3]
        night_weather = '           🌃 '+'<b>Ніч</b>'+' 🌃' + '\n' + 'Стан : '+night['status'] +'\n'+ '🌡️ : ' +night['temp']+'\n'+ '⛆ : ' + night['humidity']+'\n'+'↕️ : ' +night['pressure']+'мм рт.ст.'+'\n'+ '🌧️ : '+night['precipitation']+'\n'+'💨 : '+ night['wind']
        morning_weather = '       🏙️ : '+response['data']['locations']+'\n'+ '          🌄 '+'<b>Ранок</b>'+' 🌄'+  '\n' + 'Стан : '+morning['status'] +'\n'+ '🌡️ : ' +morning['temp']+'\n'+ '⛆ : ' + morning['humidity']+'\n'+'↕️ : ' +morning['pressure']+'мм рт.ст.'+'\n'+ '🌧️ : '+morning['precipitation']+'\n'+'💨 : '+ morning['wind']
        day_weather = '          ☀️ '+'<b>День</b>' + ' ☀️'+ '\n' + 'Стан : '+day['status'] +'\n'+ '🌡️ : ' +day['temp']+'\n'+ '⛆ : ' + day['humidity']+'\n'+'↕️ : ' +day['pressure']+'мм рт.ст.'+'\n'+ '🌧️ : '+day['precipitation']+'\n'+'💨 : '+ day['wind']
        evening_weather = '          🌆 '+'<b>Вечір</b>'+ ' 🌆' + '\n' + 'Стан : '+evening['status'] +'\n'+ '🌡️ : ' +evening['temp']+'\n'+ '⛆ : ' + evening['humidity']+'\n'+'↕️ : ' +evening['pressure']+'мм рт.ст.'+'\n'+ '🌧️ : '+evening['precipitation']+'\n'+'💨 : '+ evening['wind']
        # _morning = 'Today'+'🏙️ : '+response['data']['locations']+'\n'+weather_d['days_morning']+weather_d['status_morning'] + weather_d['temp_morning']+weather_d['feels_morning']+ weather_d['humidity_morning'] +weather_d['pressure_morning']  +weather_d['wind_morning']+weather_d['precipitation_morning']
        # _morning = weather_d['days_morning']+weather_d['status_morning'] + weather_d['temp_morning']+weather_d['feels_morning']+ weather_d['humidity_morning'] +weather_d['pressure_morning']  +weather_d['wind_morning']+weather_d['precipitation_morning']
        # _morning = weather_d['days_morning']+weather_d['status_morning'] + weather_d['temp_morning']+weather_d['feels_morning']+ weather_d['humidity_morning'] +weather_d['pressure_morning']  +weather_d['wind_morning']+weather_d['precipitation_morning']
        # _morning = weather_d['days_morning']+weather_d['status_morning'] + weather_d['temp_morning']+weather_d['feels_morning']+ weather_d['humidity_morning'] +weather_d['pressure_morning']  +weather_d['wind_morning']+weather_d['precipitation_morning']
        day_weather=morning_weather+'\n'+day_weather+'\n'+evening_weather+'\n'+night_weather
        bot.sendMessage(chat_id, day_weather, parse_mode='HTML')
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


    elif command == '🔧 Settings 🔧':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🌐 Languages 🌐')],[ KeyboardButton(text='🔙 Back 🔙')]
        ])
        bot.sendMessage(chat_id, '*Set up your bot*', reply_markup=markup, parse_mode='Markdown')
    elif command == '🔙 Back 🔙':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='📆 Show Weather 📆')],
            [KeyboardButton(text='🔧 Settings 🔧')],
        ])
        bot.sendMessage(chat_id, '*you returned back*', reply_markup=markup, parse_mode='Markdown')
    # elif command == '📝 units 📝':
    #     markup = ReplyKeyboardMarkup(keyboard=[
    #     [KeyboardButton(text='celsium(°C)'), KeyboardButton(text='fahrenheit(°F)', )],
    #     [KeyboardButton(text='❌ cancel ❌')],
    #     ])
    #     bot.sendMessage(chat_id, '*Choose Celsium or Fahrenheit*', reply_markup=markup, parse_mode='Markdown')
    elif command == '❌ Cancel ❌':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🌐 Languages 🌐')],[ KeyboardButton(text='🔙 Back 🔙')]
        ])
        bot.sendMessage(chat_id, '*Set up your bot*', reply_markup=markup, parse_mode='Markdown')
    # if command == 'celsium(°c)':
    #     markup = ReplyKeyboardMarkup(keyboard=[
    #     [KeyboardButton(text='🗓️ current weather 🗓️'), KeyboardButton(text='📅 weekly weather 📅',)],
    #     [KeyboardButton(text='🔧 settings 🔧')],
    #     ])
    #     bot.sendMessage(chat_id, '*Units now are metric(celsium)*', reply_markup=markup, parse_mode='Markdown')
    # if command == 'fahrenheit(°f)':
    #     markup = ReplyKeyboardMarkup(keyboard=[
    #     [KeyboardButton(text='🗓️ current weather 🗓️'), KeyboardButton(text='📅 weekly weather 📅',)],
    #     [KeyboardButton(text='🔧 settings 🔧')],
    #     ])
    #     bot.sendMessage(chat_id, '*Units now are imperial(fahrenheit)*', reply_markup=markup, parse_mode='Markdown')
    if command == '🌐 Languages 🌐':
        markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🏴󠁧󠁢󠁥󠁮󠁧󠁿 English 🏴󠁧󠁢󠁥󠁮󠁧󠁿'), KeyboardButton(text='🇺🇦 Українська 🇺🇦')],
        ['❌ Cancel ❌']
        ])
        bot.sendMessage(chat_id, '*Choose language*', reply_markup=markup, parse_mode='Markdown')
    if command == '🏴󠁧󠁢󠁥󠁮󠁧󠁿 English 🏴󠁧󠁢󠁥󠁮󠁧󠁿':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='📆 Show Weather 📆')],
            [KeyboardButton(text='🔧 Settings 🔧')],
        ])
        # bot.sendMessage(chat_id, "", parse_mode='HTML')
        bot.sendMessage(chat_id, '*HI!*', reply_markup=markup, parse_mode='Markdown')

        #ukrainian section












    if command == '🇺🇦 Українська 🇺🇦':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='📆 Показати Погоду 📆')],
            [KeyboardButton(text='🔧 Налаштування 🔧')],
        ])
        # bot.sendMessage(chat_id, "", parse_mode='HTML')
        bot.sendMessage(chat_id, '*Привіт!*', reply_markup=markup, parse_mode='Markdown')

    elif command == '📆 Показати Погоду 📆':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='🗓️ Теперішня Погода 🗓️'), KeyboardButton(text='📅 Погода на день 📅', )],
            [KeyboardButton(text='🔙 Назад 🔙')],
        ])
        bot.sendMessage(chat_id, "Виберіть погоду", reply_markup=markup, parse_mode='HTML')
    elif msg['text'].startswith('/location'):
        r_get = requests.get('http://127.0.0.1:8002/person?telegram_id={}'.format(msg['from']['id']))
        response = r_get.json()
        response = json.loads(response)
        location = msg['text'].replace('/location', '').lower()
        location = location.strip()
        data = {'id': response['data']['id'], 'user_tag': msg['from']['first_name'], 'telegram_id': msg['from']['id']
            , 'locations': location}
        r_put = requests.put('http://127.0.0.1:8002/person', data=data)
        loc = 'Ваша локація змінена на : ' + location
        bot.sendMessage(chat_id, loc)
    elif msg['text'].startswith('/l'):
        r_get = requests.get('http://127.0.0.1:8002/person?telegram_id={}'.format(msg['from']['id']))
        response = r_get.json()
        response = json.loads(response)
        location = msg['text'].replace('/l', '').lower()
        location = location.strip()
        data = {'id': response['data']['id'], 'user_tag': msg['from']['first_name'], 'telegram_id': msg['from']['id']
            , 'locations': location}
        r_put = requests.put('http://127.0.0.1:8002/person', data=data)
        loc = 'Ваша локація змінена на : ' + location
        bot.sendMessage(chat_id, loc)
    elif command == '🗓️ Теперішня Погода 🗓️':
        r_get = requests.get('http://127.0.0.1:8002/person?telegram_id={}'.format(msg['from']['id']))
        response = r_get.json()
        response = json.loads(response)
        print('response = {}'.format(response))
        if not response['is_error']:
            if not response['data']:
                data = {'user_tag': msg['from']['first_name'], 'telegram_id': msg['from']['id']}
                r_post = requests.post('http://127.0.0.1:8002/person', data=data)
                # print(r_post)
                r_post_data = r_post.json()
                response = json.loads(r_post_data)
                # print(r_post_data)
                user_data = response['data']
            user_id = response['data']['id']
            if response['data']['locations'] == None:
                bot.sendMessage(chat_id, '*Напишіть "/location (ваша локація)" або "/l",щоб змінити стандартну локацію !*',
                                parse_mode='Markdown')

        # result= requests.get('http://127.0.0.1:8002/weather?city={}'.format(user_location))
        # result =json.loads(result.json())
        # user_location = response['data']['locations']

        result = get_weather_meteo(response['data']['locations'])
        now = result['Now']
        # print(now)
        # weather_now = now['statusnow'] +'\n' +now['tempnow'] + '\n' + 'Вітер : ' + now['windnow'] +'\n' +now['minmaxtempdays']
        # tempnow = now['tempnow'].replace('Сьогодні о ','')
        minmax1 = now['minmaxtempdays'].replace('мін.', 'мін. ')
        minmax = minmax1.replace('макс.', 'макс. ')
        split_index = now['tempnow'].find('+') if now['tempnow'].find('+') != -1 else now['tempnow'].find('-')
        time_now = now['tempnow'][:split_index]
        temp_now = now['tempnow'][split_index:]
        # weather_now = time_now+' : ' + '\n' + '🌡️ : ' + temp_now+ '💨 : ' + now['windnow'] +'\n' + '🌡️ : ' +minmax+ '\n'  +'☀ : ️'+now['statusnow']
        weather_now = time_now + ' : ' '\n' + '🏙️ : ' + response['data']['locations'] + '\n' + 'Стан : ️' + now[
            'statusnow'] + '\n' + '🌡️ : ' + temp_now + '\n' + '💨 : ' + now['windnow']
        bot.sendMessage(chat_id, weather_now, parse_mode='HTML')

    elif command == '📅 Погода на день 📅':
        r_get = requests.get('http://127.0.0.1:8002/person?telegram_id={}'.format(msg['from']['id']))
        response = r_get.json()
        response = json.loads(response)
        # print('response = {}'.format(response))
        if not response['is_error']:
            if not response['data']:
                data = {'user_tag': msg['from']['first_name'], 'telegram_id': msg['from']['id']}
                r_post = requests.post('http://127.0.0.1:8002/person', data=data)
                # print(r_post)
                r_post_data = r_post.json()
                response = json.loads(r_post_data)
                # print(r_post_data)
                user_data = response['data']
            user_id = response['data']['id']
            if response['data']['locations'] == None:
                bot.sendMessage(chat_id, '*Напишіть "/location (ваша локація )" або "/l",щоб змінити стандартну локацію !*',
                                parse_mode='Markdown')
        result = get_weather_meteo(response['data']['locations'])
        weather_d = result["ForAllDay"]
        # weather_days= weather_d['days'] + weather_d['wind']
        # weather_day = 'Today'+'🏙️ : '+response['data']['locations']
        weather_list = result['ForAllDay']
        # for weather_d in weather_list:
        #     weather_d['wind']
        # print(weather_d['humidity'])
        print(weather_list)
        night = weather_list[0]
        morning = weather_list[1]
        day = weather_list[2]
        evening = weather_list[3]
        night_weather = '           🌃 ' + '<b>Ніч</b>' + ' 🌃' + '\n' + 'Стан : ' + night['status'] + '\n' + '🌡️ : ' + \
                        night['temp'] + '\n' + '⛆ : ' + night['humidity'] + '\n' + '↕️ : ' + night[
                            'pressure'] + 'мм рт.ст.' + '\n' + '🌧️ : ' + night['precipitation'] + '\n' + '💨 : ' + \
                        night['wind']
        morning_weather = '       🏙️ : ' + response['data'][
            'locations'] + '\n' + '          🌄 ' + '<b>Ранок</b>' + ' 🌄' + '\n' + 'Стан : ' + morning[
                              'status'] + '\n' + '🌡️ : ' + morning['temp'] + '\n' + '⛆ : ' + morning[
                              'humidity'] + '\n' + '↕️ : ' + morning['pressure'] + 'мм рт.ст.' + '\n' + '🌧️ : ' + \
                          morning['precipitation'] + '\n' + '💨 : ' + morning['wind']
        day_weather = '          ☀️ ' + '<b>День</b>' + ' ☀️' + '\n' + 'Стан : ' + day['status'] + '\n' + '🌡️ : ' + \
                      day['temp'] + '\n' + '⛆ : ' + day['humidity'] + '\n' + '↕️ : ' + day[
                          'pressure'] + 'мм рт.ст.' + '\n' + '🌧️ : ' + day['precipitation'] + '\n' + '💨 : ' + day[
                          'wind']
        evening_weather = '          🌆 ' + '<b>Вечір</b>' + ' 🌆' + '\n' + 'Стан : ' + evening[
            'status'] + '\n' + '🌡️ : ' + evening['temp'] + '\n' + '⛆ : ' + evening['humidity'] + '\n' + '↕️ : ' + \
                          evening['pressure'] + 'мм рт.ст.' + '\n' + '🌧️ : ' + evening[
                              'precipitation'] + '\n' + '💨 : ' + evening['wind']
        # _morning = 'Today'+'🏙️ : '+response['data']['locations']+'\n'+weather_d['days_morning']+weather_d['status_morning'] + weather_d['temp_morning']+weather_d['feels_morning']+ weather_d['humidity_morning'] +weather_d['pressure_morning']  +weather_d['wind_morning']+weather_d['precipitation_morning']
        # _morning = weather_d['days_morning']+weather_d['status_morning'] + weather_d['temp_morning']+weather_d['feels_morning']+ weather_d['humidity_morning'] +weather_d['pressure_morning']  +weather_d['wind_morning']+weather_d['precipitation_morning']
        # _morning = weather_d['days_morning']+weather_d['status_morning'] + weather_d['temp_morning']+weather_d['feels_morning']+ weather_d['humidity_morning'] +weather_d['pressure_morning']  +weather_d['wind_morning']+weather_d['precipitation_morning']
        # _morning = weather_d['days_morning']+weather_d['status_morning'] + weather_d['temp_morning']+weather_d['feels_morning']+ weather_d['humidity_morning'] +weather_d['pressure_morning']  +weather_d['wind_morning']+weather_d['precipitation_morning']
        day_weather = morning_weather + '\n' + day_weather + '\n' + evening_weather + '\n' + night_weather
        bot.sendMessage(chat_id, day_weather, parse_mode='HTML')
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

    elif command == '🔧 Налаштування 🔧':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='🌐 Мови 🌐')], [KeyboardButton(text='🔙 Назад 🔙')]
        ])
        bot.sendMessage(chat_id, '*Налаштуйте свого бота*', reply_markup=markup, parse_mode='Markdown')
    elif command == '🔙 Назад 🔙':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='📆 Показати Погоду 📆')],
            [KeyboardButton(text='🔧 Налаштування 🔧')],
        ])
        bot.sendMessage(chat_id, '*Ви повернулись назад*', reply_markup=markup, parse_mode='Markdown')
    # elif command == '📝 units 📝':
    #     markup = ReplyKeyboardMarkup(keyboard=[
    #     [KeyboardButton(text='celsium(°C)'), KeyboardButton(text='fahrenheit(°F)', )],
    #     [KeyboardButton(text='❌ cancel ❌')],
    #     ])
    #     bot.sendMessage(chat_id, '*Choose Celsium or Fahrenheit*', reply_markup=markup, parse_mode='Markdown')
    elif command == '❌ Відмінити ❌':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='🌐 Мови 🌐')], [KeyboardButton(text='🔙 Назад 🔙')]
        ])
        bot.sendMessage(chat_id, '*Налаштуйте свого бота*', reply_markup=markup, parse_mode='Markdown')
    # if command == 'celsium(°c)':
    #     markup = ReplyKeyboardMarkup(keyboard=[
    #     [KeyboardButton(text='🗓️ current weather 🗓️'), KeyboardButton(text='📅 weekly weather 📅',)],
    #     [KeyboardButton(text='🔧 settings 🔧')],
    #     ])
    #     bot.sendMessage(chat_id, '*Units now are metric(celsium)*', reply_markup=markup, parse_mode='Markdown')
    # if command == 'fahrenheit(°f)':
    #     markup = ReplyKeyboardMarkup(keyboard=[
    #     [KeyboardButton(text='🗓️ current weather 🗓️'), KeyboardButton(text='📅 weekly weather 📅',)],
    #     [KeyboardButton(text='🔧 settings 🔧')],
    #     ])
    #     bot.sendMessage(chat_id, '*Units now are imperial(fahrenheit)*', reply_markup=markup, parse_mode='Markdown')
    if command == '🌐 Мови 🌐':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='🏴󠁧󠁢󠁥󠁮󠁧󠁿 English 🏴󠁧󠁢󠁥󠁮󠁧󠁿'), KeyboardButton(text='🇺🇦 Українська 🇺🇦')],
            ['❌ Відмінити ❌']
        ])
        bot.sendMessage(chat_id, '*Виберіть мову*', reply_markup=markup, parse_mode='Markdown')

        # ukrainian section


# TOKEN = '577877864:AAEh1MKE62KPntQjSuEtH53sDYJDes3oYyM'
TOKEN = "587773115:AAFrW2NWni5052mgSeQBA136aFeqL9nrT-A"
bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)
try:
    MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()
except:
    print('error')

print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)


