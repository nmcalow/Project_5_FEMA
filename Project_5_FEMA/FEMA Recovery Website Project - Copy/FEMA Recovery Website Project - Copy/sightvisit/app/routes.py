from flask import render_template, flash, redirect, request, send_from_directory
from app import app
from app.forms import ContactForm, Addresses, LoginForm
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import pandas as pd
# API keys
from app.keys import keys
# Package imports for dealing with images
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# Package imports for Zillow
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults

# Package imports for Google Maps APIs
import google_streetview.api

# Geocoding and reverse Geocoding
from pygeocoder import Geocoder

# User defined functions
from app.functions import get_gps_details, convert_to_degress, get_img_coord_str, get_img_coord_tuple, pull_streetview, reverse_lookup, zillow_query, address_splitter, get_streetview_link, build_matrix, get_times, create_data_model, compute_euclidean_distance_matrix, set_address_path, print_solution, traveling_salesman

# route to home page
@app.route('/')
@app.route('/index')
def mapview():
    addresslist = Addresses()
    form = ContactForm()

    # extracting info from 10 addresses
    address_split = address_splitter(address = addresslist.address1)
    address_main = address_split[0]
    address_zip = address_split[1]
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    latitude1 = zillowresult.latitude
    longitude1 = zillowresult.longitude

    address_split = address_splitter(address = addresslist.address2)
    address_main = address_split[0]
    address_zip = address_split[1]
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    latitude2 = zillowresult.latitude
    longitude2 = zillowresult.longitude

    address_split = address_splitter(address = addresslist.address3)
    address_main = address_split[0]
    address_zip = address_split[1]
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    latitude3 = zillowresult.latitude
    longitude3 = zillowresult.longitude

    address_split = address_splitter(address = addresslist.address4)
    address_main = address_split[0]
    address_zip = address_split[1]
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    latitude4 = zillowresult.latitude
    longitude4 = zillowresult.longitude

    address_split = address_splitter(address = addresslist.address5)
    address_main = address_split[0]
    address_zip = address_split[1]
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    latitude5 = zillowresult.latitude
    longitude5 = zillowresult.longitude

    address_split = address_splitter(address = addresslist.address6)
    address_main = address_split[0]
    address_zip = address_split[1]
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    latitude6 = zillowresult.latitude
    longitude6 = zillowresult.longitude

    address_split = address_splitter(address = addresslist.address7)
    address_main = address_split[0]
    address_zip = address_split[1]
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    latitude7 = zillowresult.latitude
    longitude7 = zillowresult.longitude

    address_split = address_splitter(address = addresslist.address8)
    address_main = address_split[0]
    address_zip = address_split[1]
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    latitude8 = zillowresult.latitude
    longitude8 = zillowresult.longitude

    address_split = address_splitter(address = addresslist.address9)
    address_main = address_split[0]
    address_zip = address_split[1]
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    latitude9 = zillowresult.latitude
    longitude9 = zillowresult.longitude

    address_split = address_splitter(address = addresslist.address10)
    address_main = address_split[0]
    address_zip = address_split[1]
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    latitude10 = zillowresult.latitude
    longitude10 = zillowresult.longitude

    # creating a map in the view
    allmarkermap = Map(
        identifier="view-side",
        lat=latitude1,
        lng=longitude1,
        zoom= 17,
        markers=[(latitude1, longitude1), (latitude2, longitude2), (latitude3, longitude3), (latitude4, longitude4), (latitude5, longitude5), (latitude6, longitude6), (latitude7, longitude7), (latitude8, longitude8), (latitude9, longitude9), (latitude10, longitude10)],
        style="height:550px;width:100%;margin:0;",
        margin=0,
        )

    return render_template('index.html', allmarkermap=allmarkermap, latitude1=latitude1, longitude1=longitude1, latitude2=latitude2, longitude2=longitude2, latitude3=latitude3, longitude3=longitude3, latitude4=latitude4, longitude4=longitude4, latitude5=latitude5, longitude5=longitude5, latitude6=latitude6, longitude6=longitude6, latitude7=latitude7, longitude7=longitude7, latitude8=latitude8, longitude8=longitude8, latitude9=longitude9, latitude10=latitude10, longitude10=longitude10)


if __name__ == "__main__":
    app.run(debug=True)


