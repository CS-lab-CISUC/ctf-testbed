/home/cslab/miniconda3/bin/python launch_vms.py \
  --prefix SHIFT_CTF \
  --env="./.env" \
  --team "Team 1" \
  --config "./launch_vms-config.json" \
  --subnet "10.1.1" \
  --interface_name "Wired connection 1" \
  --network_uuid ea5aca40-b7d2-b896-5efd-dce07151d4ba \
  --commands \
  "echo 'Command started...' | sudo tee /tmp/command_config.log" \
  "sudo nmcli con mod 'Wired connection 1' ipv4.addresses {static_ip}/24 ipv4.method manual" \
  "sudo nmcli con mod 'Wired connection 1' ipv4.gateway {gateway}" \
  "sudo nmcli con mod 'Wired connection 1' +ipv4.routes '10.1.0.0/24 {gateway}'" \
  "sudo nmcli con up 'Wired connection 1'" \
  "sudo nmcli con mod 'Wired connection 1' ipv4.dns '8.8.8.8'" \
  "sudo systemctl restart NetworkManager" \
  "echo 'Network configured successfully' | sudo tee /tmp/network_config.log"
