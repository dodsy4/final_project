#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
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
from sqlalchemy import func
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)


migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class m(db.Model):
    __tablename__ = 'm'

    id = db.Column(db.Integer, primary_key=True)
    waste_stream = db.Column(db.String)
    amount = db.Column(db.Integer)
    city = db.Column(db.String(120))
    county = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    project = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
        return '<Material {}>'.format(self.name)

class c(db.Model):
    __tablename__ = 'c'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    county = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    linkedin_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    interests = db.Column(db.String(120))

    def __repr__(self):
        return '<Charity {}>'.format(self.name)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    mat_id = db.Column(db.Integer, db.ForeignKey('m.id'), nullable=False)
    a_id = db.Column(db.Integer, db.ForeignKey('a.id'), nullable=False)
    message = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Request {}{}>'.format(self.artist_id, self.venue_id)

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
@app.route('/login')
def login():
    return render_template('pages/login.html')

@app.route('/')
def index():
    return render_template('pages/home.html')

#----------------------------------------------------------------------------#
#  Materials
#----------------------------------------------------------------------------#
@app.route('/materials')
def materials():
  # TODO: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
    
    all_areas = m.query.with_entities(func.count(m.id), m.city, m.county).group_by(m.city, m.county).all()
    data = []

    for area in all_areas:
        area_materials = m.query.filter_by(county=area.county).filter_by(city=area.city).all()
    
        material_data = []
    
        for material in area_materials:
            material_data.append({
                "id": m.id,
                "name": m.name
                })
    
    
        data.append({
            "city": area.city,
            "state": area.county, 
            "venues": material_data
            })

    
    return render_template('pages/venues.html', areas=data)

@app.route('/materials/search', methods=['POST'])
def search_materials():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    search_result = db.session.query(m).filter(m.name.ilike(f'%{search_term}%')).all()
    data = []

    for result in search_result:
        data.append({
            "id": result.id,
            "name": result.name
        })
  
    response={
        "count": len(search_result),
        "data": data
    }
  
    return render_template('pages/search_materials.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/materials/<int:material_id>')
def show_material(material_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  
    material = m.query.get(material_id)

    if not material: 
        return render_template('errors/404.html')

    data = {
        "id": material.id,
        "material": material.waste_stream,
        "city": material.city,
        "state": material.county,
        "address": material.address,
        "phone": material.phone
    }

    return render_template('pages/show_material.html', material=data)


#  ----------------------------------------------------------------
#  Accounts Details
#  ----------------------------------------------------------------
@app.route('/account_details/<int:account_id>')
def show_account(account_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  
    charity = c.query.get(account_id)

    if not name: 
        return render_template('errors/404.html')

    data = {
        "id": charity.id,
        "material": charity.waste_stream,
        "city": charity.city,
        "state": charity.county,
        "address": charity.address,
        "phone": charity.phone
    }

    return render_template('pages/show_account.html', material=data)


# see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.route('/account_details/<int:account_id>/edit', methods=['GET'])
def edit_account(account_id):
    form = CharityForm()
    charity = c.query.get(account_id)
    
    if charity:
        form.name.data = c.name
        form.city.data = c.name

  # TODO: populate form with fields for charity edit

    return render_template('forms/edit_charity.html', form=form, artist=artist)

@app.route('/account_details/<int:account_id>/edit', methods=['POST'])
def edit_account_submission(account_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    error = False
    charity = c.query.get(account_id)
   
    try:
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['county']
        artist.address = request.form['address']
        artist.phone = request.form['phone']
        artist.genres = request.form['genres']
        artist.image_link = request.form['image_link']
        artist.facebook_link = request.form['facebook_link']
        artist.website = request.form['website']
        artist.seeking_description = request.form['seeking_description']
        artist.seeking_venue = request.form['seeking_venue']
        
        db.session.commit()
    
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    
    finally:
        db.session.close()
    
    if error:
        flash('An error occurred. Account details could not be changed.')

    if not error:
        flash('Account details were successfully successfully changed.')
    

    return redirect(url_for('show_account', account_id=account_id))


#  Create Account
#  ----------------------------------------------------------------

@app.route('/account/create', methods=['GET'])
def create_account_form():
    form = CharityForm()
    return render_template('forms/new_charity.html', form=form)

@app.route('/account/create', methods=['POST'])
def create_account_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    error=False
    try:
        name = request.form['name']
        city = request.form['city']
        county = request.form['county']
        address = request.form['address']
        phone = request.form['phone']
        facebook_link = request.form['facebook_link']
        website = request.form['website']

        charity = c(name=name, city=city, county=county, address=address, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website=website, seeking_description=seeking_description, seeking_venue=seeking_venue)
        db.session.add(charity)
        db.session.commit()
    
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
    
    if error:
        flash('Error. Account was not uploaded.')

    if not error:
        flash('Account was successfully uploaded.')
        
    return render_template('pages/home.html')
  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


#  Create Request
#  ----------------------------------------------------------------
@app.route('/materials/request', methods=['GET'])
def request_material_form():
    form = RequestMaterialForm()
    return render_template('forms/new_request.html', form=form)

@app.route('/materials/request', methods=['POST'])
def create_request_submission():
    error=False
    try:
        name = request.form['name']
        
        
        
        request = r(name=name, city=city, county=county, address=address, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website=website, seeking_description=seeking_description, seeking_venue=seeking_venue)
        db.session.add(request)
        db.session.commit()
    
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
    
    if error:
        flash('Error. Request was not sent.')

    if not error:
        flash('Request sent!')
        
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
