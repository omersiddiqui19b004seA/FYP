from flask import Flask, request, render_template, redirect ,url_for
from flask_sqlalchemy import SQLAlchemy
from models import db
from flask_migrate import Migrate
from datetime import datetime
from pytz import timezone
rfid_gps_data=[]


timestamp_str = datetime.now()
# date_time=timestamp_str.strftime("%Y-%m-%d %H:%M:%S")
utc_time = timezone('UTC').localize(timestamp_str)
app = Flask(__name__)
app.static_folder = 'static'
app.static_url_path = '/static'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle_tracking.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rfid = db.Column(db.String(20), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    # count = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         rfid = request.form['rfid']
#         lat = request.form['lat']
#         lng = request.form['lng']
#         # timestamp = date_time
#         vehicle = Vehicle(rfid=rfid, lat=lat, lng=lng, timestamp=utc_time)
#         db.session.add(vehicle)
#         db.session.commit()
#         return 'Vehicle location and rfid added to the database.'
#     return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        rfid = request.form['rfid']
        vehicle = Vehicle.query.filter_by(rfid=rfid).first()
        if vehicle:
            return f'RFID: {vehicle.rfid}<br>Latitude: {vehicle.lat}<br>Longitude: {vehicle.lng}<br>Timestamp: {vehicle.timestamp}'
        else:
            return 'No vehicle found with that RFID.'
    return render_template('search.html')


@app.route('/scan_rfid', methods=['GET','POST'])
def scan_rfid():
    if request.method == 'POST':
        rfid = request.form['rfid']
        lat = request.form['lat']
        lng = request.form['lng']
        vehicle = Vehicle.query.filter_by(rfid=rfid).first()
        if vehicle:
            vehicle.lat = lat
            vehicle.lng = lng
            # vehicle.count += 1
            db.session.commit()
        else:
            new_vehicle = Vehicle(rfid=rfid, lat=lat, lng=lng, timestamp=utc_time)
            db.session.add(new_vehicle)
            db.session.commit()
        return 'Inserted'
    elif request.method == 'GET':
        return render_template(('index.html'))


@app.route('/view_rfid')
def view_rfid():
    rfids = db.session.query(Vehicle).all()
    rfids=Vehicle.query.with_entities(Vehicle.rfid, Vehicle.lat , Vehicle.lng, Vehicle.timestamp).all()

    db.session.commit()
    return render_template('view_rfid.html',rfids=rfids)

@app.route('/data/', methods=['POST'])
def receive_data():
    rfid = request.form['uid']
    lat = request.form['lat']
    lng = request.form['lng']
    vehicle = Vehicle.query.filter_by(rfid=rfid).first()
    # print(rfid)
    if vehicle:
        vehicle.lat = lat
        vehicle.lng = lng
        # vehicle.count += 1
        db.session.commit()
    else:
        new_vehicle = Vehicle(rfid=rfid, lat=lat, lng=lng, timestamp=utc_time)
        db.session.add(new_vehicle)
        db.session.commit()
    return 'Inserted'


if __name__ == '__main__':
    # db.create_all()
    # app.run(debug=True)
    app.run(debug=True, host='192.168.43.206',port=5000)
