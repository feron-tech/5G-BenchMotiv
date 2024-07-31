import json
import subprocess
import re
#from influxdb_client import InfluxDBClient, Point, WritePrecision
#from influxdb_client.client.write_api import SYNCHRONOUS
import time

# Target server IP
server_ip = "192.168.0.241"
#config_file = 'configfile_tcp.json'


# Load configuration from file
def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config


def run_owping(host,count):
    command = ["owping", "-c", str(count), host]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout


def parse_owping_output(output):
    measurements = []
    sections = output.strip().split('\n\n')
    for section in sections:
        lines = section.split('\n')
        if len(lines) < 9:
            continue
        x = 0
        if re.search(r'owping', lines[0]) is None:
            x = 1
        # src_dst = re.search(r'from \[(.*)\]:\d+ to \[(.*)\]:\d+', lines[0])
        # sid = re.search(r'SID:\s+(\w+)', lines[1]).group(1)
        # first = re.search(r'first:\s+([^\s]+)', lines[2]).group(1)
        # last = re.search(r'last:\s+([^\s]+)', lines[3]).group(1)
        packets = re.search(r'(\d+) sent, (\d+) lost \(([^)]+)\), (\d+) duplicates', lines[4 + x])
        delay = re.search(r'one-way delay min/median/max = ([^/]+)/([^/]+)/([^ ]+) ms', lines[5 + x])
        jitter = re.search(r'jitter = ([^ ]+) ms', lines[6 + x]).group(1)
        hops = re.search(r'hops = (\d+)', lines[7 + x]).group(1)
        reordering = re.search(r'no reordering', lines[8 + x]) is not None

        measurement = {
            "packets_sent": int(packets.group(1)),
            "packets_lost": int(packets.group(2)),
            "loss_percentage": float(packets.group(3).replace('%', '')),
            "duplicates": int(packets.group(4)),
            "delay_min": float(delay.group(1)),
            "delay_median": float(delay.group(2)),
            "delay_max": float(delay.group(3)),
            "jitter": float(jitter),
            "hops": int(hops),
            "reordering": reordering
        }
        #write_to_influxdb(config, measurement, config['influxdb']['owamp_bucket'])
        measurements.append(measurement)
        #print(section)
    return measurements


# Function to write results to InfluxDB
def write_to_influxdb(config, results, bucket):
    client = InfluxDBClient(url=config['influxdb']['url'], token=config['influxdb']['token'],
                            org=config['influxdb']['org'])
    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = Point("owamp_results").time(time.time_ns(), WritePrecision.NS)

    for key, value in results.items():
        point = point.field(key, value)

    write_api.write(bucket=bucket, record=point)
    print("Results written to InfluxDB")


if __name__ == "__main__":
    #config = load_config(config_file)
    host='192.168.200.117'
    count=100
    owping_output = run_owping(host,count)
    measurements = parse_owping_output(owping_output)
    print(str(measurements))




