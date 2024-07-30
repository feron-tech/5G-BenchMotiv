# sniffer
```python
sudo apt install tshark
$ sudo apt-get install wireshark
$ sudo dpkg-reconfigure wireshark-common 
$ sudo usermod -a -G wireshark $USER
$ sudo reboot
```

```python
sudo apt install tshark
$ sudo apt-get install wireshark
$ sudo dpkg-reconfigure wireshark-common 
$ sudo usermod -a -G wireshark $USER
$ sudo reboot
```

```python
conda create --name sniffer python=3.8
conda activate sniffer 
sudo apt-get install iperf3
pip install iperf3
pip install pyshark
pip install pandas
pip install docker
pip install icmplib
pip install pyserial
git clone https://github.com/nokia/twampy
pip install paho-mqtt
pip install dash
pip install dash-bootstrap-components
```

# network at client and server
```python
sudo ufw disable
bind all addressed to 0.0.0.0
```

<!---sudo iptables -I INPUT -s 192.168.200.118 -j ACCEPT-->
<!---#sudo iptables -I OUTPUT -s 192.168.200.118 -j ACCEPT-->

<!---#sudo ufw allow from 192.168.200.117-->
<!---#sudo iptables -I INPUT -s 192.168.200.117 -j ACCEPT-->
<!---#sudo iptables -I OUTPUT -s 192.168.200.117 -j ACCEPT-->

<!---# sudo iptables -t nat -A PREROUTING -p tcp -d 192.168.2.X --dport 80 -jDNAT --to-destination 10.23.220.88:80-->
<!---#sudo iptables -t nat -A PREROUTING -d 192.168.200.117 --dport 8050 -jDNAT --to-destination 127.0.0.1:8050-->

<!---#sudo iptables -A PREROUTING -t nat -i ens18 -p tcp --dport 8050 -j DNAT --to 127.0.0.1:8050-->
<!---sudo iptables -A FORWARD -p tcp -d 127.0.0.1 --dport 8050 -j ACCEPT-->

# how to run
install all dockers at server and client + elevate sudo for docker
activate all apps at server via docker-compose-up, docker run
```python
python main_backend.py AND python main_frontend.py
```
docker build -t <image_name> . # assuming dockerfile exists
docker run  -it --rm --name=<container_name> -p 5201:5201 <image_name>
