#!/usr/local/bin/bash
# FreeBSD bash path

#Route to subnet 1
sudo route add -net 192.168.253.0/24 192.168.252.5

#disable ICMP redirect packets
echo "net.inet.ip.redirect=0" | sudo tee -a /etc/sysctl.conf

#enable IP forwarding
sudo sysctl net.inet.ip.forwarding=1

#Create pipes
sudo ipfw add 32000 allow ip from any to any
sudo ipfw add 100 allow layer2 not mac-type ip
sudo ipfw add 3000 pipe 1 ip from 192.168.254.0/24 to 192.168.253.0/24 in
sudo ipfw add 3100 pipe 2 ip from 192.168.254.0/24 to 192.168.253.0/24 out
sudo ipfw add 4000 pipe 3 ip from 192.168.253.0/24 to 192.168.254.0/24 in
sudo ipfw add 4100 pipe 4 ip from 192.168.253.0/24 to 192.168.254.0/24 out

sudo ipfw pipe 1 config delay 0
sudo ipfw pipe 2 config delay 0
sudo ipfw pipe 3 config delay 0
sudo ipfw pipe 4 config delay 0
