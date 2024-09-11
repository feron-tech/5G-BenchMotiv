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
pip install iperf3 pyshark pandas docker icmplib pyserial paho-mqtt dash dash-bootstrap-components matplotlib fsspec
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
cd server/server_stream
docker build -t server_stream .
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
docker run -it --rm -e ENV_SERVER_IP=xxxxxxx -e ENV_SERVER_PORT=8888 --network=bridge server_stream
docker run -d --rm -p 1883:1883 -p 8883:8883 --name nanomq emqx/nanomq:latest
iperf3 --server
$ cd /{ROOT}/golden_unit/server/udp-ping
$ ./udpServer
+ twampy/owampy activation

curl -s https://downloads.perfsonar.net/install | sh -s - tools



https://downloads.perfsonar.net/install
https://downloads.perfsonar.net
sudo apt install perfsonar-tools

sudo apt install owamp-server

sudo apt install owamp-client

και το ίδιο για twamp

αφού τρέξεις τον server στον client κάνεις owping

```

### Client-side
```python
cd /golden_unit
nano gparams.py (settings)
{ROOT}/envs/golden_unit/bin/python physical.py
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

## Tools repository
	https://docs.perfsonar.net/manage_regular_tests.html
	https://github.com/perfsonar/owamp
	https://github.com/nokia/twampy
	https://github.com/emirica/twamp-protocol
	https://github.com/perfsonar/toolkit
	https://data.mendeley.com/datasets/8cjkkw79z2/1
	https://github.com/sonata-nfv/tng-sdk-benchmark
	https://github.com/EricssonResearch/udp-ping
	https://github.com/rtlabs-com/p-net
	
## Output
1) Owamp -> owamp.json
* camp_name-> campaign name
* repeat_id-> campaign repetition ID
* exp_id -> campaign's experiment ID
* timestamp-> program timestamp
* seq_nr      sequence number     unsigned long
* tx_time    sendtime            owptimestamp (%020 PRIu64)
* tx_sync       send synchronized   boolean unsigned
* tx_err_perc     send err estimate   float (%g)
* rx_time    recvtime            owptimestamp (%020 PRIu64)
* rx_sync       recv synchronized   boolean unsigned
* rx_err_perc     recv err estimate   float (%g)
* ttl      ttl                 unsigned short
* direction      direction                string: client to/from server (ul/dl)
 
2) TWAMP -> twamp.json
* camp_name-> campaign name
* repeat_id-> campaign repetition ID
* exp_id -> campaign's experiment ID
* timestamp-> program timestamp
* tx_seq_nr     send sequence number           unsigned long
* tx_time    sendtime                       owptimestamp (%020 PRIu64)
* tx_sync       send synchronized              boolean unsigned
* tx_err_perc     send err estimate              float (%g)
* tx_rx_time   send (receive) time            owptimestamp (%020 PRIu64)
* tx_rx_sync      send (receive) synchronized    boolean unsigned
* tx_rx_err_perc    send (receive) err estimate    float (%g)
* tx_ttl     send ttl                       unsigned short
* reflect_seq_nr     reflect sequence number        unsigned long
* reflect_tx_time    reflected (send) time          owptimestamp (%020 PRIu64)
* reflect_tx_sync       reflected (send) synchronized  boolean unsigned
* reflect_tx_err_perc     reflected (send) err estimate  float (%g)
* rx_time    recvtime                       owptimestamp (%020 PRIu64)
* rx_sync       recv synchronized              boolean unsigned
* rx_err_perc     recv err estimate              float (%g)
* reflect_ttl     reflected ttl                  unsigned short