@app.route('/', methods = ['POST'])
@app.route('/index', methods = ['POST'])
def taking_addresses():

    text1 = request.form['text1']
    address1 = text1.title()

    text2 = request.form['text2']
    address2 = text2.title()

    text3 = request.form['text3']
    address3 = text3.title()

    text4 = request.form['text4']
    address4 = text4.title()

    text5 = request.form['text5']
    address5 = text5.title()

    text6 = request.form['text6']
    address6 = text6.title()

    text7 = request.form['text7']
    address7 = text7.title()

    text8 = request.form['text8']
    address8 = text8.title()

    text9 = request.form['text9']
    address9 = text9.title()

    text10 = request.form['text10']
    address10 = text10.title()



    return address1, address2, address3, address4, address5, address6, address7, address8, address9, address10

@app.route('/form1', methods = ['GET', 'POST'])
def form1():

    form = ContactForm()
    addresslist = Addresses()

    #image from the Google Street View Location
    image_link = get_streetview_link(addresslist.address1)[0]

    # extracting info from address
    address_split = address_splitter(address = addresslist.address1)
    address_main = address_split[0]
    address_zip = address_split[1]
    address_city = address_split[2]
    address_state = address_split[3]
    address_country = address_split[4]

    # zillow request
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    house_type = zillowresult.home_type
    house_size = zillowresult.home_size
    year = zillowresult.year_built
    num_beds = zillowresult.bedrooms
    num_baths = zillowresult.bathrooms.strip('.0')
    est_value = zillowresult.zestimate_amount
    est_date = zillowresult.zestimate_last_updated
    latitude = zillowresult.latitude
    longitude = zillowresult.longitude
    val_desc = "Zestimate"
    if est_value == None:
        est_value = zillowresult.tax_value
        est_date = zillowresult.tax_year
        val_desc = "Tax Assessment"

    onemarkermap = Map(
        identifier="view-side",
        lat=latitude,
        lng=longitude,
        zoom = 19,
        markers=[(latitude, longitude)],
        style="float:right; height:550px;width:640px;margin:0;",
        margin=0,
        )

    return render_template('fullform.html', form=form, onemarkermap=onemarkermap, address_main=address_main, address_zip=address_zip, address_city=address_city, address_state=address_state, address_country=address_country, bldg_type=house_type, bldg_size=house_size, built_year=year, beds=num_beds, baths=num_baths, value=est_value, val_date=est_date, latitude=latitude, longitude=longitude, val_desc=val_desc, image_link = image_link)




@app.route('/form2', methods = ['GET', 'POST'])
def form2():

    form = ContactForm()
    addresslist = Addresses()

    #image from the Google Street View Location
    image_link = get_streetview_link(addresslist.address2)[0]

    # extracting info from address
    address_split = address_splitter(address = addresslist.address2)
    address_main = address_split[0]
    address_zip = address_split[1]
    address_city = address_split[2]
    address_state = address_split[3]
    address_country = address_split[4]

    # zillow request
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    house_type = zillowresult.home_type
    house_size = zillowresult.home_size
    year = zillowresult.year_built
    num_beds = zillowresult.bedrooms
    num_baths = zillowresult.bathrooms.strip('.0')
    est_value = zillowresult.zestimate_amount
    est_date = zillowresult.zestimate_last_updated
    latitude = zillowresult.latitude
    longitude = zillowresult.longitude
    val_desc = "Zestimate"
    if est_value == None:
        est_value = zillowresult.tax_value
        est_date = zillowresult.tax_year
        val_desc = "Tax Assessment"

    onemarkermap = Map(
        identifier="view-side",
        lat=latitude,
        lng=longitude,
        zoom = 19,
        markers=[(latitude, longitude)],
        style="float:right; height:550px;width:640px;margin:0;",
        margin=0,
        )

    return render_template('fullform.html', form=form, onemarkermap=onemarkermap, address_main=address_main, address_zip=address_zip, address_city=address_city, address_state=address_state, address_country=address_country, bldg_type=house_type, bldg_size=house_size, built_year=year, beds=num_beds, baths=num_baths, value=est_value, val_date=est_date, latitude=latitude, longitude=longitude, val_desc=val_desc, image_link = image_link)


