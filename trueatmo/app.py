# -*- coding:utf-8 -*-
import json
from datetime import datetime, timedelta
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from meteo import get_weather_meteo

app = Flask(__name__)
api = Api(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:\\Users\\GOITeens\\Neeew ution\\my_db.db"
# "C:\\Users\\GOITeens\\Neeew ution"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main_db.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# DBUSER = 'trueatmo'
# DBPASS = '1q2w3e'
# DBHOST = 'db'
# DBPORT = '5432'
# DBNAME = 'trueatmo'
#
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}".format(user=DBUSER,
#                                                                       passwd=DBPASS,
#                                                                       host=DBHOST,
#                                                                       port=DBPORT,
#                                                                       db=DBNAME)
# db = SQLAlchemy(app)


class Now(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tempMax = db.Column(db.Integer)
    tempMin = db.Column(db.Integer)
    tempnow = db.Column(db.Integer)
    minmaxtempdays = db.Column(db.String(80))
    windnow = db.Column(db.Integer)
    feels = db.Column(db.String(80))
    statusnow = db.Column(db.String(80))
    notes = db.Column(db.String(80))
    timenow = db.Column(db.Integer, default=int(datetime.now().timestamp()))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))

    def __repr__(self):
        return '<Now %r>' % self.status


class ForAllDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_part = db.Column(db.String(80))
    days = db.Column(db.String(80))
    temp = db.Column(db.Integer)
    status = db.Column(db.String(80))
    feels = db.Column(db.Integer)
    precipitation = db.Column(db.Integer)
    pressure = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    wind = db.Column(db.Integer)
    timenow = db.Column(db.Integer, default=int(datetime.now().timestamp()))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))

    def __repr__(self):
        return '<Day %r>' % self.status


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80))
    minmaxtempdays = db.Column(db.String(80))
    statsdays = db.Column(db.String(80))
    site = db.Column(db.String(80))
    timenow = db.Column(db.Integer, default=int(datetime.now().timestamp()))
    addresses = db.relationship('ForAllDay', backref='city',
                                lazy='dynamic')

    def __repr__(self):
        return '<Next_Day %r>' % self.statsdays


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_tag = db.Column(db.String(50))
    telegram_id = db.Column(db.String(50))
    locations = db.Column(db.String(80))

    def __init__(self, telegram_id, user_tag, locations, id=None):
        self.id = id
        self.telegram_id = telegram_id
        self.user_tag = user_tag
        self.locations = locations

    def __repr__(self):
        return '<User %r>' % self.user_tag


class WeatherApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('tempMax', type=int)
    parser.add_argument('tempMin', type=int)
    parser.add_argument('tempnow', type=int)
    parser.add_argument('wind', type=int)
    parser.add_argument('feels', type=str)
    parser.add_argument('status', type=str)
    parser.add_argument('notes', type=str)
    parser.add_argument('site', type=str)
    parser.add_argument('timenow', type=int)
    parser.add_argument('city_id', type=int)

    parser = reqparse.RequestParser()
    parser.add_argument('user_tag', type=int, help='Rate cannot be converted')
    parser.add_argument('name')

    def post(self):
        try:
            return json.dumps({'status': 'ok'})
        except Exception as error:
            response = {'is_error': 1,
            'error_log': str(error)}
        return json.dumps(response)

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city', type=str)
        args = parser.parse_args()
        location = args.city
        city = City.query.filter_by(city=location).first()

        if city and datetime.fromtimestamp(city.timenow) >= datetime.now() - timedelta(minutes=15):
            now = Now.query.filter_by(city_id=city.id).first()
            forallday = ForAllDay.query.filter_by(city_id=city.id)
            data = {'City': row2dict(city),
                    'Now': row2dict(now),
                    'ForAllDay': rows2dict(forallday)}
            return json.dumps(data)
        data = get_weather_meteo(location)
        data['City'].update(city=location)
        city = City(**data['City'])
        db.session.add(city)
        db.session.commit()
        data['Now'].update(city_id=city.id)
        now = Now(**data['Now'])
        db.session.add(now)
        db.session.commit()
        for day_time in data['ForAllDay']:
            day_time.update(city_id=city.id)
            db.session.add(ForAllDay(**day_time))
            db.session.commit()
        return json.dumps(data)


class UserApi(Resource):
    def get(self):
        try:
            telegram_id = request.args.get('telegram_id')
            user = User.query.filter_by(telegram_id=telegram_id).first()
            data = {}
            if user:
                data = {'id': user.id,
                        'user_tag': user.user_tag,
                        'telegram_id': user.telegram_id,
                        'locations': user.locations}
            response = {'is_error': 0,
                        'data': data}

        except Exception as error:
            response = {'is_error': 1,
                        'error_log': str(error)}
        return json.dumps(response)

    def post(self):
        try:
            user_tag = request.form.get('user_tag')
            telegram_id = request.form.get('telegram_id')
            locations = request.form.get('locations')
            user = User(user_tag=user_tag, locations=locations, telegram_id=telegram_id)
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(telegram_id=telegram_id).first()
            data = {'id': user.id}
            response = {'is_error': 0,
                        'data': data}

        except Exception as error:
            response = {'is_error': 1,
                        'error_log': str(error)}
        print(response)
        return json.dumps(response)

    def put(self):
        try:
            id = request.form.get('id')
            user_tag = request.form.get('user_tag')
            telegram_id = request.form.get('telegram_id')
            locations = request.form.get('locations')
            user = User.query.filter_by(id=id).first()
            user.user_tag = user_tag
            user.telegram_id = telegram_id
            user.locations = locations
            db.session.add(user)
            db.session.commit()
            data = {'id': user.id}
            response = {'is_error': 0,
                        'data': data}

        except Exception as error:
            response = {'is_error': 1,
                        'error_log': str(error)}
        return json.dumps(response)


class ManagerDBApi(Resource):
    def post(self):
        db.create_all()
        return {'status': 'ok'}

    def get(self):
        db.drop_all()
        db.create_all()
        return 'OK'


def rows2dict(rows):
    return [row2dict(row) for row in rows]


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


api.add_resource(UserApi, '/person')
api.add_resource(ManagerDBApi, '/manager')
api.add_resource(WeatherApi, '/weather')

if __name__ == '__main__':
    app.run(debug=True, port=8002)
