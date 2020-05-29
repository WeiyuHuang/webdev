
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://weiyuhuang@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime)
    artist = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

def main():
    data = []
    venues = Venue.query.all()
    locations = set()

    for venue in venues:
        locations.add((venue.city, venue.state))

    for location in locations:
        data.append({"city": location[0],
                     "state": location[1],
                     "venues": []})

    for venue in venues:
        shows = Show.query.filter_by(venue=venue.id).all()
        num_upcoming_shows = len(shows)

        for venue_location in data:
            if venue.city == venue_location['city'] and venue.state == venue_location['state']:
                venue_location['venues'].append({
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": num_upcoming_shows
                })

    print('Finished')

if __name__ == '__main__':
    main()