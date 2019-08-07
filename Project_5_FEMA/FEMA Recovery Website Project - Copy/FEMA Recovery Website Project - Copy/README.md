# Streetview Project: FEMA Damage Assessment with Google Street View

## Group Introduction

Our team is Nick Calow, Adrian Garrido, and Scott Cohen

## Problem Statement:

After a natural disaster such as a hurricaine or tornado, FEMA send agents to perform in-person damage assesment. Our project aims to assist them in providing a platform to help those agents navigate their daily assignments. Agents will input a list of addresses through which they will be navigated from site to site based on the optimal route. Once there, agents will be able to view an image before the disaster using Google Street View, access relevant details of the structure using Zillow, and enter relevant details into a generated web form, such as condition of foundation, any structural damages, and additional comments.

## Methodology:

The heart of choosing the route for the person visiting the houses is the well-known traveling salesman problem. The traveling salesman problem asks, for a sequence of locations and the distance between every pair of locations, what is the shortest distance that one can travel and still visit all the locations. It is well-known because there is no known exact solution to it when we have a large number of locations. There, however, are "good" solutions which may or may not be exact; no one knows. A good solution is simply some route that is not obvious how to improve and that people can accept.

Good solutions are provided by tools written by Google. They are called ortools by Google ("or" is probably "operation research" where people study problems like the traveling salesman problem). It is easy to integrate input to the ortools with other Google packages such as Google Maps. That fit in well with the needs of our group project.

## Running the app

- Donwload the appropriate packages from the requirements.txt file. Download any aditional packages that prompt an error when trying to run the application, by running 'pip install [name of package]' in the terminal.

- Go to the 'sightvisit' folder in your terminal. Then run 'extract FLASK_APP=main_page.py.

- Run the command 'flask run'.

- A url should show up at the bottom like this: http://127.0.0.1:5000/

- Go to the url in your browser.

- Make sure to shut down the site by doing 'Ctrl + C' in the terminal

## Resources

- Work of previous DC cohort. Used their general website template and some of the work they did for their form. Their github page can be found (here)[https://github.com/wkarney/street_viewing_for_FEMA]

- Flask tutorial used for general understanding can be found (here)[https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world] 

- (Google Maps API)[https://github.com/googlemaps/google-maps-services-python]

- (Google Street View API)[https://pypi.org/project/google-streetview/]

- (PyZillow)[https://pypi.org/project/pyzillow/]

- (OR Tools by Google)[https://developers.google.com/optimization/]

Note that Google charges for API calls to its Google Maps APIs, but provides a free 1-year $300 credit to its Cloud Platform.


## Opportunities for Future Development:

- Better web form funtionality
- Phone App
- Automatic route guidance between addresses
- Metrics from agent reports
.