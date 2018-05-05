# -*- coding:utf-8 -*-
import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

DBUSER = 'trueatmo'
DBPASS = '1q2w3e'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'trueatmo'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}".format(user=DBUSER,
                                                                      passwd=DBPASS,
                                                                      host=DBHOST,
                                                                      port=DBPORT,
                                                                      db=DBNAME)
db = SQLAlchemy(app)


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
    def get(self, telegram_id):
        user = User.query.filter_by(telegram_id=telegram_id).first()
        respons = {'id': user.id,
                   'user_tag': user.user_tag,
                   'telegram_id': user.telegram_id,
                   'locations': user.locations}
        return json.dumps(respons)

    def post(self):
        user_tag = request.form['user_tag']
        telegram_id = request.form['telegram_id']
        locations = request.form['locations']
        user = User(user_tag=user_tag, locations=locations,telegram_id=telegram_id)
        db.session.add(user)
        db.session.commit()
        return json.dumps({'status': 'ok'})


class ManagerDBApi(Resource):
    def post(self):
        db.create_all()
        return {'status': 'ok'}

    def get(self):
        return 'OK'


api.add_resource(UserApi, '/person')
api.add_resource(ManagerDBApi, '/manager')
api.add_resource(UnprocessedApi, '/unprocessed')

if __name__ == '__main__':
    app.run(debug=True, port=8001, host='0.0.0.0')
