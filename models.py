from flask_sqlalchemy import SQLAlchemy
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String)
    facebook_link = db.Column(db.String)
    upcoming_shows = db.Column(db.Integer())
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String)
    website = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    shows = db.relationship('Show', backref='venues')


    # TODO: implement any missing fields, as a database migration using Flask-Migrate
"""
 data1={
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }


"""


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', backref='artists')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    venue = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    date = db.Column(db.TIMESTAMP(), nullable=False)


# class City(db.Model):
#     __tablename__ = 'City'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     state = db.Column(db.ForeignKey('State.id'))
#
# class State(db.Model):
#     __tablename__ = 'State'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     city = db.relationship('City', backref='states')
