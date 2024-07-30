FROM ubuntu:latest
RUN apt-get -y update && apt-get -y install iperf3
CMD ["/bin/bash", "-c", "iperf3 --server"]

# iperf3 server with docker wont wark, need to manually set