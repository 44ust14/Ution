# -*- coding:utf-8 -*-
from flask import Flask, request
import requests
import bs4, requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def search_meteo(text):
    response = requests.post('http://meteo.ua/ua/search-forecast-by-city-name', data={'name': text})
    b = bs4.BeautifulSoup(response.text, "html.parser")
    p3 = b.select('.main_cont p a')
    # print(response.history)
    # for r in response.history:
    #     print(r.url)
    # with open('data.html', 'w') as f:
    #     f.write(response.text.replace('\u2602','').replace('\ufeff',''))
    if not p3:
        result = parse(response=response)
        return result
    # print(p3)
    hrefs = p3[0]['href']
    # print(hrefs)
    result = parse(hrefs=hrefs)
    # print(result)
    return result


def parse(hrefs=None, response=None):
    if hrefs:
        response = requests.get('http://meteo.ua{}'.format(hrefs))
    # s = requests.get('http://meteo.ua/ua/44/lvov')
    b = bs4.BeautifulSoup(response.text, "html.parser")
    result = {}
    Now = {}
    For_All_Day = []
    City = {}
    p3 = b.select('.wi_now')
    tempnow = p3[0].getText().strip().replace('\n', '')
    # print(tempnow.strip())

    p3 = b.select('.wiw_power')
    windnow = p3[0].getText().strip().replace('\n', '')
    # print(windnow.strip())

    p3 = b.select('.win_img img')
    statsnow = p3[1]["title"].strip().replace('\n', '')
    # print(statsnow.strip())

    p3 = b.select('.wwt_tmps')
    minmaxtempdays = p3[0].getText().strip().replace('\n', '')
    # print(minmaxtempdays.strip())

    Now.update(tempnow=tempnow, windnow=windnow, statusnow=statsnow, minmaxtempdays=minmaxtempdays)

    p3 = b.select('.wnow_cnt .wnow_days ')
    daysnight = p3[0].getText().strip().replace('\n', '')
    # print(daysnight.strip())

    p3 = b.select('.wnow_cnt .wnow_tmpr')
    tempnight = p3[0].getText().strip().replace('\n', '')
    # print(tempnight.strip())

    p3 = b.select('.wnow_cnt .wnow_icns img')
    statsnight = p3[1]["title"].strip().replace('\n', '')
    # print(statsnight.strip())

    p3 = b.select('.wni_left')
    feelsnight = p3[1].getText().strip().replace('\n', '')
    # print(feelsnight.strip())

    p3 = b.select('.wni_left')
    precipitationnight = p3[2].getText().strip().replace('\n', '')
    # print(precipitationnight.strip())

    p3 = b.select('.wni_left')
    pressurenight = p3[3].getText().strip().replace('\n', '')
    # print(pressurenight.strip())

    p3 = b.select('.wni_left')
    humiditynight = p3[4].getText().strip().replace('\n', '')
    # print(humiditynight.strip())

    p3 = b.select('.wni_left')
    windnight = p3[5].getText().strip().replace('\n', '')
    # print(windnight.strip())

    For_All_Day_night = {}

    For_All_Day_night.update(days=daysnight, temp=tempnight, status=statsnight, feels=feelsnight,
                             precipitation=precipitationnight, pressure=pressurenight,
                             humidity=humiditynight, wind=windnight)
    For_All_Day.append(For_All_Day_night)

    p3 = b.select('.wnow_cnt .wnow_days')
    daysmorning = p3[2].getText().strip().replace('\n', '')
    # print(daysmorning.strip())

    p3 = b.select('.wnow_cnt .wnow_tmpr')
    tempmorning = p3[1].getText().strip().replace('\n', '')
    # print(tempmorning.strip())

    p3 = b.select('.wnow_cnt .wnow_icns img')
    statsmorning = p3[1]["title"].strip().replace('\n', '')
    # print(statsmorning)

    p3 = b.select('.wnow_info td div')
    feelsmorning = p3[1].getText().strip().replace('\n', '')
    # print(feelsmorning.strip())

    wnow_infos = b.select('.wnow_info')
    p3 = wnow_infos[1].select('td div')[2]
    precipitationmorning = p3.getText().strip().replace('\n', '')
    # print(precipitationmorning.strip())

    wnow_info = b.select('.wnow_info')
    p3 = wnow_info[2].select('td div')[2]
    pressuremorning = p3.getText().strip().replace('\n', '')
    # print(pressuremorning.strip())

    wnow_infos = b.select('.wnow_info')
    p3 = wnow_infos[3].select('td div')[1]
    humiditymorning = p3.getText().strip().replace('\n', '')
    # print(humiditymorning.strip())

    wnow_infos = b.select('.wnow_info')
    p3 = wnow_infos[4].select('td div')[1]
    windmorning = p3.getText().strip().replace('\n', '')
    # print(windmorning.strip())

    For_All_Day_morning = {}

    For_All_Day_morning.update(days=daysmorning, temp=tempmorning,
                               status=statsmorning, feels=feelsmorning,
                               precipitation=precipitationmorning,
                               pressure=pressuremorning, humidity=humiditymorning,
                               wind=windmorning)
    For_All_Day.append(For_All_Day_morning)

    p3 = b.select('.wnow_cnt .wnow_days')
    daysday = p3[2].getText().strip().replace('\n', '')
    # print(daysday.strip())

    p3 = b.select('.wnow_cnt .wnow_tmpr')
    tempday = p3[2].getText().strip().replace('\n', '')
    # print(tempday.strip())

    p3 = b.select('.wnow_cnt .wnow_icns img')
    statsday = p3[1]["title"].strip().replace('\n', '')
    # print(statsday.strip())

    p3 = b.select('.wnow_info td div')
    feelsday = p3[1].getText().strip().replace('\n', '')
    # print(feelsday.strip())

    wnow_infos = b.select('.wnow_info')
    p3 = wnow_infos[1].select('td div')[2]
    precipitationday = p3.getText().strip().replace('\n', '')
    # print(precipitationday.strip())

    wnow_info = b.select('.wnow_info')
    p3 = wnow_info[2].select('td div')[2]
    pressureday = p3.getText().strip().replace('\n', '')
    # print(pressureday.strip())

    wnow_infos = b.select('.wnow_info')
    p3 = wnow_infos[3].select('td div')[2]
    humidityday = p3.getText().strip().replace('\n', '')
    # print(humidityday.strip())

    wnow_infos = b.select('.wnow_info')
    p3 = wnow_infos[4].select('td div')[2]
    windday = p3.getText().strip().replace('\n', '')
    # print(windday.strip())

    For_All_Day_day = {}

    For_All_Day_day.update(days=daysday, temp=tempday,
                           status=statsday, feels=feelsday, precipitation=precipitationday,
                           pressure=pressureday, humidity=humidityday, wind=windday)
    For_All_Day.append(For_All_Day_day)

    p3 = b.select('td .wnow_days')
    daysevening = p3[3].getText().strip().replace('\n', '')
    # print(daysevening.strip())

    p3 = b.select('.wnow_cnt .wnow_tmpr')
    tempevening = p3[3].getText().strip().replace('\n', '')
    # print(tempevening.strip())

    p3 = b.select('.wnow_cnt .wnow_icns img')
    statsevening = p3[3]["title"].strip().replace('\n', '')
    # print(statsevening.strip())

    p3 = b.select('.wnow_info td div')
    feelsevening = p3[3].getText().strip().replace('\n', '')
    # print(feelsevening.strip())

    wnow_infos = b.select('.wnow_info')
    p3 = wnow_infos[1].select('td div')[3]
    precipitationevening = p3.getText().strip().replace('\n', '')
    # print(precipitationevening.strip())

    wnow_info = b.select('.wnow_info')
    p3 = wnow_info[2].select('td div')[3]
    pressureevening = p3.getText().strip().replace('\n', '')
    # print(pressureevening.strip())

    wnow_infos = b.select('.wnow_info')
    p3 = wnow_infos[3].select('td div')[3]
    humidityevening = p3.getText().strip().replace('\n', '')
    # print(humidityevening.strip())

    wnow_infos = b.select('.wnow_info')
    p3 = wnow_infos[4].select('td div')[3]
    windevening = p3.getText().strip().replace('\n', '')
    # print(windevening.strip())

    For_All_Day_evening = {}

    For_All_Day_evening.update(days=daysevening, temp=tempevening,
                               status=statsevening, feels=feelsevening,
                               precipitation=precipitationevening,
                               pressure=pressureevening, humidity=humidityevening,
                               wind=windevening)
    For_All_Day.append(For_All_Day_evening)

    p3 = b.select('.wwt_tmps')
    minmaxtempdays = p3[0].getText().strip().replace('\n', '')
    # print(minmaxtempdays.strip())

    p3 = b.select('#dt_today > a > div.wwt_img.vl_parent > span.vl_child > span > img')
    statsdays = p3[0]["title"].strip().replace('\n', '')
    # print(statsdays.strip())

    City.update(minmaxtempdays=minmaxtempdays, statsdays=statsdays, site='meteo.ua')
    # print(result)

    result.update(Now=Now)
    result.update(ForAllDay=For_All_Day)
    result.update(City=City)
    return result


