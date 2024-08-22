#!/usr/local/bin/bash
# FreeBSD bash path
# Increase dummynet pipe buffer limit to accomodate for large BDP
sudo sysctl net.inet.ip.dummynet.pipe_byte_limit=10000000

# Increase bridge node socket buffers for large BDP
sudo sysctl kern.ipc.maxsockbuf=16777216
sudo sysctl net.inet.tcp.sendspace=12582912
sudo sysctl net.inet.tcp.recvspace=12582912

# Create pipe rules
sudo ipfw add 32000 allow ip from any to any
sudo ipfw add 100 allow layer2 not mac-type IP
