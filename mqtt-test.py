import paho.mqtt.client as mqtt
import time

time1=0

#========= For MQTT ===========
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    
def on_message(mqttc, obj, msg):
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    msg_buff = msg.topic + " " + str(msg.qos) + " " + str(msg.payload)
    msg_topic = msg.topic
    print (msg_buff)
    
def on_publish(mqttc, obj, mid):
    pass
    #print("publish: " + str(mid))
    
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
    
def on_log(mqttc, obj, level, string):
    print(string)

#MQTT Connection
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
ready_f=0
while 1:    
    try:
        mqttc.connect("192.168.10.151", 1883, 60)
        ready_f=1
    except:
        print ('Waiting for the server...')
        time.sleep(1)
    if ready_f==1:
        break
# subscribe data that is received from photon particle
mqttc.subscribe("ev_second", 0)
# mqttc.subscribe("downtime")

while 1:
    mqttc.loop(timeout=0.001)

    time1=time1+1
    if time1 >= 5000000:   #Send data to billboard every second
        try:
            pass
            #mqttc.publish("ev_second",'data',0);
        except:
            print("There is an error on Sending Data!");
        time1=0
