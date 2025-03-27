
# Capture the Flag shiftappens25

Descrição do proj...
https://cs-lab.cisuc.uc.pt/shiftappens25/


## Arquitetura

bla bla


## Requirements

### Templates

The Vms have to be ready to be deployed in Xen Orchestra and coverted as a template. Xen Orchestra only supports Ova files. Therefore in case you used a Virtualization Software like VMWare you will need to use OVF Tool.

The Vm also needs to have Xen Guest Utilities installed since this raised alot of issues here is a quick universal install for all distributions

#### Prerequesites
```bash
sudo apt update
sudo apt install -y git golang make
sudo apt install network-manager
```

#### Clone xe-guest-utilities
```bash
cd ~
git clone https://github.com/xenserver/xe-guest-utilities.git
cd xe-guest-utilities
export GO111MODULE=on
go mod tidy
go mod vendor
go mod download

make
```

#### Move Binaries to Sys Path

```bash
sudo mv build/obj/xe-daemon /usr/local/bin/
sudo mv build/obj/xenstore /usr/local/bin/
```

#### Check if it´s working

```bash
xe-daemon --version
```

####  Create a systemd Service

```bash
sudo nano /etc/systemd/system/xe-daemon.service
```

And paste this:
```txt
[Unit]
Description=XE Guest Utilities Daemon
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/xe-daemon -d
Restart=always

[Install]
WantedBy=multi-user.target
```


####  Execution

```bash
sudo systemctl daemon-reload
sudo systemctl enable xe-daemon
sudo systemctl start xe-daemon
```

####  Verification

```bash
systemctl status xe-daemon
```


⚠️ Recomendations ⚠️

Altought the script allows specific commands to be executed for each VM. It´s recommended for the user to make use of crontab and configure it with the commands the Challenge VM needs on boot.

It´s also recommended the use of Headless Mode.



## Documentation

## Json Documentation

The Json files in CTF-D are responsible for that configuration of challenges, team and users.

### Challenge Example
```json
"Challenge X": {
        "name": "",                  # Name of the Challenge and Vm
        "category": "",              # Dunno
        "description": "",           # Description of Challenge and VM
        "value":"",                  # Dunno
        "state": "",                 # Dunno
        "type": "",                  # Dunno
        "max_attempts": "",          # Dunno
        "hint": "",                  # Dunno
        "hint_cost": "",             # Dunno
        "flag": "",                  # Dunno
        "flag_type": "",             # Dunno
        "file_path": "",             # Dunno
        "template_uuid": "",         # Template UUID of VM in Xen Orchestra
        "network_uuid": "",          # Network UUID of Subnet to be configured withVPN
        "user":"",                   # User credential of VM to ssh into
        "password":"",               # Password credential of VM to ssh into
        "commands": [],              # Optional Commands to be executed on VM start
        "ImAModule":false            # Explanation Bellow
    }
```

#### ImAModule Explanation
If we have 3 challenges that dont need a unique VM, we configure the 3 challenges to use the same template_uuid. For the first challenge the ImAModule should be false, the other 2 challenges should have this atribute as true. This makes it so the Challengs are associated with only one VM ip.

Example:

