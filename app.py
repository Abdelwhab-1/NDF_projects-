#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db, Venue, Artist, Show
from flask_migrate import Migrate
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app=app,db=db)

# TODO: connect to a local postgresql database
#----------------------------------------------------------------------------#
# helping functions.
#----------------------------------------------------------------------------#
# from python without join
def upcoming(arg):
    shows = arg.shows
    current_date = datetime.now()
    shows = [show for show  in shows if show.date > current_date]
    return shows

def get_past_shows(arg):
    shows = arg.shows
    current_date = datetime.now()
    shows = [show for show  in shows if show.date < current_date]
    return shows
def future_past_shows_wraper(func, venue):
    return func(venue)
#--------------------------------------------------------#
def past(venue):
    # past_show = get_past_shows(venue)
    past_show = db.session.query(Artist,Show).join(Show).filter(Show.venue == venue.id).filter(Show.date < datetime.now()).all()
    past_shows = list()
    for set in past_show:
        dic = {
            "artist_id": set[0].id,
            "artist_name": set[0].name,
            "artist_image_link": set[0].image_link,
            "start_time": str(set[1].date)

        }
        past_shows.append(dic)
    return past_shows


def future(venue):
    #upcoming_show = upcoming(venue)
    upcoming_show = db.session.query(Artist,Show).join(Show).filter(Show.venue == venue.id).filter(Show.date > datetime.now()).all()
    upcoming_shows = list()
    for set in upcoming_show:
        dic = {
            "artist_id": set[0].id,
            "artist_name": set[0].name,
            "artist_image_link": set[0].image_link,
            "start_time": str(set[1].date)

        }
        upcoming_shows.append(dic)
    return upcoming_shows


def artist_past(artist):
    #past_show = get_past_shows(artist)
    past_show = db.session.query(Venue,Show).join(Show).filter(Show.artist == artist.id).filter(Show.date < datetime.now()).all()
    past_shows = list()
    for set in past_show:
        dic = {
        "venue_id": set[0].id,
        "venue_name": set[0].name,
        "venue_image_link": set[0].image_link,
        "start_time": str(set[1].date)
        }
        past_shows.append(dic)
    return past_shows

