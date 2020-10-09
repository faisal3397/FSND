#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
# to generate random integers when inserting an object to DB
import random 
# to trace the last error
import sys
# to split genres string by multiple delimeters
import re
# to compare dates
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
# migrate all the models in 'app' to the database 'db'
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
  venue_name = db.Column(db.String, db.ForeignKey('Venue.name'), unique=True, nullable=False)
  artist_name = db.Column(db.String, db.ForeignKey('Artist.name'), unique=True, nullable=False)
  venue_image_link = db.Column(db.String(500), db.ForeignKey('Venue.image_link'), unique=True)
  artist_image_link = db.Column(db.String(500), db.ForeignKey('Artist.image_link'), unique=True)
  start_time = db.Column(db.DateTime())

class Venue(db.Model):
  __tablename__ = 'Venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500), unique=True)
  facebook_link = db.Column(db.String(120))

  # TODO: implement any missing fields, as a database migration using Flask-Migrate
  genres = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean)
  seeking_description = db.Column(db.String(500))
  website = db.Column(db.String(120))
  past_shows = db.relationship('Show', backref='past_venues', primaryjoin="and_(Venue.id==Show.venue_id, Show.start_time < func.current_date())")
  past_shows_count = db.Column(db.Integer)
  upcoming_shows = db.relationship('Show', backref='upcoming_venues', primaryjoin="and_(Venue.id==Show.venue_id, Show.start_time >= func.current_date())")
  upcoming_shows_count = db.Column(db.Integer)

  def __repr__(self):
    return f'<Venue ID: {self.id}, \n Name: {self.name}, \n City: {self.city}, \n State: {self.state}, \n Address: {self.address}, \n Phone: {self.phone}, \n Genres: {self.genres} \n ----------------------------->'


