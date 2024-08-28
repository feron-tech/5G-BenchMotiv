# Golden Unit

## Installation
### Client-side

https://github.com/geodranas/golden_unit.git

System (Unix)
```python
$ sudo snap install curl
$ sudo su
$ curl -s https://downloads.perfsonar.net/install | sh -s - tools
$ exit
$ sudo apt-get install iperf3
$ sudo apt install tshark
$ sudo apt-get install wireshark
$ sudo dpkg-reconfigure wireshark-common 
$ sudo usermod -a -G wireshark $USER
$ sudo apt-get install docker(.io)
$ sudo groupadd docker
$ sudo gpasswd -a $USER docker
$ sudo reboot
```

Software
```python
$ cd /{ROOT}/golden_unit/client
$ git clone https://github.com/EricssonResearch/udp-ping.git
$ sudo apt-get install build-essential
$ sudo apt-get install libboost-program-options-dev
$ sudo apt-get install cmake
$ cd /{ROOT}/golden_unit/client/udp-ping
$ g++ -o udpServer udpServer.cpp -lboost_program_options
$ g++ -o udpClient udpClient.cpp -lboost_program_options
```

Python/Anaconda
```python
conda create --name golden_unit python=3.8
conda activate golden_unit 
pip install iperf3 pyshark pandas docker icmplib pyserial paho-mqtt dash dash-bootstrap-components
```

Docker images
```python
cd client/client_opencv
docker build -t client_opencv .
cd client/client_mqtt
docker build -t client_mqtt .
```
### Server-side
Software
```python
$ cd /{ROOT}/golden_unit/server
$ git clone https://github.com/EricssonResearch/udp-ping.git
$ sudo apt-get install build-essential
$ sudo apt-get install libboost-program-options-dev
$ sudo apt-get install cmake
$ cd /{ROOT}/golden_unit/server/udp-ping
$ g++ -o udpServer udpServer.cpp -lboost_program_options
$ g++ -o udpClient udpClient.cpp -lboost_program_options
```

Network
```python
sudo ufw disable
```
Docker images
```python
cd server/server_opencv
docker build -t server_opencv .
```
```python
$ sudo snap install curl
$ sudo su
$ curl -s https://downloads.perfsonar.net/install | sh -s - tools
$ exit
$ sudo apt-get install iperf3
$ sudo apt-get install docker(.io)
$ sudo groupadd docker
$ sudo gpasswd -a $USER docker
$ sudo reboot
```

## Execution
### Server-side
```python
docker run -it --rm -p 8888:8888 server_opencv
docker run -d --rm -p 1883:1883 -p 8883:8883 --name nanomq emqx/nanomq:latest
iperf3 --server
$ cd /{ROOT}/golden_unit/server/udp-ping
$ ./udpServer
+ twampy/owampy activation
```

### Client-side
```python
cd /golden_unit
nano gparams.py (settings)
python main_backend.py 
open new terminal
python main_frontend.py
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

