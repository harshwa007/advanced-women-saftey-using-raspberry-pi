import sendmail
from twilio.rest import Client
import serial
import time
import string
import pynmea2
from geopy.geocoders import Nominatim
import gps

lat=gps.lat2
lng=gps.lng2
 

def send_alert():

# Initialize Nominatim API
    geolocator = Nominatim(user_agent="geoapiExercises")

# Assign Latitude & Longitude
    Latitude = str(lat)
    Longitude = str(lng)
# Get location with geocode
    location = geolocator.geocode(Latitude+","+Longitude)

# Display location
    print("\nLocation of the given Latitude and Longitude:")
    print(location)


    account_sid = ''
    auth_token = ''
    twilio_number = ''

    client = Client(account_sid, auth_token)
#bb = 'GPS Location is:----\n'+gps+'\nLocation of the given Latitude and Longitude:'+location
    bb=gps.gps1+str(location)
    message = client.messages.create(
        body=bb, from_=twilio_number, to='number')
    print(message.body)

    call = client.calls.create(
        twiml='<Response><Say>help me please! I am in danger my location is send to you via message</Say></Response>', to='', from_='')
    print(call.sid)
