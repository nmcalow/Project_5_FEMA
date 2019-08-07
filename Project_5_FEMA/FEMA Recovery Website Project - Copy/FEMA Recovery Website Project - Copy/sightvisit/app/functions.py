"""
This file contains functions used within the SightVisit application, including:
Functions for pulling and utilizing metadata in imagery
Functions for pulling external data from APIs:
- Google Maps streetview data
- Google reverse geocode/address lookup functionality
- Zillow data on house prices and details
"""

# Route functionality
from __future__ import print_function
import math
import googlemaps
from googlemaps.distance_matrix import distance_matrix
import ortools
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd

# Package imports for dealing with images
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# Package imports for Zillow
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults

# Package imports for Google Maps APIs
import google_streetview.api

# Geocoding and reverse Geocoding
from pygeocoder import Geocoder

#API keys
from app.keys import keys

# Imagery functionality
def get_gps_details(img):
    """Function for extracting GPS data from image

    Args:
        img (.jpeg / .png et al.): an image file

    Returns:
        Dictionary with following key: value pairs:
            'GPSLatitudeRef': str = 'N' or 'S'
            'GPSLatitude': tuple of tuples,
            'GPSLongitudeRef': str = 'E' or 'W',
            'GPSLongitude': tuple of tuples,
            'GPSAltitudeRef': byte string,
            'GPSAltitude': tuple,
            'GPSTimeStamp': tuple of tuples,
            'GPSSpeedRef': str,
            'GPSSpeed': tuple,
            'GPSImgDirectionRef': str,
            'GPSImgDirection': tuple,
            'GPSDestBearingRef': str,
            'GPSDestBearing': tuple,
            'GPSDateStamp': str representing datetime,
            'GPSHPositioningError': tuple}
    """
    gpsinfo = {}
    exif = {TAGS[k]: v for k, v in img._getexif().items() if k in TAGS}
    for item in exif['GPSInfo'].keys():
        name = GPSTAGS.get(item, item)
        gpsinfo[name] = exif['GPSInfo'][item]
    return gpsinfo


