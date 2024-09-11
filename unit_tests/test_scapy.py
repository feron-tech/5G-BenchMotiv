from scapy.all import *

# Create a TCP SYN packet
packet = IP(dst="192.168.1.1")/TCP(dport=80, flags="S")

# Send the packet and receive the response
response = sr1(packet)

# Print the response
print(response)