#!/bin/bash

# ----------------------------------------------
# Configs
# ----------------------------------------------
echo "Intializing Configs"
declare -A VARS
VARS["INITIAL_DIR"]=$(pwd)
VARS["VPN_DIR"]="/etc/openvpn"
VARS["EASY_RSA_DIR"]="${VARS["VPN_DIR"]}/easy-rsa"
VARS["DB_FILE"]="${VARS["VPN_DIR"]}/vpn_users.db"
VARS["CLIENTS_DIR"]="${VARS["VPN_DIR"]}/client"
VARS["CLIENTS_CCD_DIR"]="${VARS["VPN_DIR"]}/ccd"
VARS["VPN_MASK"]="192"
VARS["SERVER_MASK"]="${VARS["VPN_MASK"]}.0.0"
VARS["SERVER_PORT"]="1194"
VARS["SERVER_IP"]="${VARS["SERVER_MASK"]}.0"
VARS["SERVER_TEAM_VIF_IP"]="${VARS["SERVER_MASK"]}.254"
VARS["SERVER_HOST_IP"]="${VARS["SERVER_MASK"]}.1"
# VARS["SERVER_PUBLIC_IP"]="10.3.3.232"
VARS["SERVER_PUBLIC_IP"]="193.136.212.157"
VARS["TEAMS_COUNT"]="${TEAMS_COUNT:-2}"
VARS["TEAMS_USERS_COUNT"]="${TEAMS_USERS_COUNT:-3}"
VARS["SERVER_VPN_NAME"]="ctf_orch"
VARS["SERVER_OUT_INTERFACE"]="enX0"
VARS["SERVER_ADDITIONAL_VIFS"]="2"
VARS["SERVER_SUBNET_INTERFACE_BASE"]="enX"
VARS["SERVER_SUBNET_ORG_INTERFACE"]="enX1"
VARS["SERVER_SUBNET_DEFAULT_INTERFACE"]="enX2"
VARS["SERVER_LOG"]="server-openvpn-status.log"
VARS["CLIENT_LOG"]="client-openvpn-status.log"
VARS["TC_FILE"]="traffic_shaping.sh"
VARS["EVENT_NAME"]="SHIFT_CTF"
VARS["TEAM_VM_PREFIX"]="CTF-TEAM"
VARS["POOL_NAME"]="cslab"
VARS["NETWORK_NAME"]="${VARS["EVENT_NAME"]}-NETWORK"
VARS["TEAMS_VM_WORKERS"]="${TEAMS_VM_WORKERS:-5}"

# Loop through the associative array and create global variables using eval
for key in "${!VARS[@]}"; do
    eval "$key='${VARS[$key]}'"
    echo "$key='${VARS[$key]}'"
done

skippable_values=(3 9 11 16)

# ----------------------------------------------
# CleanUP: Removing any old OpenVPN installation
# ----------------------------------------------
cleanup() {
  echo "Removing any previous installation"
  rm -rf $INITIAL_DIR/tmp
  mkdir -p $INITIAL_DIR/tmp

  sudo systemctl stop openvpn@server

  sudo apt remove --purge -y openvpn easy-rsa
  sudo rm -rf /etc/openvpn /var/log/openvpn
  sudo iptables -F
  sudo iptables -X
  sudo iptables -t nat -F
  sudo iptables -t nat -X
  sudo tc qdisc del dev tun0 root
  sudo tc qdisc del dev tun0 ingress

  # sudo route -n | grep "^$VPN_MASK\."  # TODO: remove installed routes; careful with existing routes.., indeed this removes some routes that are not established afterwards, not sure why
  # sudo route del -net 10.0.0.0 netmask 255.0.0.0 # not sure why this was necessary
  # if we change to 192 this is not a problem
#  for i in "${skippable_values[@]}"; do
#    sudo ip route add 10.$i.0.0/16 dev enX0  # add route for DEI clients
#  done
  /home/cslab/miniconda3/bin/python $INITIAL_DIR/setup_xo.py --tmp="$INITIAL_DIR/tmp" --env="$INITIAL_DIR/.env" --action='cleanup' --prefix=$EVENT_NAME --vm_prefix=$TEAM_VM_PREFIX --params='{"openvpn_vm_name":"'"$SERVER_VPN_NAME"'","num_teams":"'"$TEAMS_COUNT"'","pool_name":"'"$POOL_NAME"'","network_name":"'"$NETWORK_NAME"'","add_vifs":"'"$SERVER_ADDITIONAL_VIFS"'"}' 2>&1 > $INITIAL_DIR/tmp/setup_xo-cleanup.txt
}



