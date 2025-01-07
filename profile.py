'''
Dumbbell topology to test QUIC and TCP fairness
'''
# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the emulab extensions library. (BridgedLink)
import geni.rspec.emulab as emulab

# Create a portal context, needed to defined parameters
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Describe the parameter(s) this profile script can accept.
# quic_version is used to decide which OS version, chrome-har-capturer version is used.
pc.defineParameter( "quic_version", "Specify the quic version to setup (Q037, RFCv1)", portal.ParameterType.STRING, "RFCv1" )
# project is used to specify the project path to give permissions to apache server.
pc.defineParameter( "project", "Specify the emulab project name", portal.ParameterType.STRING, "FEC-HTTP" )

# Retrieve the values the user specifies during instantiation.
params = pc.bindParameters()

# Check parameter validity.
# Add custom conditions here
valid_versions = ["Q037", "RFCv1"]
if params.quic_version not in valid_versions:
    error = portal.ParameterError("Invalid quic_version. It should be either 'Q037' or 'RFCv1'.", ['quic_version'])
    pc.reportError(error)

# this function will spit out some nice JSON-formatted exception info on stderr
pc.verifyParameters()

'''
SERVER NODES
'''
# Add a raw PC to the request.
ping_server = request.RawPC("ping_server")
# d430 -> 64GB ECC Memory, Two Intel E5-2630v3 8-Core CPUs at 2.4 GHz (Haswell)
ping_server.hardware_type = 'd430'
# https://docs.emulab.net/advanced-topics.html , Public IP Access
# server.routable_control_ip = True
iface1 = ping_server.addInterface()
# Specify the IPv4 address
iface1.addAddress(pg.IPv4Address("192.168.253.11", "255.255.255.0"))


# Add a raw PC to the request.
#cubic_server = request.RawPC("cubic_server")
# d430 -> 64GB ECC Memory, Two Intel E5-2630v3 8-Core CPUs at 2.4 GHz (Haswell)
#cubic_server.hardware_type = 'd430'
# https://docs.emulab.net/advanced-topics.html , Public IP Access
# server.routable_control_ip = True
#iface2 = cubic_server.addInterface()
# Specify the IPv4 address
#iface2.addAddress(pg.IPv4Address("192.168.253.21", "255.255.255.0"))


# Add a raw PC to the request.
bbr_server = request.RawPC("bbr_server")
# d430 -> 64GB ECC Memory, Two Intel E5-2630v3 8-Core CPUs at 2.4 GHz (Haswell)
bbr_server.hardware_type = 'd430'
# https://docs.emulab.net/advanced-topics.html , Public IP Access
# server.routable_control_ip = True
iface3 = bbr_server.addInterface()
# Specify the IPv4 address
iface3.addAddress(pg.IPv4Address("192.168.253.31", "255.255.255.0"))


'''
CLIENT NODES
'''

ping_client = request.RawPC("ping_client")
# d710 -> 12 GB memory, 2.4 GHz quad-core
#quic_client_1.hardware_type = 'd710'
ping_client.hardware_type = 'd430'
# client.routable_control_ip = True
iface4 = ping_client.addInterface()
# Specify the IPv4 address
iface4.addAddress(pg.IPv4Address("192.168.254.11", "255.255.255.0"))


#cubic_client = request.RawPC("cubic_client")
# d710 -> 12 GB memory, 2.4 GHz quad-core
#cubic_client.hardware_type = 'd430'
# client.routable_control_ip = True
#iface5 = cubic_client.addInterface()
# Specify the IPv4 address
#iface5.addAddress(pg.IPv4Address("192.168.254.21", "255.255.255.0"))


bbr_client = request.RawPC("bbr_client")
# d710 -> 12 GB memory, 2.4 GHz quad-core
#tcp_client.hardware_type = 'd710'
bbr_client.hardware_type = 'd430'
# client.routable_control_ip = True
iface6 = bbr_client.addInterface()
# Specify the IPv4 address
iface6.addAddress(pg.IPv4Address("192.168.254.31", "255.255.255.0"))

ubuntu_22 = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
ubuntu_18 = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD"
fbsd_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:FBSD132-64-STD"

# Request that a specific image be installed on this node
ubuntu_image = ubuntu_22 if params.quic_version == 'RFCv1' else ubuntu_18
ping_server.disk_image = ubuntu_image
#cubic_server.disk_image = ubuntu_image
bbr_server.disk_image = ubuntu_image
ping_client.disk_image = ubuntu_image
#cubic_client.disk_image = ubuntu_image
bbr_client.disk_image = ubuntu_image

'''
ROUTERS
'''
# Create 2 bridged links R1 and R2 between the two subnets

#R1
link_bridge_R1 = request.Bridge('link_bridge_R1', 'if1', 'if0')
link_bridge_R1.hardware_type = 'd710'
#link_bridge_R1.hardware_type = 'd430'
link_bridge_R1.disk_image = fbsd_image