@app.route('/form3', methods = ['GET', 'POST'])
def form3():

    form = ContactForm()
    addresslist = Addresses()


    #image from the Google Street View Location
    image_link = get_streetview_link(addresslist.address3)[0]

    # extracting info from address
    address_split = address_splitter(address = addresslist.address3)
    address_main = address_split[0]
    address_zip = address_split[1]
    address_city = address_split[2]
    address_state = address_split[3]
    address_country = address_split[4]

    # zillow request
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    house_type = zillowresult.home_type
    house_size = zillowresult.home_size
    year = zillowresult.year_built
    num_beds = zillowresult.bedrooms
    num_baths = zillowresult.bathrooms.strip('.0')
    est_value = zillowresult.zestimate_amount
    est_date = zillowresult.zestimate_last_updated
    latitude = zillowresult.latitude
    longitude = zillowresult.longitude
    val_desc = "Zestimate"
    if est_value == None:
        est_value = zillowresult.tax_value
        est_date = zillowresult.tax_year
        val_desc = "Tax Assessment"

    onemarkermap = Map(
        identifier="view-side",
        lat=latitude,
        lng=longitude,
        zoom = 19,
        markers=[(latitude, longitude)],
        style="float:right; height:550px;width:640px;margin:0;",
        margin=0,
        )

    return render_template('fullform.html', form=form, onemarkermap=onemarkermap, address_main=address_main, address_zip=address_zip, address_city=address_city, address_state=address_state, address_country=address_country, bldg_type=house_type, bldg_size=house_size, built_year=year, beds=num_beds, baths=num_baths, value=est_value, val_date=est_date, latitude=latitude, longitude=longitude, val_desc=val_desc, image_link = image_link)


@app.route('/form4', methods = ['GET', 'POST'])
def form4():

    form = ContactForm()
    addresslist = Addresses()


    #image from the Google Street View Location
    image_link = get_streetview_link(addresslist.address4)[0]

    # extracting info from address
    address_split = address_splitter(address = addresslist.address4)
    address_main = address_split[0]
    address_zip = address_split[1]
    address_city = address_split[2]
    address_state = address_split[3]
    address_country = address_split[4]

    # zillow request
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    house_type = zillowresult.home_type
    house_size = zillowresult.home_size
    year = zillowresult.year_built
    num_beds = zillowresult.bedrooms
    num_baths = zillowresult.bathrooms.strip('.0')
    est_value = zillowresult.zestimate_amount
    est_date = zillowresult.zestimate_last_updated
    latitude = zillowresult.latitude
    longitude = zillowresult.longitude
    val_desc = "Zestimate"
    if est_value == None:
        est_value = zillowresult.tax_value
        est_date = zillowresult.tax_year
        val_desc = "Tax Assessment"

    onemarkermap = Map(
        identifier="view-side",
        lat=latitude,
        lng=longitude,
        zoom = 19,
        markers=[(latitude, longitude)],
        style="float:right; height:550px;width:640px;margin:0;",
        margin=0,
        )

    return render_template('fullform.html', form=form, onemarkermap=onemarkermap, address_main=address_main, address_zip=address_zip, address_city=address_city, address_state=address_state, address_country=address_country, bldg_type=house_type, bldg_size=house_size, built_year=year, beds=num_beds, baths=num_baths, value=est_value, val_date=est_date, latitude=latitude, longitude=longitude, val_desc=val_desc, image_link = image_link)


@app.route('/form5', methods = ['GET', 'POST'])
def form5():

    form = ContactForm()
    addresslist = Addresses()


    #image from the Google Street View Location
    image_link = get_streetview_link(addresslist.address5)[0]

    # extracting info from address
    address_split = address_splitter(address = addresslist.address5)
    address_main = address_split[0]
    address_zip = address_split[1]
    address_city = address_split[2]
    address_state = address_split[3]
    address_country = address_split[4]

    # zillow request
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    house_type = zillowresult.home_type
    house_size = zillowresult.home_size
    year = zillowresult.year_built
    num_beds = zillowresult.bedrooms
    num_baths = zillowresult.bathrooms.strip('.0')
    est_value = zillowresult.zestimate_amount
    est_date = zillowresult.zestimate_last_updated
    latitude = zillowresult.latitude
    longitude = zillowresult.longitude
    val_desc = "Zestimate"
    if est_value == None:
        est_value = zillowresult.tax_value
        est_date = zillowresult.tax_year
        val_desc = "Tax Assessment"

    onemarkermap = Map(
        identifier="view-side",
        lat=latitude,
        lng=longitude,
        zoom = 19,
        markers=[(latitude, longitude)],
        style="float:right; height:550px;width:640px;margin:0;",
        margin=0,
        )

    return render_template('fullform.html', form=form, onemarkermap=onemarkermap, address_main=address_main, address_zip=address_zip, address_city=address_city, address_state=address_state, address_country=address_country, bldg_type=house_type, bldg_size=house_size, built_year=year, beds=num_beds, baths=num_baths, value=est_value, val_date=est_date, latitude=latitude, longitude=longitude, val_desc=val_desc, image_link = image_link)


