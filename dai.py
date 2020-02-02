from iottalkpy import dan
from geopy.geocoders import Nominatim
import random, time, requests
from config import (IoTtalk_URL, username,
                    device_addr, device_name, device_model,
                    idf_list, odf_list,
                    time_interval)

''' IoTtalk data handler '''
def on_data(odf_name, data):
    dan.log.info(f"[da] {odf_name}: {data}")

def on_signal(signal, df_list):
    dan.log.info('[cmd] %s, %s', signal, df_list)

def on_register():
    dan.log.info('[da] register successfully')

def on_deregister():
    dan.log.info('[da] register fail')

''' IoTtalk registration '''
context = dan.register(
    IoTtalk_URL,
    on_signal=on_signal,
    on_data=on_data,
    idf_list=idf_list,
    odf_list=odf_list,
    accept_protos=['mqtt'],
    name=device_name,
    #id_=device_addr,
    profile={
        'model': device_model,
        'u_name': username
    },
    on_register=on_register,
    on_deregister=on_deregister
)

# Locolization Setting
'''geolocator = Nominatim(user_agent="Google Maps")
location = geolocator.geocode("Taichung, Taiwan")'''

ip_request = requests.get('https://get.geojs.io/v1/ip.json')
my_ip = ip_request.json()['ip']

geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
geo_request = requests.get(geo_request_url)
geo_data = geo_request.json()

while True:
    dan.push('Dummy_Sensor', [random.randint(0, 100), geo_data['latitude'], geo_data['longitude']])
    time.sleep(time_interval)