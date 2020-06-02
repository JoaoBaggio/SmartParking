import paho.mqtt.client as mqtt
import json
import time

client = mqtt.Client()
client.username_pw_set("8qttpktuerb8", "wBlCJgB8hbJU")
#client.connect("mqtt.demo.konkerlabs.net", 1883)
#client.publish("data/8qttpktuerb8/pub/Vagas", 88)


while(1):
    for i in range(100):
        client.connect("mqtt.demo.konkerlabs.net", 1883)
        client.publish("data/8qttpktuerb8/pub/Vagas", i)
        time.sleep(1)
    for i in range(99, -1, -1):
        client.connect("mqtt.demo.konkerlabs.net", 1883)
        client.publish("data/8qttpktuerb8/pub/Vagas", i)
        time.sleep(1)

