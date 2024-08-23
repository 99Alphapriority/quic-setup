#!/usr/local/bin/bash
# FreeBSD bash path

#Route to subnet 1
sudo route add -net 192.168.253.0/24 192.168.252.5

#disable ICMP redirect packets
echo "net.inet.ip.redirect=0" | sudo tee -a /etc/sysctl.conf

#enable IP forwarding
sudo sysctl net.inet.ip.forwarding=1
