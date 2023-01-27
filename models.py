from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username



class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rfid = db.Column(db.String(20), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    # count = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    def __init__(self, rfid, lat, lng, timestamp):
        self.rfid = rfid
        self.lat = lat
        self.lng = lng
        self.timestamp = timestamp
        # self.count = count

    def __repr__(self):
        return f'<Vehicle {self.rfid}>'