def artist_future(artist):
    # upcomings = upcoming(artist)
    upcomings = db.session.query(Venue,Show).join(Show).filter(Show.artist == artist.id).filter(Show.date > datetime.now()).all()
    upcoming_shows = list()
    for set in upcomings:
        dic = {
        "venue_id": set[0].id,
        "venue_name": set[0].name,
        "venue_image_link": set[0].image_link,
        "start_time": str(set[1].date)
        }
        upcoming_shows.append(dic)
    return upcoming_shows
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

    all_venues = Venue.query.order_by(Venue.state).all()
    data = list()
    current = None
    current_city = None
    for venu in all_venues:
        if venu.state == current:
            if current_city == venu.city:
                venue_detail = {
                  "id": venu.id,
                  "name": venu.name,
                  "num_upcoming_shows": len(upcoming(venu))
                }
                result['venues'].append(venue_detail)
            else:
                data.append(result)
                current_city = venu.city
                result = {
                  "city": venu.city,
                  "state": venu.state,
                  "venues": []
                }
                venue_detail ={
                  "id": venu.id,
                  "name": venu.name,
                  "num_upcoming_shows": len(upcoming(venu))
                }
                result["venues"].append(venue_detail)
        else:
            if current:
                data.append(result)
            current = venu.state
            current_city = venu.city
            result = {
              "state": venu.state,
              "city" : venu.city,
              "venues": []
            }
            venue_detail = {
              "id": venu.id,
              "name": venu.name,
              "num_upcoming_shows": len(upcoming(venu))
            }
            result['venues'].append(venue_detail )
    data.append(result)
    return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
      # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
      # seach for Hop should return "The Musical Hop".
      # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
      term = f"%{request.form.get('search_term')}%"
      result = Venue.query.filter(Venue.name.ilike(term)).all()
      data = list()
      count = 0
      for venue in result:
          artist_dict = {
              "id": venue.id,
              "name": venue.name,
              "num_upcoming_shows": len(future(venue))
          }
          data.append(artist_dict)
          count += 1
      response = {
          "count": count,
          "data": data
      }
      return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue = Venue.query.get_or_404(venue_id)
    past_shows = past(venue)
    upcoming_shows = future(venue)
    data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows":past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    venue = Venue()

    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state = request.form.get("state")
    venue.address = request.form.get('state')
    venue.phone = request.form.get('phone')
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form.get("facebook_link")
    venue.website_link = request.form.get('website_link')
    venue.image_link = request.form.get('image_link')
    venue.seeking_talent = bool(request.form.get('is_seeking'))
    venue.seeking_description = request.form.get('seeking_description')

    try:
        db.session.add(venue)
        db.session.commit()
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
        return render_template('errors/500.html'), 500

    # on successful db insert, flash success
    flash('Venue ' + venue.name + ' was successfully listed!')
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    venue = Venue.query.get_or_404(venue_id)
    venue_name = venue.name
    venue_id = venue.id
    try:
        db.session.delete(venue)
        db.session.commit()
        flash('Venue' + venue_name+ ' that has id ' + str(venue_id) + 'was successfully deleted!')
    except:
        db.session.rollback()
        flash('Venue' + venue_name + ' that has id ' +  str(venue_id) + 'wasn\'t  successfully deleted!')
        return render_template('errors/500.html'), 500


    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    artists = Artist.query.limit(4).all()
    data = list()
    for artist in artists:
        dic = {
            'id': artist.id,
            'name': artist.name
        }
        data.append(dic)
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    term = f"%{request.form.get('search_term')}%".lower()
    result = Artist.query.filter(Artist.name.like(term)).all()
    data = list()
    count = 0
    for artist in result:
      artist_dict = {
          "id": artist.id,
          "name": artist.name,
          "num_upcoming_shows": len(artist_future(artist))
      }
      data.append(artist_dict)
      count += 1
    response={
    "count": count,
    "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    artist = Artist.query.get_or_404(artist_id)
    past_shows = artist_past(artist)
    upcoming_shows = artist_future(artist)
    data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artst = Artist.query.get_or_404(artist_id)
    artist={
    "id": artst.id,
    "name": artst.name,
    "genres": artst.genres,
    "city": artst.city,
    "state": artst.state,
    "phone": artst.phone,
    "website": artst.website_link,
    "facebook_link": artst.facebook_link ,
    "seeking_venue":  artst.seeking_venue ,
    "seeking_description": artst.seeking_description,
    "image_link": artst.image_link
    }
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.genres = request.form.getlist('genres')
    artist.phone = request.form.get('phone')
    artist.website_link = request.form.get('website_link')
    artist.image_link = request.form.get('image_link')
    artist.seeking_venue = bool(request.form.get('is_seeking'))
    artist.seeking_description = request.form.get('seeking_description')
    artist.facebook_link = request.form.get("facebook_link")

    try:
      db.session.commit()
      flash('Artist ' + artist.name + ' was successfully updated!')
    except :
        db.session.rollback()
        flash('Artist ' + artist.name + ' was not updated!')
        return render_template('errors/500.html'), 500
    # artist record with ID <artist_id> using the new attributes
    return redirect(url_for('show_artist', artist_id=artist.id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get_or_404(venue_id)
  venue={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get_or_404(venue_id)

    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state = request.form.get("state")
    venue.address = request.form.get('state')
    venue.phone = request.form.get('phone')
    venue.genres = request.form.getlist('genres')
    venue.website_link = request.form.get('website_link')
    venue.image_link = request.form.get('image_link')
    venue.seeking_talent =bool(request.form.get('is_seeking'))
    venue.seeking_description = request.form.get('seeking_description')
    venue.facebook_link = request.form.get("facebook_link")
    venue_id = venue.id
    try:
        db.session.commit()
        flash('Venue ' + venue.name + ' was successfully updated!')
    except Exception as e :
        print(e)
        db.session.rollback()
        flash('Venue ' + venue.name + ' wasn\'t updated!')
        return render_template('errors/500.html'), 500
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    artist = Artist()

    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.genres = request.form.getlist('genres')
    artist.phone = request.form.get('phone')
    artist.website_link = request.form.get('website_link')
    artist.image_link = request.form.get('image_link')
    artist.seeking_talent = bool(request.form.get('is_seeking'))
    artist.seeking_description = request.form.get('seeking_description')
    artist.facebook_link = request.form.get("facebook_link")
    try:
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + artist.name + ' was successfully listed!')
    except Exception as e :
        print(e)
        db.session.rollback()
        flash('An error occurred. Artist ' + request.form.get("name") + ' could not be listed.')
        return render_template('errors/500.html'), 500
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    shows_list = Show.query.limit(6).all()
    data = list()
    for show in shows_list:
        details = {
            "venue_id": show.venue,
            "venue_name": show.venues.name,
            "artist_id": show.artist,
            "artist_name": show.artists.name,
            "artist_image_link": show.artists.image_link,
            "start_time": str(show.date)
        }
        data.append(details)
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    show = Show()
    try:
        artist = Artist.query.get_or_404(request.form.get('artist_id'))
        venue = Venue.query.get_or_404(request.form.get('venue_id'))
    except:
        flash('eiher artsit or venue id isn\'t corrent')
        return render_template('errors/500.html'), 500

    show.venue = venue.id
    show.artist = artist.id
    show.date = request.form.get('start_time')
    flash('Show was successfully listed!')
    try:
        db.session.add(show)
        db.session.commit()
    except:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
        return render_template('errors/500.html'), 500
    # on successful db insert, flash success

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
