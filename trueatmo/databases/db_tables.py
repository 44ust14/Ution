from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/GOITeens/Giiit project/Ution/trueatmo/main_db.db'
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

    def __init__(self, id, city_or_country , Cmin , Cmax , Ccur , status , wind , site, time):
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
    locations = db.Column(db.String(80))
    waiting_for_location =db.Column(db.Integer)


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

if __name__ == '__main__':
    app.run(port = 4777)
    User1 = User(id = id,user_tag = 'ghhgh' , locations = 'hghgh')
    db.session.add(User1)
    db.session.commit()
