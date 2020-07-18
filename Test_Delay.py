from iottalkpy import dan
import time
from config import (IoTtalk_URL, username,
                            device_name, device_model,
                            idf_list, odf_list)
counter = 0
delays = 0

''' IoTtalk data handler '''
def on_data(odf_name, data):
    global counter, delays
    counter += 1
    delay = time.time() - data[0]
    delays += delay
    print(f'{delay} second')
    if counter == 100:
        print(f'average {delays / 100} second')
        exit()

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

while True:
    dan.push('Dummy_Sensor', [time.time()])
    time.sleep(0.01)