# ----------------------------------------------
# Setting up OpenVPN
# ----------------------------------------------
setup_openvpn() {
  # Installing OpenVPN and dependencies
  echo "Installing OpenVPN and dependencies"
  sudo apt update && sudo apt install -y openvpn easy-rsa iptables-persistent sqlite3

  # Creating necessary directories
  echo "Creating OpenVPN directories..."
  sudo mkdir -p $EASY_RSA_DIR $CLIENTS_DIR
  sudo ln -s /usr/share/easy-rsa/* $EASY_RSA_DIR
  sudo chown -R $USER:$USER $EASY_RSA_DIR

  # Initializing Public Key Infrastructure (PKI)
  echo "Initializing PKI..."
  cd $EASY_RSA_DIR
  ./easyrsa init-pki
  echo -e "\n\n" | ./easyrsa build-ca nopass
  ./easyrsa gen-dh
  ./easyrsa gen-crl
  echo "yes" | ./easyrsa build-server-full server nopass

  # Copying required files to OpenVPN directory
  cp pki/ca.crt pki/private/ca.key pki/issued/server.crt pki/private/server.key pki/dh.pem $VPN_DIR/

  # Configuring OpenVPN server
  echo "Configuring OpenVPN Server..."

  # Copy traffic control script
  chmod +x $INITIAL_DIR/$TC_FILE
  sudo cp $INITIAL_DIR/$TC_FILE $VPN_DIR

  local subnet_org_base="$VPN_MASK.0.1"
  local subnet_org="$subnet_org_base.0"
  local subnet_org_w_mask="$subnet_org/24"

  cat > $VPN_DIR/server.conf <<EOF
port $SERVER_PORT
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
topology subnet
dh dh.pem
ifconfig-pool-persist ipp.txt
keepalive 10 120
comp-lzo
persist-key
persist-tun
status $SERVER_LOG
verb 9
explicit-exit-notify 1
client-config-dir $CLIENTS_CCD_DIR
server $SERVER_IP 255.255.255.0
learn-address $TC_FILE
script-security 3
push 'route $subnet_org 255.255.255.0'
EOF
}


# ----------------------------------------------
# Routing, firewall, network
# ----------------------------------------------
load_network_uuid(){
  content=$(cat $INITIAL_DIR/tmp/temp_new_network.txt)
  NETWORK_UUID=$(echo "$content" | jq -r '.network_id')
  echo "Created network uuid: $NETWORK_UUID"
}

setup_routes_firewall_network(){
  # Enabling IP forwarding
  echo "Enabling IP forwarding..."
  echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf > /dev/null
  sudo sysctl -p > /dev/null

  # Configuring firewall rules
  echo "Configuring firewall rules..."
  sudo iptables -P FORWARD DROP  # REJECT by default
  sudo iptables -A INPUT -p udp --dport $SERVER_PORT -j ACCEPT
  sudo iptables -A FORWARD -s $SERVER_IP/24 -j ACCEPT

  /home/cslab/miniconda3/bin/python $INITIAL_DIR/setup_xo.py --tmp="$INITIAL_DIR/tmp" --env="$INITIAL_DIR/.env" --action='setup' --prefix=$EVENT_NAME --vm_prefix=$TEAM_VM_PREFIX --params='{"openvpn_vm_name":"'"$SERVER_VPN_NAME"'","num_teams":'$TEAMS_COUNT',"pool_name":"'"$POOL_NAME"'","network_name":"'"$NETWORK_NAME"'","add_vifs":"'"$SERVER_ADDITIONAL_VIFS"'"}' 2>&1 > $INITIAL_DIR/tmp/setup_xo-setup.txt
  load_network_uuid
  # rm $INITIAL_DIR/tmp/temp_new_network.txt




  # setup org subnet
  local subnet_org_base="$VPN_MASK.0.1"
  local subnet_org="$subnet_org_base.0"
  local subnet_org_w_mask="$subnet_org/24"

  # local subnet_interface=$SERVER_SUBNET_INTERFACE_BASE$(($TEAMS_COUNT+1))
  local subnet_interface=$SERVER_SUBNET_ORG_INTERFACE

  # defining IPs; this assumes a static approach, where the interface name for the teams is > enX0
  sudo ip link set $subnet_interface up
  sudo ip addr add "$subnet_org_base.1/24" dev $subnet_interface
  sudo ip route add $subnet_org_w_mask via $subnet_org_base.1 dev $subnet_interface

  # Set iptables for organization subnet and outbound traffic
  sudo iptables -A FORWARD -s $subnet_org_w_mask -o $SERVER_OUT_INTERFACE -j ACCEPT # FORWWARD exterior
  sudo iptables -A FORWARD -i $SERVER_OUT_INTERFACE -d $subnet_org_w_mask -m state --state ESTABLISHED,RELATED -j ACCEPT  # allow return
  sudo iptables -t nat -A POSTROUTING -s $subnet_org_w_mask -o $SERVER_OUT_INTERFACE -j MASQUERADE


  # setup team NIC and subnet
  # setting up NIC that will be used for all teams VMs; 20250329
  sudo ip link set $SERVER_SUBNET_DEFAULT_INTERFACE up
  sudo ip addr add "$SERVER_TEAM_VIF_IP/8" dev $SERVER_SUBNET_DEFAULT_INTERFACE

}


# ----------------------------------------------
# Create Team User
# ----------------------------------------------
create_user() {
    local subnet_ch_base=$4
    local subnet_ch=$5
    local subnet_ch_w_mask=$6
    local subnet_vpn_client_base=$7
    local username="$1-$2-$3"
    local client_ip="$subnet_vpn_client_base.$j"
    local team_folder="$CLIENTS_DIR/$1-$2"

    local subnet_org_base="$VPN_MASK.0.1"
    local subnet_org="$subnet_org_base.0"
    local subnet_org_w_mask="$subnet_org/24"

    # Create VPN user
    echo "Creating user $username"
    echo "yes" | ./easyrsa build-client-full $username nopass
    mkdir -p $CLIENTS_DIR
    mkdir -p $team_folder

    cat > $team_folder/$username.ovpn <<EOF
client
dev tun
proto udp
remote $SERVER_PUBLIC_IP $SERVER_PORT
resolv-retry infinite
nobind
persist-key
persist-tun
remote-cert-tls server
auth SHA256
cipher AES-256-CBC
comp-lzo
verb 3
<ca>
$(cat $VPN_DIR/ca.crt)
</ca>
<cert>
$(cat $EASY_RSA_DIR/pki/issued/$username.crt)
</cert>
<key>
$(cat $EASY_RSA_DIR/pki/private/$username.key)
</key>
status $CLIENT_LOG
script-security 2
up $username-add_routes.sh
EOF

    # ccd for defining user configs (used on VPN client side)
    mkdir -p $CLIENTS_CCD_DIR
    cat > $CLIENTS_CCD_DIR/$username <<EOF
ifconfig-push $client_ip 255.255.255.0
EOF

    # script that will be executed when VPN client connects, to establish the routes (on the VPN client side)
    cat > $team_folder/$username-add_routes.sh <<EOF
#!/bin/bash
OS=\$(uname -s 2>/dev/null || echo "Windows")

case "\$OS" in
    Linux)
        echo "Detected OS: Linux"
        # ip route add default via $client_ip dev tun0
        ip route add $SERVER_HOST_IP via $client_ip
        ip route add $subnet_ch_w_mask via $client_ip
        ip route add $subnet_org_w_mask via $client_ip
        ;;
    Darwin)
        echo "Detected OS: macOS"
        # sudo route -n add default $client_ip
        /sbin/route -n add $SERVER_HOST_IP $client_ip
        /sbin/route -n add $subnet_ch_w_mask $client_ip
        /sbin/route -n add $subnet_org_w_mask $client_ip
        ;;
    MINGW*|CYGWIN*|MSYS*|Windows)
        echo "Detected OS: Windows"
        # netsh interface ipv4 add route 0.0.0.0/0 $client_ip
        netsh interface ipv4 add route $SERVER_HOST_IP $client_ip
        netsh interface ipv4 add route $subnet_ch_w_mask $client_ip
        netsh interface ipv4 add route $subnet_org_w_mask $client_ip
        ;;
    *)
        echo "Unsupported OS: \$OS"
        exit 1
        ;;
esac
EOF
    chmod +x $team_folder/$username-add_routes.sh

    # Storing user details in the database
#    sqlite3 $DB_FILE "INSERT INTO users (username, config) VALUES ('$username', '$team_folder/$username.ovpn');"
    echo "User $username successfully created!"
}


# ----------------------------------------------
# Create Organization VMS
# ----------------------------------------------
setup_organization_vms(){
    local subnet_org_base="$VPN_MASK.0.1"

: <<EOF
EOF
    echo "Initializing organization VMs (might take a while)"
    echo "$(time /home/cslab/miniconda3/bin/python $INITIAL_DIR/launch_vms.py \
                --base_dir $INITIAL_DIR \
                --prefix $EVENT_NAME \
                --vm_prefix $TEAM_VM_PREFIX \
                --env="$INITIAL_DIR/.env" \
                --team "Organization VM" \
                --config "$INITIAL_DIR/organization_vms-config.json" \
                --subnet "$subnet_org_base" \
                --interface_name "Wired connection 1" \
                --network_uuid $NETWORK_UUID \
                --commands \
                "echo 'Command started...' | sudo tee /tmp/command_config.log" \
                "sudo nmcli con mod 'Wired connection 1' ipv4.addresses {static_ip}/24 ipv4.method manual" \
                "sudo nmcli con mod 'Wired connection 1' ipv4.gateway {gateway}" \
                "sudo nmcli con mod 'Wired connection 1' +ipv4.routes '$VPN_MASK.0.0.0/24 {gateway}'" \
                "sudo nmcli con up 'Wired connection 1'" \
                "sudo nmcli con mod 'Wired connection 1' ipv4.dns '$(resolvectl status $SERVER_OUT_INTERFACE | grep 'Current DNS Server:' | awk '{print $NF}')'"\
                "sudo systemctl restart NetworkManager" \
                "echo 'Network configured successfully'")" |  sudo tee $INITIAL_DIR/tmp/setup_organization_vms_network_config.log


}




# ----------------------------------------------
# Create Team
# ----------------------------------------------
create_team_rules() {
    echo "Creating team rules $2"
    local subnet_vpn_clients_base="$VPN_MASK.$2.0"
    local subnet_vpn_clients="$subnet_vpn_clients_base.0"
    local subnet_vpn_clients_w_mask="$subnet_vpn_clients/24"
    local subnet_ch_base="$VPN_MASK.$2.1"
    local subnet_ch="$subnet_ch_base.0"
    local subnet_ch_w_mask="$subnet_ch/24"
    local j
    cd $EASY_RSA_DIR

    local subnet_org_base="$VPN_MASK.0.1"
    local subnet_org="$subnet_org_base.0"
    local subnet_org_w_mask="$subnet_org/24"

    for ((j = 1; j <= $TEAMS_USERS_COUNT; j++)); do
        create_user "$1" "$2" "$j" "$subnet_ch_base" "$subnet_ch" "$subnet_ch_w_mask" "$subnet_vpn_clients_base"
    done

    echo "Defining routing rules/rejection $2"
    # Update server.conf to route team subnet
    cat <<EOF | sudo tee -a "$VPN_DIR/server.conf" > /dev/null
push 'route $subnet_ch 255.255.255.0'
route $subnet_vpn_clients 255.255.255.0
EOF

    # Block forward to other teams IPs
    for ((y = 1; y <= 255; y++)); do
        if [ "$y" = "$2" ]; then
            continue
        fi
        local o_subnet_vpn_clients_base="$VPN_MASK.$y.0"
        local o_subnet_vpn_clients="$o_subnet_vpn_clients_base.0"
        local o_subnet_vpn_clients_w_mask="$o_subnet_vpn_clients/24"
        local o_subnet_ch_base="$VPN_MASK.$y.1"
        local o_subnet_ch="$o_subnet_ch_base.0"
        local o_subnet_ch_w_mask="$o_subnet_ch/24"

        # NOTE: this is not strictly necessary, as iptables policy is drop; however, this overwrites
        # other range IPs that could be accessible through $SERVER_OUT_INTERFACE
        sudo iptables -I FORWARD 1 -s $subnet_vpn_clients_w_mask -d "$o_subnet_vpn_clients/16" -j REJECT
        # sudo iptables -A FORWARD -s $subnet_vpn_clients_w_mask -d "$o_subnet_ch/16" -j REJECT # /16 covers $VPN_MASK.X.0.0 and $VPN_MASK.X.1.0

        sudo iptables -I FORWARD 1 -s $subnet_ch_w_mask -d "$o_subnet_vpn_clients/16" -j REJECT
        # sudo iptables -A FORWARD -s $subnet_ch_w_mask -d "$o_subnet_ch/16" -j REJECT  # /16 covers $VPN_MASK.X.0.0 and $VPN_MASK.X.1.0
    done

    # Set iptables for VPN clients subnet and outbound traffic
    sudo iptables -A FORWARD -s $subnet_vpn_clients_w_mask -d $subnet_ch_w_mask -j ACCEPT #  FORWARD subnet team VMs
    sudo iptables -A FORWARD -s $subnet_vpn_clients_w_mask -d $subnet_org_w_mask -j ACCEPT #  FORWARD subnet team VMs
    sudo iptables -A FORWARD -s $subnet_vpn_clients_w_mask -o $SERVER_OUT_INTERFACE -j ACCEPT #  FORWARD exterior
    sudo iptables -A FORWARD -i $SERVER_OUT_INTERFACE -d $subnet_vpn_clients_w_mask -m state --state ESTABLISHED,RELATED -j ACCEPT  # allow return
    sudo iptables -t nat -A POSTROUTING -s $subnet_vpn_clients_w_mask -o $SERVER_OUT_INTERFACE -j MASQUERADE

    # Set iptables for team subnet and outbound traffic
    sudo iptables -A FORWARD -s $subnet_ch_w_mask -d $subnet_vpn_clients_w_mask -j ACCEPT # FORWARD subnet team VPN clients
    sudo iptables -A FORWARD -s $subnet_org_w_mask -d $subnet_vpn_clients_w_mask -j ACCEPT # FORWARD subnet team VPN clients
    sudo iptables -A FORWARD -s $subnet_ch_w_mask -o $SERVER_OUT_INTERFACE -j ACCEPT # FORWWARD exterior
    sudo iptables -A FORWARD -i $SERVER_OUT_INTERFACE -d $subnet_ch_w_mask -m state --state ESTABLISHED,RELATED -j ACCEPT  # allow return
    sudo iptables -t nat -A POSTROUTING -s $subnet_ch_w_mask -o $SERVER_OUT_INTERFACE -j MASQUERADE

    # setting VIF for the various teams; 20250329
    sudo ip route add $subnet_ch_w_mask via $SERVER_TEAM_VIF_IP dev $SERVER_SUBNET_DEFAULT_INTERFACE

    # defining IPs; this assumes a static approach, where the interface name for the teams is > enX0
    # sudo ip link set $SERVER_SUBNET_INTERFACE_BASE$2 up
    # sudo ip addr add "$subnet_ch_base.1/24" dev $SERVER_SUBNET_INTERFACE_BASE$2
    # sudo ip route add $subnet_ch_w_mask via $subnet_ch_base.1 dev $SERVER_SUBNET_INTERFACE_BASE$2
}

create_team_vms(){
    local subnet_ch_base="$VPN_MASK.$2.1"
: <<EOF
EOF
    echo "Initializing team $2 VMs (might take a while)"
    echo "$(time /home/cslab/miniconda3/bin/python $INITIAL_DIR/launch_vms.py \
                --base_dir $INITIAL_DIR \
                --prefix $EVENT_NAME \
                --vm_prefix $TEAM_VM_PREFIX \
                --env="$INITIAL_DIR/.env" \
                --team "$2" \
                --config "$INITIAL_DIR/challenges_vms-config.json" \
                --subnet "$subnet_ch_base" \
                --interface_name "Wired connection 1" \
                --network_uuid $NETWORK_UUID \
                --gateway "$SERVER_TEAM_VIF_IP" \
                --commands \
                "echo 'Command started...' | sudo tee /tmp/command_config.log" \
                "sudo nmcli con mod 'Wired connection 1' ipv4.addresses {static_ip}/24 ipv4.method manual" \
                "sudo nmcli con mod 'Wired connection 1' +ipv4.routes '$SERVER_TEAM_VIF_IP/32'" \
                "sudo nmcli con mod 'Wired connection 1' ipv4.gateway {gateway}" \
                "sudo nmcli con mod 'Wired connection 1' +ipv4.routes '$VPN_MASK.$2.0.0/24 {gateway}'" \
                "sudo nmcli con up 'Wired connection 1'" \
                "sudo nmcli con mod 'Wired connection 1' ipv4.dns '$(resolvectl status $SERVER_OUT_INTERFACE | grep 'Current DNS Server:' | awk '{print $NF}')'"\
                "sudo systemctl restart NetworkManager" \
                "echo 'Network configured successfully'")" | sudo tee $INITIAL_DIR/tmp/setup_team_$2_vms_network_config.log

                # f"ip addr add {STATIC_IP}/24 dev eth0",
                # f"ip route add {GATEWAY} dev eth0",
                # "ip route add $VPN_MASK.1.0.0/24 via $VPN_MASK.1.1.1 dev eth0",
}

setup_new_team(){
  load_network_uuid

  # TODO: this function is to be used to create additional teams
  # note that this needs to identify the previous max team, and increment on it
  # works with flag -f setup_new_team
  echo $TEAM_VM_PREFIX
  new_team=$(/home/cslab/miniconda3/bin/python $INITIAL_DIR/setup_xo.py --tmp="$INITIAL_DIR/tmp" --env="$INITIAL_DIR/.env" --action='check' --prefix=$EVENT_NAME --vm_prefix=$TEAM_VM_PREFIX)

  echo "Existing teams $new_team"
  ((new_team++))
  echo "Creating new team $new_team"
  create_team_rules "team" "$new_team" "0"
  create_team_vms "team" "$new_team"
}

setup_team_rules(){
  # Creating a database for VPN users
  # echo "Creating user database..."
  # sqlite3 $DB_FILE "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, config TEXT);"

  # Creating team vms
  echo "Creating teams rules"
  for ((i = 1; i <= TEAMS_COUNT; i++)); do
    skip=false
    for value in "${skippable_values[@]}"; do
        if [ "$i" -eq "$value" ]; then
            skip=true
            break
        fi
    done

    if [ "$skip" = false ]; then
        create_team_rules "team" "$i" "0"
    fi
  done
}

setup_team_vms() {
  echo "Creating team VMs with controlled parallelism..."

  local max_workers="${VARS["TEAMS_VM_WORKERS"]:-5}"
  local running_jobs=0
  declare -a pids=()

  for ((i = 1; i <= TEAMS_COUNT; i++)); do
    skip=false
    for value in "${skippable_values[@]}"; do
        if [ "$i" -eq "$value" ]; then
            skip=true
            break
        fi
    done

    if [ "$skip" = false ]; then
      (
        echo "[Team $i] Starting..."
        create_team_vms "team" "$i"
        echo "[Team $i] Finished!"
      ) &

      pids+=($!)
      ((running_jobs++))

      if (( running_jobs >= max_workers )); then
        wait -n 
        ((running_jobs--))
      fi
    fi
  done

  # Wait for all remaining jobs
  for pid in "${pids[@]}"; do
    wait "$pid"
  done

  echo "All teams created!"
}




# ----------------------------------------------
# Enable & start OpenVPN server
# ----------------------------------------------
start_openvpn(){
  # Starting and enabling OpenVPN service
  echo "Starting OpenVPN service"
  sudo systemctl enable openvpn@server
  sudo systemctl restart openvpn@server
}

flag_used=false
while getopts ":f:" opt; do
  flag_used=true
  case $opt in
    f)
      function_name="$OPTARG"
      if declare -f "$function_name" > /dev/null; then
        echo "calling $function_name"
        "$function_name"
      else
        echo "Error: Function '$function_name' not found."
      fi
      ;;
    *) echo "Usage: $0 [-f function (cleanup setup_openvpn setup_routes_firewall_network setup_team_rules setup_team_vms start)]" ;;
  esac
done

if [ "$flag_used" = false ]; then
  cleanup
  setup_openvpn
  setup_routes_firewall_network
  setup_team_rules
  start_openvpn
  setup_organization_vms
  setup_team_vms
fi

echo "Script finished"