@app.route('/form6', methods = ['GET', 'POST'])
def form6():

    form = ContactForm()
    addresslist = Addresses()


    #image from the Google Street View Location
    image_link = get_streetview_link(addresslist.address6)[0]

    # extracting info from address
    address_split = address_splitter(address = addresslist.address6)
    address_main = address_split[0]
    address_zip = address_split[1]
    address_city = address_split[2]
    address_state = address_split[3]
    address_country = address_split[4]

    # zillow request
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    house_type = zillowresult.home_type
    house_size = zillowresult.home_size
    year = zillowresult.year_built
    num_beds = zillowresult.bedrooms
    num_baths = zillowresult.bathrooms.strip('.0')
    est_value = zillowresult.zestimate_amount
    est_date = zillowresult.zestimate_last_updated
    latitude = zillowresult.latitude
    longitude = zillowresult.longitude
    val_desc = "Zestimate"
    if est_value == None:
        est_value = zillowresult.tax_value
        est_date = zillowresult.tax_year
        val_desc = "Tax Assessment"

    onemarkermap = Map(
        identifier="view-side",
        lat=latitude,
        lng=longitude,
        zoom = 19,
        markers=[(latitude, longitude)],
        style="float:right; height:550px;width:640px;margin:0;",
        margin=0,
        )

    return render_template('fullform.html', form=form, onemarkermap=onemarkermap, address_main=address_main, address_zip=address_zip, address_city=address_city, address_state=address_state, address_country=address_country, bldg_type=house_type, bldg_size=house_size, built_year=year, beds=num_beds, baths=num_baths, value=est_value, val_date=est_date, latitude=latitude, longitude=longitude, val_desc=val_desc, image_link = image_link)


@app.route('/form7', methods = ['GET', 'POST'])
def form7():

    form = ContactForm()
    addresslist = Addresses()


    #image from the Google Street View Location
    image_link = get_streetview_link(addresslist.address7)[0]

    # extracting info from address
    address_split = address_splitter(address = addresslist.address7)
    address_main = address_split[0]
    address_zip = address_split[1]
    address_city = address_split[2]
    address_state = address_split[3]
    address_country = address_split[4]

    # zillow request
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    house_type = zillowresult.home_type
    house_size = zillowresult.home_size
    year = zillowresult.year_built
    num_beds = zillowresult.bedrooms
    num_baths = zillowresult.bathrooms.strip('.0')
    est_value = zillowresult.zestimate_amount
    est_date = zillowresult.zestimate_last_updated
    latitude = zillowresult.latitude
    longitude = zillowresult.longitude
    val_desc = "Zestimate"
    if est_value == None:
        est_value = zillowresult.tax_value
        est_date = zillowresult.tax_year
        val_desc = "Tax Assessment"

    onemarkermap = Map(
        identifier="view-side",
        lat=latitude,
        lng=longitude,
        zoom = 19,
        markers=[(latitude, longitude)],
        style="float:right; height:550px;width:640px;margin:0;",
        margin=0,
        )

    return render_template('fullform.html', form=form, onemarkermap=onemarkermap, address_main=address_main, address_zip=address_zip, address_city=address_city, address_state=address_state, address_country=address_country, bldg_type=house_type, bldg_size=house_size, built_year=year, beds=num_beds, baths=num_baths, value=est_value, val_date=est_date, latitude=latitude, longitude=longitude, val_desc=val_desc, image_link = image_link)


