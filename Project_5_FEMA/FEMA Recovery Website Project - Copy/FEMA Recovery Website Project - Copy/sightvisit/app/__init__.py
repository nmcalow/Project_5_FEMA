from flask import Flask
from config import Config
from flask_googlemaps import GoogleMaps
from app.keys import keys
# Flask uses the location of the module passed here as
# a starting point when it needs to load associated resources such as
# template files
app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOADED_PHOTOS_DEST'] = 'app/img'
app.config['GOOGLEMAPS_KEY'] = keys.google
GoogleMaps(app)


from app import routes
