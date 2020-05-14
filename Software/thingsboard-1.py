#! python3.4

import paho.mqtt.client as mqtt
import time,json

def on_log(client, userdata, level, buf):
   print(buf) 
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
        client.loop_stop()  
def on_disconnect(client, userdata, rc):
   print("client disconnected ok")
def on_publish(client, userdata, mid):
    print("In on_pub callback mid= "  ,mid)
count=0
mqtt.Client.connected_flag=False#create flag in class
mqtt.Client.suppress_puback_flag=False
client = mqtt.Client("python1")             #create new instance 
#client.on_log=on_log
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

broker="demo.thingsboard.io"
port =1883
topic="v1/devices/me/telemetry"
username="wmSKKBmp9O3wgPCGYpmw"
password=""
if username !="":
   pass
client.username_pw_set(username, password)
client.connect(broker,port)           #establish connection
while not client.connected_flag: #wait in loop
   client.loop()
   time.sleep(1)
time.sleep(3)
data=dict()
for i in range(100):
    data["main-light"]="ON"
    data["main-Door"]="OPEN"
    data_out=json.dumps(data) #create JSON object
    print("publish topic",topic, "data out= ",data_out)
    ret=client.publish(topic,data_out,0)    #publish
    time.sleep(5)
    client.loop()
    data["main-light"]="OFF"
    data["main-Door"]="CLOSED"
    data_out=json.dumps(data)
    print("publish topic",topic, "data out= ",data_out)
    ret=client.publish(topic,data_out,0)    #publish
    time.sleep(5)
    client.loop()    

client.disconnect()