#R2
link_bridge_R2 = request.Bridge('link_bridge_R2', 'if1', 'if0')
link_bridge_R2.hardware_type = 'd710'
#link_bridge_R2.hardware_type = 'd430'
link_bridge_R2.disk_image = fbsd_image

iface7 = link_bridge_R1.iface0
iface8 = link_bridge_R1.iface1
iface9 = link_bridge_R2.iface0
iface10 = link_bridge_R2.iface1

iface7.addAddress(pg.IPv4Address("192.168.253.5", "255.255.255.0"))
iface8.addAddress(pg.IPv4Address("192.168.252.5", "255.255.255.0"))
iface9.addAddress(pg.IPv4Address("192.168.252.6", "255.255.255.0"))
iface10.addAddress(pg.IPv4Address("192.168.254.6", "255.255.255.0"))

# R1 Link link_bridge_left
link_bridge_R1_left = request.Link('link_bridge_R1_left')
link_bridge_R1_left.Site('undefined')
link_bridge_R1_left.addInterface(iface7)
link_bridge_R1_left.addInterface(iface1)
#link_bridge_R1_left.addInterface(iface2)
link_bridge_R1_left.addInterface(iface3)

# R1 Link link_bridge_right
link_bridge_R1_right = request.Link('link_bridge_R1_right')
link_bridge_R1_right.Site('undefined')
link_bridge_R1_right.addInterface(iface8)
link_bridge_R1_right.addInterface(iface9)

'''
# R2 Link link_bridge_left
link_bridge_R2_left = request.Link('link_bridge_R2_left')
link_bridge_R2_left.Site('undefined')
link_bridge_R2_left.addInterface(iface9)
#link_bridge_R2_left.addInterface(iface8)
'''

# Link link_bridge_right
link_bridge_R2_right = request.Link('link_bridge_R2_right')
link_bridge_R2_right.Site('undefined')
link_bridge_R2_right.addInterface(iface10)
link_bridge_R2_right.addInterface(iface4)
#link_bridge_R2_right.addInterface(iface5)
link_bridge_R2_right.addInterface(iface6)


# Give bridge some shaping parameters. (Implict parameter found in real link)
# link.bandwidth = 10000
# link.latency   = 36  # Implicit latency in live network link (IMC'17)

# pass variable to script
project = params.project
# Install and execute a script that is contained in the repository.
ping_server.addService(pg.Execute(shell="sh", command="export PROJECT="+ project + " QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/install-deps.sh"))
ping_server.addService(pg.Execute(shell="sh", command="export PROJECT="+ project + " QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/server-nodes-static-route.sh"))
#cubic_server.addService(pg.Execute(shell="sh", command="export PROJECT="+ project + " QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/install-deps.sh"))
#cubic_server.addService(pg.Execute(shell="sh", command="export PROJECT="+ project + " QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/server-nodes-static-route.sh"))
bbr_server.addService(pg.Execute(shell="sh", command="export PROJECT="+ project + " QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/install-deps.sh"))
bbr_server.addService(pg.Execute(shell="sh", command="export PROJECT="+ project + " QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/server-nodes-static-route.sh"))

ping_client.addService(pg.Execute(shell="sh", command="export PROJECT="+ project + " QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/install-deps.sh"))
ping_client.addService(pg.Execute(shell="sh", command="export PROJECT="+ project + " QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/client-nodes-static-route.sh"))
#cubic_client.addService(pg.Execute(shell="sh", command="export PROJECT="+ project + " QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/install-deps.sh"))
#cubic_client.addService(pg.Execute(shell="sh", command="export PROJECT="+ project + " QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/client-nodes-static-route.sh"))
bbr_client.addService(pg.Execute(shell="sh", command="export PROJECT="+ project + " QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/install-deps.sh"))
bbr_client.addService(pg.Execute(shell="sh", command="export PROJECT="+ project + " QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/client-nodes-static-route.sh"))


# Install specific packages
ping_server.addService(pg.Execute(shell="sh", command="/local/repository/scripts/install-apache.sh"))
#cubic_server.addService(pg.Execute(shell="sh", command="/local/repository/scripts/install-apache.sh"))
bbr_server.addService(pg.Execute(shell="sh", command="/local/repository/scripts/install-apache.sh"))
ping_client.addService(pg.Execute(shell="sh", command="export QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/install-client.sh"))
#cubic_client.addService(pg.Execute(shell="sh", command="export QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/install-client.sh"))
bbr_client.addService(pg.Execute(shell="sh", command="export QUIC_VERSION="+ params.quic_version +" && /local/repository/scripts/install-client.sh"))
link_bridge_R1.addService(pg.Execute(shell="sh", command="/local/repository/scripts/bridge-tunning.sh"))
link_bridge_R1.addService(pg.Execute(shell="sh", command="/local/repository/scripts/R1-static-route.sh"))
link_bridge_R2.addService(pg.Execute(shell="sh", command="/local/repository/scripts/bridge-tunning.sh"))
link_bridge_R2.addService(pg.Execute(shell="sh", command="/local/repository/scripts/R2-static-route.sh"))

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