def convert_to_degress(coords):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format

    Credit should be provided to Shadab Zafar; see his GitHub at
    https://gist.github.com/dufferzafar/f455099332ade457599cf97070a930b6

    Args:
        coords (tuple): coordinates in degrees as nested tuple, where tuple[0] corresponds with hours, tuple[1] corresponds with minutes, and tuple[2] (optional) corresponds with seconds

    Returns:
        (float): coordinates as float number
    """
    deg_num, deg_denom = coords[0]
    d = float(deg_num) / float(deg_denom)
    min_num, min_denom = coords[1]
    m = float(min_num) / float(min_denom)
    try:
        sec_num, sec_denom = coords[2]
        s = float(sec_num) / float(sec_denom)
    except:
        s = 0
    return d + (m / 60.0) + (s / 3600.0)


def get_img_coord_str(img):
    """Function for extracting latitude, longitude coordinates from image as string result

    Args:
        img (.jpeg / .png et al.): an image file

    Returns:
        (str): GPS coordinates as 'latitude,longitude'
    """

    lat = convert_to_degress(get_gps_details(img)['GPSLatitude'])
    if get_gps_details(img)['GPSLatitudeRef'] == 'S':
        lat = -lat

    longitude = convert_to_degress(get_gps_details(img)['GPSLongitude'])
    if get_gps_details(img)['GPSLongitudeRef'] == 'W':
        longitude = -longitude

    return str(lat) + ',' + str(longitude)


def get_img_coord_tuple(img):
    """Function for extracting latitude, longitude coordinates from image as numerical result

    Args:
        img (.jpeg / .png et al.): an image file

    Returns:
        (tuple): latitude and logitudes coordinates as floats
    """

    lat = convert_to_degress(get_gps_details(img)['GPSLatitude'])
    if get_gps_details(img)['GPSLatitudeRef'] == 'S':
        lat = -lat

    longitude = convert_to_degress(get_gps_details(img)['GPSLongitude'])
    if get_gps_details(img)['GPSLongitudeRef'] == 'W':
        longitude = -longitude

    return lat, longitude


# Google Maps streetview functionality
def pull_streetview(location,
                        size='640x480',
                        fov='90',
                        pitch='0',
                        radius='50',
                        key=keys.google,
                        heading=None):
    """Function for obtaining google streetview image for a given location (either address or latitude,longitude; formated as str)

    Args:
        location (str): location either as address or lat./long.

        size (str): (default='(640x480)') size of the outputted image in pixels

        fov (str): (default='90')

        ptich (str): (default='0')

        key (str): (default=keys.google) google streetview api key

        heading (str): (default=None)

    Returns:
        downloads photo of streetview
    """
    try:
        filename = location.replace(' ', '_')
    except:
        filename = round(time.time(), 0)
    params = [{
        'size': size,
        'location': location,
        'fov': fov,
        'pitch': pitch,
        'radius': radius,
        'key': key
    }]
    if heading != None:
        params[0]['heading'] = heading

    results = google_streetview.api.results(params)
    results.download_links('./app/img')

def get_streetview_link(location,
                        size='640x480',
                        fov='90',
                        pitch='0',
                        radius='50',
                        key=keys.google,
                        heading=None):
    """Function for obtaining google streetview image for a given location (either address or latitude,longitude; formated as str)

    Args:
        location (str): location either as address or lat./long.

        size (str): (default='(640x480)') size of the outputted image in pixels

        fov (str): (default='90')

        ptich (str): (default='0')

        key (str): (default=keys.google) google streetview api key

        heading (str): (default=None)

    Returns:
        url with most recent google streetview photo
    """
    params = [{
        'size': size,
    	'location': location,
        'fov': fov,
    	'pitch': pitch,
        'radius': radius,
    	'key': keys.google
    }]
    if heading != None:
        params[0]['heading'] = heading

    results = google_streetview.api.results(params)
    return results.links

def reverse_lookup(lat, long, key=keys.google):
    """Function for lookup of addresses from latitude, longitude details using Google Maps API

    Args:
        lat (float): latitude as float

        long (float): longitude as float

        key (str): (default=keys.google) google maps api key

    Returns:
        returns a tuple with address (str), zipcode (str)
        """
    result = str(Geocoder(api_key=key).reverse_geocode(lat, long))
    location_details = result.split(",")
    address = location_details[0]
    zipcode = location_details[-2][-5:]
    city = location_details[1]
    state = location_details[2].split(" ")[1]
    return address, zipcode, city, state


# Zillow functionality
def zillow_query(address, zipcode, key=keys.zillow):
    """Function for obtaining data for a given address location

    Args:
        address (str): street address

        zipcode (str): zipcode corresponding with street address

        key (str): (default='YOURAPIKEYHERE') zillow api key

    Returns:
        returns a GetDeepSearchResults object which has following attributes available:
            'zillow_id'
            'home_type'
            'home_detail_link'
            'graph_data_link'
            'map_this_home_link'
            'latitude'
            'longitude'
            'tax_year'
            'tax_value'
            'year_built'
            'property_size'
            'home_size'
            'bathrooms'
            'bedrooms'
            'last_sold_date'
            'last_sold_price'
            'zestimate_amount'
            'zestimate_last_updated'
            'zestimate_value_change'
            'zestimate_valuation_range_high'
            'zestimate_valuationRange_low'
            'zestimate_percentile'
    """
    zillow_data = ZillowWrapper(key)
    deep_search_response = zillow_data.get_deep_search_results(
        address, zipcode)
    result = GetDeepSearchResults(deep_search_response)
    return result

# extracts info from address string, zip, city, state, country
def address_splitter(address):
    address_main = address.split(',')[0]
    address_zip = address.split()[-2:][0].strip(',')
    address_city = address.split(',')[1]
    address_state = address.split()[-3:][0].strip(',')
    address_country = address.split(',')[3]
    return address_main, address_zip, address_city, address_state, address_country



def auth_list(address1, address2 = "", address3 = "",
              address4 = "", address5 = "", address6 = "",
              address7 = "", address8 = "", address9 = "",
              address10 = ""): #authenticates each address and returns a list for get_times
    client = googlemaps.Client(key = keys.google)
    list_in = list([address1, address2, address3, address4, address5, address6, address7, address8, address9, address10])
    list_out = []
    for item in list_in:
        try:
            location = googlemaps.places.find_place(client, item, 'textquery')
            if location['status'] == 'OK': #Checks to ensure the address actually exists in some form
                list_out.append(item)
        except: #certain string formats will throw errors. Catches them and does not add them to the final lsit
            pass
    return list_out


def build_matrix(matrix): #Takes the distance matrix dictionary into a DataFrame
    final = pd.DataFrame(columns = matrix['destination_addresses'], index = matrix['origin_addresses'])
    for col_count, col in enumerate(matrix['destination_addresses']):#column for loop
        for row_count, row in enumerate(matrix['origin_addresses']): #row for loop
            #proper dig through the dictionary
            final[row][col] = matrix['rows'][col_count]['elements'][row_count]['duration']['value']
    return final

def get_times(destinations): #Takes in a list of addresses
    client = googlemaps.Client(key = keys.google)
    matrix = distance_matrix(client = client,
                             origins = destinations, #Makes it a symmetrical 2D array
                             destinations = destinations,
                             mode = 'driving', #If methods change, or want added funcionality, mode goes here
                            language = 'english',
                            units = 'imperial') #Same goes for units(metric)
    return build_matrix(matrix)


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    # Locations in block units
    data['locations'] = [
    ]  # yapf: disable
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def compute_euclidean_distance_matrix(locations):
    """Creates callback to return distance between points."""
    distances = {}
    distances_df=get_times(locations)
    print(distances_df)
    print(distances_df.iloc[0,0])
    print(distances_df.iloc[0,1])
    print(distances_df.iloc[0,2])
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            distances[from_counter][to_counter] = (int(
            distances_df.iloc[from_counter,to_counter]))
    return distances

def set_address_path(manager, routing, assignment,data_locations):
    """Output assignment in variables address1,...address10"""
    assignment.ObjectiveValue()
    index = routing.Start(0)
    route_distance = 0
    address_list=[]
    while not routing.IsEnd(index):
        cur_node=manager.IndexToNode(index)
#         print('what are: index,cur_node=',index,cur_node)
        address_list.append(data_locations[cur_node])
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    manager.IndexToNode(index)
#     print('almost there: ',address_list)
    address1=address_list[0]
    address2=address_list[1]
    address3=address_list[2]
    address4=address_list[3]
    address5=address_list[4]
    address6=address_list[5]
    address7=address_list[6]
    address8=address_list[7]
    address9=address_list[8]
    address10=address_list[9]
    return address1,address2,address3,address4,address5,address6,address7,address8,address9,address10

def print_solution(manager, routing, assignment):
    """Prints assignment on console."""
    print('Objective: {}'.format(assignment.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Objective: {}m\n'.format(route_distance)


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # NEW SPOT TO MAKE distance_matrix
    distance_matrix = compute_euclidean_distance_matrix(destinations_1)
    manager = pywrapcp.RoutingIndexManager(
        len(destinations_1), data['num_vehicles'], data['depot'])

#     # Create the routing index manager.
#     manager = pywrapcp.RoutingIndexManager(
#         len(data['locations']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

#     distance_matrix = compute_euclidean_distance_matrix(data['locations'])
def distance_callback(from_index, to_index):
    """Returns the distance between the two nodes."""
    # Convert from routing variable Index to distance matrix NodeIndex.
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        print_solution(manager, routing, assignment)



#Wrapper for all the functions regarding routing functionality
def traveling_salesman(destinations_1):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # NEW SPOT TO MAKE distance_matrix
    distance_matrix = compute_euclidean_distance_matrix(destinations_1)
    manager = pywrapcp.RoutingIndexManager(
        len(destinations_1), data['num_vehicles'], data['depot'])

#     # Create the routing index manager.
#     manager = pywrapcp.RoutingIndexManager(
#         len(data['locations']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

#     distance_matrix = compute_euclidean_distance_matrix(data['locations'])

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
#     if assignment:
#         print_solution(manager, routing, assignment)
    if assignment:
        address1,address2,address3,address4,address5,address6,address7,address8,address9,address10=\
        set_address_path(manager, routing, assignment,destinations_1)
    return address1,address2,address3,address4,address5,address6,address7,address8,address9,address10
