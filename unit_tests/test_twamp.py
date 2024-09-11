import json
import subprocess
import re
from datetime import datetime
#from influxdb_client import InfluxDBClient, Point, WritePrecision
#from influxdb_client.client.write_api import SYNCHRONOUS
import socket
import time

config_file = 'configfile_tcp.json'


# Load configuration from file
def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config


# Execute the twping command and get the results
def run_twping(host,count):

    cmd = ["twping", "-c", str(count), host]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error running twping: {result.stderr}")
        return None
    return result.stdout


# Parse the twping output
def parse_twping_output(output):
    data = {}
    lines = output.split('\n')
    print(output)
    for line in lines:
        if "sent, " in line:
            match = re.search(r"(\d+) sent, (\d+) lost \(([\d\.]+)%\)", line)
            if match:
                data["sent"] = int(match.group(1))
                data["lost"] = int(match.group(2))
                data["loss_percentage"] = float(match.group(3))
        elif "round-trip time min/median/max" in line:
            match = re.search(r"([\d\.]+)/([\d\.]+)/([\d\.]+) ms", line)
            if match:
                data["rtt_min"] = float(match.group(1))
                data["rtt_median"] = float(match.group(2))
                data["rtt_max"] = float(match.group(3))
        elif "send time min/median/max" in line:
            match = re.search(r"([\d\.]+)/([\d\.]+)/([\d\.]+) ms", line)
            if match:
                data["send_min"] = float(match.group(1))
                data["send_median"] = float(match.group(2))
                data["send_max"] = float(match.group(3))
        elif "reflect time min/median/max" in line:
            match = re.search(r"([\d\.-]+)/([\d\.-]+)/([\d\.-]+) ms", line)
            if match:
                data["reflect_min"] = float(match.group(1))
                data["reflect_median"] = float(match.group(2))
                data["reflect_max"] = float(match.group(3))
        elif "reflector processing time min/max" in line:
            match = re.search(r"([\d\.]+)/([\d\.]+) ms", line)
            if match:
                data["reflector_min"] = float(match.group(1))
                data["reflector_max"] = float(match.group(2))
        elif "two-way jitter" in line:
            match = re.search(r"([\d\.]+) ms", line)
            if match:
                data["two_way_jitter"] = float(match.group(1))
        elif "send jitter" in line:
            match = re.search(r"([\d\.]+) ms", line)
            if match:
                data["send_jitter"] = float(match.group(1))
        elif "reflect jitter" in line:
            match = re.search(r"([\d\.]+) ms", line)
            if match:
                data["reflect_jitter"] = float(match.group(1))
    return data


# Send the parsed data to InfluxDB
def send_to_influxdb(config, results):
    client = InfluxDBClient(url=config['influxdb']['url'], token=config['influxdb']['token'],
                            org=config['influxdb']['org'])
    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = Point("twamp_results").time(time.time_ns(), WritePrecision.NS)

    for key, value in results.items():
        point = point.field(key, value)

    write_api.write(bucket=config['influxdb']['twamp_bucket'], record=point)
    print("Results written to InfluxDB")


def main(host,count):
    #config = load_config(config_file)
    output = run_twping(host,count)
    if output:
        data = parse_twping_output(output)
        if data:
            print(str(data))
            #send_to_influxdb(config, data)
        else:
            print("Failed to parse twping output.")
    else:
        print("Failed to execute twping command.")


if __name__ == "__main__":
    host='192.168.200.117'
    count=100
    main(host,count)
