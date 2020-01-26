from iottalkpy import dan
#from geopy.geocoders import Nominatim
import random, time
from config import (IoTtalk_URL, username,
                    device_addr, device_name, device_model,
                    idf_list, odf_list)

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
    id_=device_addr,
    profile={
        'model': device_model,
        'u_name': username
    },
    on_register=on_register,
    on_deregister=on_deregister
)

# Get location
'''geolocator = Nominatim()
location = geolocator.geocode("175 5th Avenue NYC")
print(location.addres)'''

while True:
    dan.push('Dummy_Sensor', [random.randint(1,10)])
    time.sleep(10)