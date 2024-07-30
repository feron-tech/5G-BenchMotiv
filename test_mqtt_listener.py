import paho.mqtt.client as paho
import random
import gparams

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("(MQTT) Connected to MQTT Broker!")
    else:
        print("(MQTT) Failed to connect, return code %d\n", rc)

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("(MQTT) Subscription established, info:" + str(mid) + " qos=" + str(granted_qos))

def on_message(client, userdata, msg):
    try:
        print('(MQTT) Received:'+str(msg.payload)+',from topic:'+str(msg.topic)+',with QoS='+str(msg.qos))
    except Exception as e:
        print('(MQTT) ERROR read msg:'+str(e))

def run(host,port):
    client = paho.Client(client_id=f'python-mqtt-{random.randint(0, 100)}', userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect

    #client.username_pw_set(global_veh._MQTT_USERNAME, global_veh._MQTT_PASSWORD)
    client.connect(host=host,port=port)

    # setting callbacks, use separate functions like above for better visibility
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    # subscribe to all topics of encyclopedia by using the wildcard "#"
    client.subscribe(topic='golden_unit/test', qos=1)

    # loop_forever for simplicity, here you need to stop the loop manually
    # you can also use loop_start and loop_stop
    client.loop_forever()

if __name__ == '__main__':
    print("(MQTT) Initializing MQTT service")
    run(host='192.168.200.117',port=gparams._PORT_SERVER_MQTT1)