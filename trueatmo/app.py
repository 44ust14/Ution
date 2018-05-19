# -*- coding:utf-8 -*-
import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:\\Users\\GOITeens\\Neeew ution\\my_db.db"
# "C:\\Users\\GOITeens\\Neeew ution"
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


class Unprocessed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_or_country = db.Column(db.String(80))
    Cmin = db.Column(db.Integer)
    Cmax = db.Column(db.Integer)
    Ccur = db.Column(db.Integer)
    status = db.Column(db.String(80))
    wind = db.Column(db.Integer)
    site = db.Column(db.String(80))
    time = db.Column(db.Integer)

    def __init__(self, city_or_country, Cmin, Cmax, Ccur, status, wind, site, time, id=None):
        self.id = id
        self.city_or_country = city_or_country
        self.Cmin = Cmin
        self.Cmax = Cmax
        self.Ccur = Ccur
        self.status = status
        self.Ccur = Ccur
        self.wind = wind
        self.site = site
        self.time = time

    def __repr__(self):
        return '<Unprocessed %r>' % self.status


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


class Processed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_or_country = db.Column(db.String(80))
    Cmin = db.Column(db.Integer)
    Cmax = db.Column(db.Integer)
    Ccur = db.Column(db.Integer)
    status = db.Column(db.String(80))
    wind = db.Column(db.Integer)
    time = db.Column(db.Integer)

    def __init__(self, city_or_country, Cmin, Cmax, Ccur, status, wind, time, id=None):
        self.id = id
        self.city_or_country = city_or_country
        self.Cmin = Cmin
        self.Cmax = Cmax
        self.Ccur = Ccur
        self.status = status
        self.Ccur = Ccur
        self.wind = wind
        self.time = time

    def __repr__(self):
        return '<Processed %r>' % self.city_or_country


class UnprocessedApi(Resource):
    def get(self):
        city_or_country = request.args['city_or_country']
        Cmin = request.args['Cmin']
        Cmax = request.args['Cmax']
        Ccur = request.args['Ccur']
        status = request.args['status']
        wind = request.args['wind']
        site = request.args['site']
        time = request.args['time']
        user = User.query.filter_by(city_or_country=city_or_country, ).first()
        return jsonify({'Cmin': Cmin})

    def post(self):
        city_or_country = request.form['city_or_country']
        Cmin = request.form['Cmin']
        Cmax = request.form['Cmax']
        Ccur = request.form['Ccur']
        status = request.form['status']
        wind = request.form['wind']
        site = request.form['site']
        time = request.form['time']
        row = Unprocessed(city_or_country, Cmin, Cmax, Ccur, status, wind, site, time)
        db.session.add(row)
        db.session.commit()
        return {'status': 'ok'}




class UserApi(Resource):
    def wait(self):
    def get(self):
        try:
            telegram_id = request.args.get('telegram_id')
            user = User.query.filter_by(telegram_id=telegram_id).first()
            data= {}
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
            id = request.form.get['id']
            user_tag = request.form.get['user_tag']
            telegram_id = request.form.get['telegram_id']
            locations = request.form.get['locations']
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
        db.create_all()
        return 'OK'


api.add_resource(UserApi, '/person')
api.add_resource(ManagerDBApi, '/manager')
api.add_resource(UnprocessedApi, '/unprocessed')

if __name__ == '__main__':
    app.run(debug=True, port=8002)
