import time
import paho.mqtt.client as mqtt
import sys

BROKER_HOST = "localhost"
BROKER_PORT = 1883

TOPICS = ["temperature","windspeed","visibility"]
USER= {"temperature":"sub1","windspeed":"sub2","visibility":"sub3"}
PASSWORD = {"temperature":"test1","windspeed":"test2","visibility":"test3"}
QOS = {"temperature":0,"windspeed":1,"visibility":0}
RETAIN = {"temperature":False,"windspeed":False,"visibility":True}


def on_connect(client,userdata,flags,rc):
    print(f"[SUBSCRIBER] Connected with result code {rc}")
    client.subscribe(userdata['topic'],userdata['qos'],userdata['retain'])
    print(f"[SUBSCRIBER] Subscribed to topic:{userdata['topic']}")

def on_message(client,userdata,msg):
    print("[SUBSCRIBER] Message received!")
    print(f"        Topic:{msg.topic}")
    print(f"        Payload:{msg.payload.decode('utf-8')}")
    print(f"        QoS:{msg.qos}")
    print(f"        Retained:{msg.retain}")

def main(topic):
    client = mqtt.Client(client_id="python-subscriber") 

    userdata = {"topic":topic,"qos":QOS[topic],"retain":RETAIN[topic]}
    client.on_connect = on_connect
    client.on_message = on_message
    client.user_data_set(userdata)
    client.username_pw_set(username=USER[topic],password=PASSWORD[topic])
    client.connect(BROKER_HOST,BROKER_PORT,keepalive=60)
    
    print("Waiting for messages... Press Ctrl+C to exit.")
    client.loop_forever()

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Usage: subscriber.py <arg1>")
        sys.exit(1)
    elif sys.argv[1] in TOPICS:
        main(sys.argv[1])
    else:
        print("The parameter can only be temperature/windspeed/visibility")