def get_weather_meteo(text):
    return search_meteo(text)


if __name__ == '__main__':
    print('result = {}'.format(get_weather_meteo("Львів")))

# class UnprocessedApi(resourse):
#     def post(self):
#         city_or_country = request.form["city_or_country"] string
#         tempMax = request.form['tempMax'] int
#         tempMin = request.form['tempmin'] int
#         tempnow = request.form['tempnow'] int
#         wind = request.form['windnow'] int
#         feels = request.form['feelsnow']
#         status = request.form['statusnow']
#         notes = request.form['notes']
#         site = request.form['http://meteo.ua']
#         timenow = request.form['timenow']
#
#
#         days = request.form['daysnight']
#         temp = request.form['tempnight']
#         status = request.form['statusnight']
#         feels = request.form['feelsnight']
#         precipitation = request.form['precipitationnight']
#         pressure = request.form['pressurenight']
#         humidity = request.form['humiditynight']
#         wind = request.form['windnight']
#         timenow = request.form['timenow']
#
#         days = request.form['daysmorining']
#         temp = request.form['tempmorining']
#         status = request.form['statusmorining']
#         feels = request.form['feelmsorining']
#         precipitation = request.form['precipitationmorining']
#         pressure = request.form['pressuremorining']
#         humidity = request.form['humiditymorining']
#         wind = request.form['windmorining']
#         site = request.form['http://meteo.ua']
#         timenow = request.form['timenow']
#
#
#         days = request.form['daysday']
#         temp = request.form['tempday']
#         status = request.form['statusday']
#         feels = request.form['feelsday']
#         precipitation = request.form['precipitationday']
#         pressure = request.form['pressureday']
#         humidity = request.form['humidityday']
#         wind = request.form['windday']
#         site = request.form['http://meteo.ua']
#         timenow = request.form['timenow']
#
#         daysevening = request.form['daysevening']
#         temp = request.form['tempevening']
#         status = request.form['statusevening']
#         feels = request.form['feelsevening']
#         precipitation = request.form['precipitationevening']
#         pressure = request.form['pressureevening']
#         hymidity = request.form['hymidityevening']
#         wind = request.form['windevening']
#         site = request.form['http://meteo.ua']
#         timenow = request.form['timenow']
#
#         minmaxtempdays = request.form['minmaxtempdays']
#         statdays = request.form['statdays']
#         site = request.form['http://meteo.ua']
#         timenow = request.form['timenow']
