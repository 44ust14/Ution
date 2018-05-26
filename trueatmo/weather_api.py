# -*- coding:utf-8 -*-
import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from meteo import get_weather_meteo
app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///databases\\main_db.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_tag = db.Column(db.String(50))
    locations = db.Column(db.String(80))


    def __init__(self, user_tag , locations, id=None):
        self.id = id
        self.user_tag = user_tag
        self.locations = locations


    def __repr__(self):
        return '<User %r>' % self.user_tag

class WeatherApi(Resource):
    class Now(Resource):
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
            response = {'is_error': 1,+
                        'error_log': str(error)}
        return json.dumps(response)

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city', type=str)
        args = parser.parse_args()
        location = args.city
        city = City.query.filter_by(city=location).first()

        if city and city.timenow >= datetime.now() - timedelta(minutes=15):
            now = Now.query.filter_by(city_id=city.id).first()
            forallday = ForAllDay.query.filter_by(city_id=city.id).first()
            return ()
        data = get_weather_meteo(location)

        return json.dumps(data)

class UserApi(Resource):
    def get(self, telegram_id):
      try:
        user = User.query.filter_by(telegram_id=telegram_id).first()
        response = {'id': user.id,
                   'user_tag': user.user_tag,
                   'telegram_id': user.telegram_id,
                   'locations': user.locations}
        return json.dumps(respons)
      except Exception as error:
            response = {'is_error': 1,
                        'error_log': str(error)}
        return json.dumps(response)

    def post(self):
      try:
      #  parser = reqparse.RequestParser()
      #  parser.add_argument('user_tag', type=int, help='Rate cannot be converted')
      #  parser.add_argument('name')
      # args = parser.parse_args()
        user_tag = request.form['user_tag']
        telegram_id = request.form['telegram_id']
        locations = request.form['locations']
        user = User(user_tag=user_tag, locations=locations,telegram_id=telegram_id)
        db.session.add(user)
        db.session.commit()
        return json.dumps({'status': 'ok'})
      except Exception as error:
            response = {'is_error': 1,
                        'error_log': str(error)}
        return json.dumps(response)


    def put(self):
      try:
        user_id = 1
        user = User.query.filter_by(id = user_id).first()
        user_tag = request.form['user_tag']
        telegram_id = request.form['telegram_id']
        locations = request.form['locations']
        id = request.form['id']
        user.user_tag = user_tag
        db.session.add(user)
        db.session.commit()
        return json.dumps({'status': 'ok'})
       except Exception as error:
            response = {'is_error': 1,
                        'error_log': str(error)}
        return json.dumps(response)

class ManagerDBApi(Resource):

        def post(self):
             db.create_all()
             return {'status': 'ok'}

api.add_resource(UserApi, '/person')
api.add_resource(ManagerDBApi, '/create_db')
api.add_resource(WeatherApi, '/weather')







if __name__ == '__main__':
    app.run(debug=True, port=2228)