```json
    "Challenge 7": {
        "name": "CH2-Hard-Challenge Vieira-(Module1)",
        "category": "",
        "description": "Vieira Module 1",
        "value": 500,
        "state": "visible",
        "type": "standard",
        "max_attempts": 0,
        "hint": "Test VM",
        "hint_cost": 250,
        "flag": "Test_Flag",
        "flag_type": "static",
        "file_path": null,
        "template_uuid": "60e77e42-a119-1a81-3980-066c0db51105",
        "network_uuid": "ea5aca40-b7d2-b896-5efd-dce07151d4ba",
        "user":"",
        "password":"",
        "commands": [],
        "ImAModule":false
    },
    "Challenge 8": {
        "name": "CH3-Hard-Challenge Vieira-(Module2)",
        "category": "",
        "description": "Vieira Module 2",
        "value": 500,
        "state": "visible",
        "type": "standard",
        "max_attempts": 0,
        "hint": "Test VM",
        "hint_cost": 250,
        "flag": "Test_Flag",
        "flag_type": "static",
        "file_path": null,
        "template_uuid": "60e77e42-a119-1a81-3980-066c0db51105",
        "network_uuid": "ea5aca40-b7d2-b896-5efd-dce07151d4ba",
        "user":"",
        "password":"",
        "commands": [],
        "ImAModule":true
    }
  ```

  Output of Script:

  ```bash
  Resposta do servidor Flask: {
    "Team 1": {
      "[\"CH1-NotWorkingTestPurposes\"]": "10.1.1.2",
      "[\"CH2-Hard-Challenge Vieira-(Module1)\", \"CH3-Hard-Challenge Vieira-(Module2)\"]": "10.1.1.3"
    },
    "Team 2": {
      "[\"CH1-NotWorkingTestPurposes\"]": "10.2.1.2",
      "[\"CH2-Hard-Challenge Vieira-(Module1)\", \"CH3-Hard-Challenge Vieira-(Module2)\"]": "10.2.1.3"
    }
  }
```

### User Example

```json
"User_X": {
        "name": "",
        "email": "",
        "password": "",
        "type": "",
        "verified": True,
        "hidden": False,
        "banned": False,
        "fields": [],
        "country": "",
        "team": "Team_X"
    }
```

### Team Example
```json
 "Team_2": {
        "name": "Team 2",
        "password": "joaquimsilvateam",
    }
```

## WebServer Documentation

#### Init the script that initilizaes the VMs

```http
  POST /create-vms
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `payload` | `json` | **Obrigatório**. O json relativo a configuração dos challenges e nº de equipas |

#### Return Config Files

```http
  GET /download
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `X`      | `X` | X |



## Environment variables

The script makes use of Environment variables in order to not expose sensative information

### CTF-D
In CTF-D for the Script to run this environment variables have to be defined:
```bash
cd ctf-testbed/CTF-D
nano .env

CTFD_URL=             #CTF-D Website
CTFD_TOKEN=           #Admin Token generated in CTF-D Website (Config -> Acess Token)
```

### Server-Side

```bash
cd ctf-testbed/CTF-D
nano .env

XO_WS_URL = ""                # Xen Orchestra URL
USERNAME = ""                 # Xen Orchestra admin user
PASSWORD = ""                 # Xen Orchestra admin password
DEFAULT_VM_DESCRIPTION = ""   # Default VM Description for Xen Orchestra
OUTPUT_FILE = ""              # Output file
COM = ""                      # Xen Orchestra password (?)

```
## Execution

### Venv Activation and Web Server

First you will need to activate the Web Server. For that we have to run the Web Server with sudo to acess the /etc/ folder. It´s recommended to actiavate a venv for sudo execution as showed:

```bash
  cd server-side
  python3 -m venv venv
  source venv/bin/activate
  pip install flask python-dotenv
  sudo -E venv/bin/python server.py
```

You should see something like this:
```bash
(venv) (base) cslab@ctforch:~/ctf-testbed/server-side$ sudo -E venv/bin/python server.py
 * Serving Flask app 'server'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 667-150-742
 ```

The use of a tmux terminal is option, in case you want to here is how to intilizate it:
```bash
tmux new-session -A -s WebServer
```

To detach the process and keep it running do ctrl+b and ctr+d


### Main Script

To execute the main script

```bash
cd CTF-D
python3 script.py
```

This script will populate the CTF-D with challenges/users and teams so make sure there are no existing challenges/teams and users in order to not raise a conflit.

The script will end when the script from server-side returns the IPs of the VMs that were created for each team.

### Getting Configuration Files

In order to get files with the teams ips and VPN configs the user should make a GET request to the WebServer

```bash
curl -O -J http://{WEBSERVERIP}:{WEBSERVERPORT}/download
unzip ctf_vm_package.zip
```

