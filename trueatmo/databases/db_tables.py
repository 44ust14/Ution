from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./my_db.db'
db = SQLAlchemy(app)


class Now(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        tempMax = db.Column(db.Integer)
        tempMin = db.Column(db.Integer)
        tempnow = db.Column(db.Integer)
        wind = db.Column(db.Integer)
        feels = db.Column(db.String(80))
        status = db.Column(db.String(80))
        notes = db.Column(db.String(80))
        site = db.Column(db.String(80))
        timenow = db.Column(db.Integer)
        city_id = db.Column(db.Integer, db.ForeignKey('city.id') , primary_key=True)

        def __init__(self, id, tempMax , tempMin , tempnow , wind , feels , status, notes , site , timenow , city_id):
            self.id = id
            self.tempMax = tempMax
            self.tempMin = tempMin
            self.tempnow = tempnow
            self.wind = wind
            self.feels = feels
            self.status = status
            self.notes = notes
            self.site = site
            self.timenow = timenow
            self.city_id = city_id

        def __repr__(self):
            return '<Now %r>' % self.status

class ForAllDay(db.Model):
        id = db.Column(db.Integer , primary_key=True)
        day_part = db.Column(db.String(80))
        days = db.Column(db.String(80))
        temp = db.Column(db.Integer)
        status = db.Column(db.String(80))
        feels = db.Column(db.Integer)
        precipitation = db.Column(db.Integer)
        pressure = db.Column(db.Integer)
        humidity = db.Column(db.Integer)
        wind = db.Column(db.Integer)
        site = db.Column(db.String(80))
        timenow = db.Column(db.Integer)
        city_id = db.Column(db.Integer, db.ForeignKey('city.id'))

        def __init__(self, id, day_part , days , temp , status, feels , precipitation , pressure , humidity, wind , site , timenow , city_id):
            self.id = id
            self.day_part = day_part
            self.days = days
            self.status = status
            self.feels = feels
            self.precipitation = precipitation
            self.pressure = pressure
            self.humidity = humidity
            self.wind = wind
            self.site = site
            self.timenow = timenow
            self.city_id = city_id



        def __repr__(self):
            return '<Day %r>' % self.status

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80))
    minmaxtempdays = db.Column(db.Integer)
    statdays = db.Column(db.String(80))
    site = db.Column(db.String(80))
    timenow = db.Column(db.Integer)
    addresses = db.relationship('For_All_Day', backref='city',
                                lazy='dynamic')


    def __init__(self, id, city , minmaxtempdays , statdays ,site ,timenow ):
        self.id = id
        self.city = city
        self.minmaxtempdays = minmaxtempdays
        self.statdays = statdays
        self.site = site
        self.timenow = timenow


    def __repr__(self):
        return '<Next_Day %r>' % self.statdays


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_tag = db.Column(db.String(50))
    locations = db.Column(db.String(80))


    def __init__(self, id, user_tag , locations):
        self.id = id
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

    def __init__(self, id, city_or_country , Cmin , Cmax , Ccur , status , wind , time):
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

@app.route('/user/<id>/<user_tag>/<locations>' , methods = ['GET' , 'POST'])
def home(user_tag , locations , id):
    db.create_all()
    User1 = User(id = id,user_tag = user_tag , locations = locations)
    db.session.add(User1)
    db.session.commit()
    #return 'ok'
    return 'You have created User with tag that equials {} , and with location {}'.format(user_tag,locations)

def as_dict(object):
    res = []
    if isinstance(object,list):
        for ob in object:
            res.append({c.name: getattr(ob, c.name) for c in ob.__table__.columns})
    else:
        res.append({c.name: getattr(object, c.name) for c in object.__table__.columns})
    return res

if _name_ == '_main_':
    app.run(port = 4777)
    User1 = User(id = id,user_tag = 'ghhgh' , locations = 'hghgh')
    db.session.add(User1)
    db.session.commit()