@app.route('/form8', methods = ['GET', 'POST'])
def form8():

    form = ContactForm()
    addresslist = Addresses()


    #image from the Google Street View Location
    image_link = get_streetview_link(addresslist.address8)[0]

    # extracting info from address
    address_split = address_splitter(address = addresslist.address8)
    address_main = address_split[0]
    address_zip = address_split[1]
    address_city = address_split[2]
    address_state = address_split[3]
    address_country = address_split[4]

    # zillow request
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    house_type = zillowresult.home_type
    house_size = zillowresult.home_size
    year = zillowresult.year_built
    num_beds = zillowresult.bedrooms
    num_baths = zillowresult.bathrooms.strip('.0')
    est_value = zillowresult.zestimate_amount
    est_date = zillowresult.zestimate_last_updated
    latitude = zillowresult.latitude
    longitude = zillowresult.longitude
    val_desc = "Zestimate"
    if est_value == None:
        est_value = zillowresult.tax_value
        est_date = zillowresult.tax_year
        val_desc = "Tax Assessment"

    onemarkermap = Map(
        identifier="view-side",
        lat=latitude,
        lng=longitude,
        zoom = 19,
        markers=[(latitude, longitude)],
        style="float:right; height:550px;width:640px;margin:0;",
        margin=0,
        )

    return render_template('fullform.html', form=form, onemarkermap=onemarkermap, address_main=address_main, address_zip=address_zip, address_city=address_city, address_state=address_state, address_country=address_country, bldg_type=house_type, bldg_size=house_size, built_year=year, beds=num_beds, baths=num_baths, value=est_value, val_date=est_date, latitude=latitude, longitude=longitude, val_desc=val_desc, image_link = image_link)



@app.route('/form9', methods = ['GET', 'POST'])
def form9():

    form = ContactForm()
    addresslist = Addresses()


    #image from the Google Street View Location
    image_link = get_streetview_link(addresslist.address9)[0]

    # extracting info from address
    address_split = address_splitter(address = addresslist.address9)
    address_main = address_split[0]
    address_zip = address_split[1]
    address_city = address_split[2]
    address_state = address_split[3]
    address_country = address_split[4]

    # zillow request
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    house_type = zillowresult.home_type
    house_size = zillowresult.home_size
    year = zillowresult.year_built
    num_beds = zillowresult.bedrooms
    num_baths = zillowresult.bathrooms.strip('.0')
    est_value = zillowresult.zestimate_amount
    est_date = zillowresult.zestimate_last_updated
    latitude = zillowresult.latitude
    longitude = zillowresult.longitude
    val_desc = "Zestimate"
    if est_value == None:
        est_value = zillowresult.tax_value
        est_date = zillowresult.tax_year
        val_desc = "Tax Assessment"

    onemarkermap = Map(
        identifier="view-side",
        lat=latitude,
        lng=longitude,
        zoom = 19,
        markers=[(latitude, longitude)],
        style="float:right; height:550px;width:640px;margin:0;",
        margin=0,
        )

    return render_template('fullform.html', form=form, onemarkermap=onemarkermap, address_main=address_main, address_zip=address_zip, address_city=address_city, address_state=address_state, address_country=address_country, bldg_type=house_type, bldg_size=house_size, built_year=year, beds=num_beds, baths=num_baths, value=est_value, val_date=est_date, latitude=latitude, longitude=longitude, val_desc=val_desc, image_link = image_link)



@app.route('/form10', methods = ['GET', 'POST'])
def form10():

    form = ContactForm()
    addresslist = Addresses()


    #image from the Google Street View Location
    image_link = get_streetview_link(addresslist.address10)[0]

    # extracting info from address
    address_split = address_splitter(address = addresslist.address10)
    address_main = address_split[0]
    address_zip = address_split[1]
    address_city = address_split[2]
    address_state = address_split[3]
    address_country = address_split[4]

    # zillow request
    zillowresult = zillow_query(address=address_main, zipcode=address_zip, key=keys.zillow)
    house_type = zillowresult.home_type
    house_size = zillowresult.home_size
    year = zillowresult.year_built
    num_beds = zillowresult.bedrooms
    num_baths = zillowresult.bathrooms.strip('.0')
    est_value = zillowresult.zestimate_amount
    est_date = zillowresult.zestimate_last_updated
    latitude = zillowresult.latitude
    longitude = zillowresult.longitude
    val_desc = "Zestimate"
    if est_value == None:
        est_value = zillowresult.tax_value
        est_date = zillowresult.tax_year
        val_desc = "Tax Assessment"

    onemarkermap = Map(
        identifier="view-side",
        lat=latitude,
        lng=longitude,
        zoom = 19,
        markers=[(latitude, longitude)],
        style="float:right; height:550px;width:640px;margin:0;",
        margin=0,
        )

    return render_template('fullform.html', form=form, onemarkermap=onemarkermap, address_main=address_main, address_zip=address_zip, address_city=address_city, address_state=address_state, address_country=address_country, bldg_type=house_type, bldg_size=house_size, built_year=year, beds=num_beds, baths=num_baths, value=est_value, val_date=est_date, latitude=latitude, longitude=longitude, val_desc=val_desc, image_link = image_link)



# Source: Miguel Grinberg https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
