The initialize_server.sh script initializes the whole server-side system, installing and configuring OpenVPN server and clients. It creates clients throught subnets for each team, each client has a fixed IP. 

Each team VMs are in the same network as the OpenVPN server host, each on a different interface, all configure through the script. 

Network configs, routes, and firewalls are configured accordingly. Traffic shapping also in place to restrict bandwidth.

Check the system architecture and VPN architecture diagram (high level indicators of routes, not extensive) for more info.

server:
sudo bash initialize_server.sh 2>&1 | tee log.txt

client:
sudo openvpn --config team1-1.ovpn 2>&1 | tee log.txt