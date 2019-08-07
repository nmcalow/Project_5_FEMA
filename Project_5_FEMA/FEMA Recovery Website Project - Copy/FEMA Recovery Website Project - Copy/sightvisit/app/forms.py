# request wtf and flask forms
from flask_wtf import FlaskForm, Form
# request assortmemt of field options for forms
from wtforms import TextField, IntegerField, TextAreaField, StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField
# request for valid info in TextField
from wtforms.validators import DataRequired
import pandas as pd
# request for display error
from wtforms import validators, ValidationError
from app.functions import get_gps_details, convert_to_degress, get_img_coord_str, get_img_coord_tuple, pull_streetview, reverse_lookup, zillow_query, address_splitter, get_streetview_link, build_matrix, get_times, create_data_model, compute_euclidean_distance_matrix, set_address_path, print_solution, traveling_salesman


# Login form with fields
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
# Contect for template used for Disaster Form
class ContactForm(Form):
   name = TextField("Owner Name:",[validators.Required("Please enter your name.")])
   Homes = SelectField('House Type (Conventional/Manufactured):', choices = [('C','Conventional'),('M','Manufactured')])
   Insurance = SelectField('Does the homeowner have insurance?', choices = [('Y','Yes'),('N','No'),('P','Partial')])
   Flood_Plain = SelectField('Is the property in a flood plain?', choices = [('Y','Yes'),('N','No')])
   Flood_Insurance = SelectField('Does the homeowner have flood insurance?', choices = [('Y','Yes'),('N','No')])
   Address = TextField("Address:")
   Zip_Code = TextField('Zipcode:')
   State = SelectField('State/Territory:', choices = [("Alabama","Alabama"),("Alaska","Alaska"),("Arizona","Arizona"),("Arkansas","Arkansas"),("California","California"),("Colorado","Colorado"),("Connecticut","Connecticut"),("Delaware","Delaware"),("Florida","Florida"),("Georgia","Georgia"),("Hawaii","Hawaii"),("Idaho","Idaho"),("Illinois","Illinois"),("Indiana","Indiana"),("Iowa","Iowa"),("Kansas","Kansas"),("Kentucky","Kentucky"),("Louisiana","Louisiana"),("Maine","Maine"),("Maryland","Maryland"),("Massachusetts","Massachusetts"),("Michigan","Michigan"),("Minnesota","Minnesota"),("Mississippi","Mississippi"),("Missouri","Missouri"),("Montana","Montana"),("Nebraska","Nebraska"),("Nevada","Nevada"),("New Hampshire","New Hampshire"),("New Jersey","New Jersey"),("New Mexico","New Mexico"),("New York","New York"),("North Carolina","North Carolina"),("North Dakota","North Dakota"),("Ohio","Ohio"),("Oklahoma","Oklahoma"),("Oregon","Oregon"),("Pennsylvania","Pennsylvania"),("Puerto Rico","Puerto Rico"),("Rhode Island","Rhode Island"),("South Carolina","South Carolina"),("South Dakota","South Dakota"),("Tennessee","Tennessee"),("Texas","Texas"),("Utah","Utah"),("Vermont","Vermont"),("Virginia","Virginia"),("Washington","Washington"),("West Virginia","West Virginia"),("Wisconsin","Wisconsin"),("Wyoming","Wyoming")])
   Flood_NonFlood = SelectField('Damage (Flood/Non-Flood)?', choices = [('fld', 'Flood'),('nfld', 'Non-Flood')])
   Damage_Level = SelectField('Damage Level', choices = [('Inex', 'Inaccessible'),
      ('ds', 'Destroyed'),('maj', 'Major'),('min', 'Minor'),('aff', 'Affected')])
   email = TextField("Email:",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
   submit = SubmitField("Send")


class Addresses():
    address1 = '35 Commonwealth Park, Newton, MA 02459, USA'
    address2 = '29 Commonwealth Park, Newton, MA 02459, USA'
    address3 = '26 Commonwealth Park, Newton, MA 02459, USA'
    address4 = '20 Commonwealth Park, Newton, MA 02459, USA'
    address5 = '19 Commonwealth Park, Newton, MA 02459, USA'
    address6 = '16 Commonwealth Park, Newton, MA 02459, USA'
    address7 = '15 Commonwealth Park, Newton, MA 02459, USA'
    address8 = '7 Commonwealth Park, Newton, MA 02459, USA'
    address9 = '36 Commonwealth Park, Newton, MA 02459, USA'
    address10 = '35 Royce Rd, Newton Centre, MA 02459, USA'

    addresslist = [address1,address2,address3,address4,address5,address6,address7,address8,address9,address10]


    address1,address2,address3,address4,address5,address6,address7,address8,address9,address10 = traveling_salesman(addresslist)



# Source: Miguel Grinberg https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
# Source: Lalith Polepeddi https://code.tutsplus.com/tutorials/intro-to-flask-adding-a-contact-page--net-28982
