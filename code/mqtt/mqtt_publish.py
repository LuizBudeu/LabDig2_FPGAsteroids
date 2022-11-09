import paho.mqtt.client as mqtt
import time
import random


client = mqtt.Client("b9ba9369-ea8a-4de1-b029-40d3b04f9d25")
client.connect("broker.emqx.io")

while True:
    a = random.randint(0, 100)
    s = 'hello world'
    client.publish("FPGAsteroids", s)
    client.publish("FPGAsteroids", a)
    print('Sent message: ' + s)
    print(f'Sent message: {a}' )
    time.sleep(5)
