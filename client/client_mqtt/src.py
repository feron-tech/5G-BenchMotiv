import time
import paho.mqtt.client as mqtt
import os
import random
import string
def on_publish(client, userdata, mid, reason_code, properties):
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
_server_ip= os.environ['ENV_SERVER_IP']

_sleep_sec=os.environ['SLEEP_SEC']
_server_ip= os.environ['ENV_SERVER_IP']
_server_port= int(os.environ['ENV_SERVER_PORT'])
_max_size=int(os.environ['MAX_PAYLOAD_SIZE'])
print('Will send to ip:'+str(_server_ip)+',port='+str(_server_port))


unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish

mqttc.user_data_set(unacked_publish)
mqttc.connect(host=_server_ip, port=_server_port)
mqttc.loop_start()

# Our application produce some messages
while True:
    mytime=str(time.time())

    size = random.randint(1, _max_size)
    payload = ''.join(random.choices(string.ascii_letters + string.digits, k=size))

    msg_info = mqttc.publish(topic='golden_unit/test', payload=payload, qos=1)
    unacked_publish.add(msg_info.mid)

    time.sleep(_sleep_sec)


mqttc.disconnect()
mqttc.loop_stop()