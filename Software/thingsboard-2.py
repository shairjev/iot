#! python3.4

import paho.mqtt.client as mqtt
import time,json,random
broker="192.168.1.184"
#broker="broker.hivemq.com"
broker="demo.thingsboard.io"
#broker="iot.eclipse.org"
port =1883

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
   pass
   #print("In on_pub callback mid= "  ,mid)
count=0
mqtt.Client.connected_flag=False#create flag in class
mqtt.Client.suppress_puback_flag=False
client = mqtt.Client("python1")             #create new instance 
#client.on_log=on_log
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
username="aSJxxNTVEu5QtHCRERtH"
password=""
if username !="":
    client.username_pw_set(username, password)

client.connect(broker,port)           #establish connection
#client.loop_start()
while not client.connected_flag: #wait in loop
   client.loop()
   print("In wait loop")
   time.sleep(1)
time.sleep(3)
print("publishing qos of 1")

#######
class Sensor:
   def __init__(self,client,topic,qos,change,interval,direction,\
                start_value,min_value,max_value):
      self.client=client
      self.change_up=change
      self.change_down= -change
      self.change=change
      self.interval=interval
      self.temp=start_value
      self.max_value=max_value
      self.min_value=min_value
      self.direction=direction
      self.topic=topic
      self.qos=qos
      
   def random_change(self):
     a=random.randint(0,10)
     b=random.randint(0,25)
     print("direction =",self.direction)
     if b==6 and self.direction=="up": 
         self.direction="down"
         #print("Reversing")
     elif b==6 and self.direction=="down":#decreasing temperature
         self.direction="up"
         #print("Reversing")
     if self.direction=="up":
         self.change=self.change_up
     else:
         self.change=self.change_down    
     if a==5 and self.direction=="up":
          self.change=self.change_down
     elif a==5 and self.direction=="down":
         self.change=self.change_up
   def publish(self,data_out):
      print("data out=",data_out)
      self.client.publish(self.topic,data_out,self.qos)    #publish
      
   def update(self):
      self.random_change()
      self.temp=self.temp+self.change
   def start(self):
     while True:
         self.update()
         self.client.loop(0.01)
         if self.temp>=self.max_value:
             self.temp=self.max_value
         if self.temp<=self.min_value:
             self.temp=self.min_value

         #print("temp =",self.temp)
         if json_data_flag:
            data=dict()
            data["room-temp"]=self.temp
            data_out=json.dumps(data)
         else:
            data_out=self.temp
         self.publish(data_out)
         #print("change is ",self.change)
         time.sleep(self.interval)
json_data_flag=True #publish as Json encoded data
topic="v1/devices/me/telemetry"
qos=0
change=0.5
interval=2
direction="up"
min_value=0
max_value=30
start_value=20
s=Sensor(client,topic,qos,change,interval,direction,start_value,min_value,max_value)
s.start()
     

client.disconnect()



