import paho.mqtt.client as mqttClient
import time
import os
import subprocess

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected =True
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    if message.payload == 'ON':
        print "Message received: " + message.topic + " : " + message.payload
        os.system('clear')
        time.sleep(1.5)
        if message.topic == 'Misc/PrayerTrigger':
            subprocess.Popen(["omxplayer", "/home/pi/share/adhan.mp4", "--aspect-mode", "fill"])
        else:
            subprocess.Popen(["omxplayer", "/home/pi/share/adhanfajr.mp4", "--aspect-mode", "fill"])

Connected = False

broker_address = "XXX.XXX.XXX.XXX" #Your MQTT broker IP address
port = 1883 #default port change as required
user = "xxxxxx" #mqtt user name change as required
password = "xxxxxxxx" #mqtt password change as required
client = mqttClient.Client("prayertime")
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=port)
client.loop_start()

while Connected != True:
    time.sleep(0.1)

client.subscribe('Misc/PrayerTrigger')
client.subscribe('Misc/PrayerTriggerFajr')

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print "exiting"
    client.disconnect()
    client.loop_stop()
