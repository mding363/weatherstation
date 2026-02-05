import time
import paho.mqtt.client as mqtt
import ssl
import random
import json
from datetime import datetime

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC_TEMPERATURE = "temperature"
TOPIC_WINDSPEED = "windspeed"
TOPIC_VISIBILITY = "visibility"
UNIT = {"temperature":"degree celsius","windspeed":"m/s","visibility":"m"}

X = 6 #second
#In the first time, generate a random temperature/windspeed/visibility
#Afterwards,every new random value will be generated according to the previous value
#To avoid the value changes too quick in 1 mins, keep the value in 2 decimal


#The temperature range is between -40 and 50 degree celsius 
def temperature_sensor(last_value):
    if last_value == -1000:
        return round(random.uniform(-40,50),2)
    else:
        return round(last_value + random.uniform(-1,1),2)

#The windspeed range is between 0 and 113 m/s    
def windspeed_sensor(last_value):
    if last_value == -1000:
        return round(random.uniform(0,113),2)
    else:
        return round(last_value + random.uniform(-10,10),2)

#The runway visual range is between 50 and 2000 m
def visibility_sensor(last_value):
    if last_value == -1000:
        return round(random.uniform(50,2000),2)
    else:
        return round(last_value + random.uniform(-2,2),2)

def save2json(p_count,p_time,p_temperature,p_windspeed,p_visibility):
    filename = "record/record"+str(p_count)+".json"
    record = {"time":p_time,"temperature":p_temperature,\
              "windspeed":p_windspeed,"visibility":p_visibility}
    with open(filename,'w') as fp:
        json.dump(record,fp)

def on_connect(client,userdata,flgs,rc):
    print(f"[PUBLISHER] Connected with result code {rc}")

def main():
    print(f"[PUBLISHER] Connecting to broker at {BROKER_HOST}:{BROKER_PORT}...")

    client = mqtt.Client(client_id="python-publisher")
    client.username_pw_set(username='ivy',password="test")
    client.on_connect = on_connect
    client.connect(BROKER_HOST,BROKER_PORT,keepalive=60)
    client.loop_start()

    try:
        temperature = -1000
        windspeed = -1000
        visibility = -1000
        counter = 0
        while True:
            counter = counter + 1
            
            #generate sensor value
            temperature = temperature_sensor(temperature)
            windspeed = windspeed_sensor(windspeed)
            visibility = visibility_sensor(visibility)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            save2json(counter,timestamp,temperature,windspeed,visibility)

            message_temperature = f"The temperature is {temperature} {UNIT['temperature']}"
            message_windspeed = f"The wind speed is {windspeed} {UNIT['windspeed']}"
            message_visibility = f"The visibility is {visibility} {UNIT['visibility']}"

            #publish message
            client.publish(TOPIC_TEMPERATURE, payload=message_temperature,qos=0)
            client.publish(TOPIC_WINDSPEED,payload=message_windspeed,qos=1)
            client.publish(TOPIC_VISIBILITY,payload=message_visibility,retain=True)
            print (f"[PUBLISHER] publishing message: temperature is {temperature},windspeed is {windspeed}, and visibility is {visibility}")
  
            time.sleep(X)
    except KeyboardInterrupt:
        print("\n[PUBLISHER] Stopping publisher...")
    finally:
        client.loop_stop()
        client.disconnect()
        print("[PUBLISHER] Disconnected from broker.")

if __name__ == "__main__":
    main()            