class Artist(db.Model):
  __tablename__ = 'Artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String(120))
  image_link = db.Column(db.String(500), unique=True)
  facebook_link = db.Column(db.String(120))

  # TODO: implement any missing fields, as a database migration using Flask-Migrate
  website = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean)
  seeking_description = db.Column(db.String(500))
  past_shows = db.relationship('Show', backref='past_artists', primaryjoin="and_(Artist.id==Show.artist_id, Show.start_time < func.current_date())")
  past_shows_count = db.Column(db.Integer)
  upcoming_shows = db.relationship('Show', backref='upcoming_artists', primaryjoin="and_(Artist.id==Show.artist_id, Show.start_time >= func.current_date())")
  upcoming_shows_count = db.Column(db.Integer)

  def __repr__(self):
    return f'<Artist ID: {self.id}, \n Name: {self.name}, \n City: {self.city}, \n State: {self.state}, \n Phone: {self.phone}, \n Genres: {self.genres} \n ----------------------------->'

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  venues = Venue.query.all()
  data = []

  for venue in venues:
    city_found = False
    if len(data) > 0:
      for venues_city in data:
        if venues_city['city'] == venue.city:
          venues_city['venues'].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(venue.upcoming_shows)
          })
          city_found = True
          break
        else:
          # continue until we find the venue's city in data list
          continue
      # if the loop is done, and we didn't find the venue's city in data list, 
      # then we'll create and append the venue's city to the data list
      if not city_found:
        venues_city = {
          "city": venue.city,
          "state": venue.state,
          "venues": [{
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(venue.upcoming_shows)
          }]
        }
        data.append(venues_city)
    else:
      venues_city = {
        "city": venue.city,
        "state": venue.state,
        "venues": [{
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": len(venue.upcoming_shows)
        }]
      }
      data.append(venues_city)


  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')
  # add %% before and after search term to get all the results that has the search term in their names
  search = "%{}%".format(search_term)
  search_query = Venue.query.filter(Venue.name.ilike(search)).all()
  response={
    "count": len(search_query),
    "data": []
  }
  for venue in search_query:
    response['data'].append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": venue.upcoming_shows_count,
    })
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  venue.genres = re.split('{|}|,', venue.genres) # split genres to remove unwanted delimeters e.g."{","}",","
  data={
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
    "past_shows": venue.past_shows,
    "upcoming_shows": venue.upcoming_shows,
    "past_shows_count": len(venue.past_shows),
    "upcoming_shows_count": len(venue.upcoming_shows),
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
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try:
    id = random.randint(0, 9999)
    name = request.form.get("name")
    city = request.form.get("city")
    state = request.form.get("state")
    address = request.form.get("address")
    phone = request.form.get("phone")
    image_link = request.form.get("image_link")
    facebook_link = request.form.get("facebook_link")
    genres = request.form.getlist("genres")
    website = request.form.get("website")

    if request.form.get("seeking_talent") == 'y':
      seeking_talent = True
      seeking_description = request.form.get("seeking_description")
    else:
      seeking_talent = False
      seeking_description = ''
    
    venue = Venue(
      id=id, 
      name=name, 
      city=city, 
      state=state, 
      address=address, 
      phone=phone, 
      image_link=image_link, 
      facebook_link=facebook_link, 
      genres=genres, 
      website=website,
      seeking_talent=seeking_talent,
      seeking_description=seeking_description,
    )
    db.session.add(venue)
    db.session.commit()
  except():
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    flash('Venue ' + request.form['name'] + ' was not listed due to some error!')
  else:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')


  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except():
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    print('Venue ' + venue.name + ' was not deleted due to some error!')
  else:
    print('Venue ' + venue.name + ' was successfully deleted!')


  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data = []
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term', '')
  # add %% before and after search term to get all the results that has the search term in their names
  search = "%{}%".format(search_term)
  search_query = Artist.query.filter(Artist.name.ilike(search)).all()
  response={
    "count": len(search_query),
    "data": []
  }
  for artist in search_query:
    response['data'].append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": artist.upcoming_shows_count,
    })

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artists table, using artist_id
  artist = Artist.query.get(artist_id)
  artist.genres = re.split('{|}|,', artist.genres) # split genres to remove unwanted delimeters e.g."{","}",","
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": artist.past_shows,
    "upcoming_shows": artist.upcoming_shows,
    "past_shows_count": len(artist.past_shows),
    "upcoming_shows_count": len(artist.upcoming_shows),
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get(artist_id)

  # since these fields are different, e.g. TextAreaField, BooleanField,etc..., 
  # we need to handle it in a different way
  seeking_venue = ''
  if artist.seeking_venue:
    form.seeking_venue.data = 'y'
  form.seeking_description.data = artist.seeking_description
  form.genres.data = artist.genres

  data={
    "id": artist.id,
    "name": artist.name,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "image_link": artist.image_link,
  }
  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  try:
    artist = Artist.query.get(artist_id)
    artist.name = request.form.get("name")
    artist.city = request.form.get("city")
    artist.state = request.form.get("state")
    artist.phone = request.form.get("phone")
    artist.image_link = request.form.get("image_link")
    artist.facebook_link = request.form.get("facebook_link")
    artist.genres = request.form.getlist("genres")
    artist.website = request.form.get("website")

    if request.form.get("seeking_venue") == 'y':
      artist.seeking_venue = True
      artist.seeking_description = request.form.get("seeking_description")
    else:
      artist.seeking_venue = False
      artist.seeking_description = ''

    db.session.commit()
  except():
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    flash('Artist ' + request.form['name'] + ' was not updated due to some error!')
  else:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # TODO: populate form with values from venue with ID <venue_id>
  venue = Venue.query.get(venue_id)

  # since these fields are different, e.g. TextAreaField, BooleanField,etc..., 
  # we need to handle it in a different way
  seeking_talent = ''
  if venue.seeking_talent:
    form.seeking_talent.data = 'y'
  form.seeking_description.data = venue.seeking_description
  form.genres.data = venue.genres

  data={
    "id": venue.id,
    "name": venue.name,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "image_link": venue.image_link,
    "past_shows": venue.past_shows,
    "upcoming_shows": venue.upcoming_shows,
    "past_shows_count": len(venue.past_shows),
    "upcoming_shows_count": len(venue.upcoming_shows),
  }
  return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  try:
    venue = Venue.query.get(venue_id)
    venue.name = request.form.get("name")
    venue.city = request.form.get("city")
    venue.state = request.form.get("state")
    venue.address = request.form.get("address")
    venue.phone = request.form.get("phone")
    venue.image_link = request.form.get("image_link")
    venue.facebook_link = request.form.get("facebook_link")
    venue.genres = request.form.getlist("genres")
    venue.website = request.form.get("website")

    if request.form.get("seeking_talent") == 'y':
      venue.seeking_talent = True
      venue.seeking_description = request.form.get("seeking_description")
    else:
      venue.seeking_talent = False
      venue.seeking_description = ''
    db.session.commit()
  except():
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('Venue ' + request.form['name'] + ' was not updated due to some error!')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try:
    id = random.randint(0, 9999)
    name = request.form.get("name")
    city = request.form.get("city")
    state = request.form.get("state")
    phone = request.form.get("phone")
    image_link = request.form.get("image_link")
    facebook_link = request.form.get("facebook_link")
    genres = request.form.getlist("genres")
    website = request.form.get("website")

    if request.form.get("seeking_venue") == 'y':
      seeking_venue = True
      seeking_description = request.form.get("seeking_description")
    else:
      seeking_venue = False
      seeking_description = ''
    
    artist = Artist(
      id=id, 
      name=name, 
      city=city, 
      state=state, 
      phone=phone, 
      image_link=image_link, 
      facebook_link=facebook_link, 
      genres=genres, 
      website=website,
      seeking_venue=seeking_venue,
      seeking_description=seeking_description,
    )
    db.session.add(artist)
    db.session.commit()
  except():
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    flash('Artist ' + request.form['name'] + ' was not listed due to some error!')
  else:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  shows = Show.query.all()
  for show in shows:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue_name,
      "artist_id": show.artist_id,
      "artist_name": show.artist_name,
      "artist_image_link": show.artist_image_link,
      "start_time": show.start_time
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False

  try:
    id = random.randint(0, 9999)
    venue_id = request.form.get('venue_id')
    artist_id = request.form.get('artist_id')
    venue = Venue.query.get(venue_id)
    artist = Artist.query.get(artist_id)

    venue_name = venue.name
    artist_name = artist.name
    venue_image_link = venue.image_link
    artist_image_link = artist.image_link
    start_time = request.form.get('start_time')
    # convert start_time from string to timestamp
    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    show = Show(
      id=id,
      venue_id=venue_id,
      artist_id=artist_id,
      venue_name=venue_name,
      artist_name=artist_name,
      venue_image_link=venue_image_link,
      artist_image_link=artist_image_link,
      start_time = start_time
    )
    db.session.add(show)
    db.session.commit()
  except():
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  # TODO: on unsuccessful db insert, flash an error instead.
  if error:
    flash('An error occurred. Show could not be listed.')
  else:
    # on successful db insert, flash success
    flash('Show was successfully listed!')

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
