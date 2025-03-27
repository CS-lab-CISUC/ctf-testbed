[sudo] password for cslab: Intializing Configs
EVENT_NAME='SHIFT_CTF'
CLIENTS_DIR='/etc/openvpn/client'
TC_FILE='traffic_shaping.sh'
SERVER_PUBLIC_IP='10.3.3.232'
EASY_RSA_DIR='/etc/openvpn/easy-rsa'
INITIAL_DIR='/home/cslab/ctf-testbed/server-side'
TEAM_VM_PREFIX='CTF-TEAM'
SERVER_LOG='server-openvpn-status.log'
SERVER_HOST_IP='10.0.0.1'
CLIENTS_CCD_DIR='/etc/openvpn/ccd'
SERVER_IP='10.0.0.0'
NETWORK_NAME='SHIFT_CTF-NETWORK'
SERVER_SUBNET_INTERFACE_BASE='enX'
SERVER_VPN_NAME='ctf_orch'
CLIENT_LOG='client-openvpn-status.log'
SERVER_MASK='10.0.0'
POOL_NAME='cslab'
VPN_DIR='/etc/openvpn'
SERVER_OUT_INTERFACE='enX0'
DB_FILE='/etc/openvpn/vpn_users.db'
TEAMS_USERS_COUNT='5'
TEAMS_COUNT='3'
CLIENT_MASK='10'
Removing any previous installation

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

Reading package lists...
Building dependency tree...
Reading state information...
The following packages were automatically installed and are no longer required:
  libccid libeac3 libpcsclite1 libpkcs11-helper1t64 opensc opensc-pkcs11 pcscd
Use 'sudo apt autoremove' to remove them.
The following packages will be REMOVED:
  easy-rsa* openvpn*
0 upgraded, 0 newly installed, 2 to remove and 131 not upgraded.
After this operation, 2,054 kB disk space will be freed.
(Reading database ... 157605 files and directories currently installed.)
Removing easy-rsa (3.1.7-2) ...
Removing openvpn (2.6.12-0ubuntu0.24.04.1) ...
Processing triggers for man-db (2.12.0-4build2) ...
(Reading database ... 157501 files and directories currently installed.)
Purging configuration files for openvpn (2.6.12-0ubuntu0.24.04.1) ...
dpkg: warning: while removing openvpn, directory '/etc/openvpn/client' not empty so not removed
Cannot find device "tun0"
Cannot find device "tun0"
10.1.1.0        0.0.0.0         255.255.255.0   U     0      0        0 enX1
10.2.1.0        0.0.0.0         255.255.255.0   U     0      0        0 enX2
10.3.0.0        0.0.0.0         255.255.0.0     U     100    0        0 enX0
10.3.0.254      0.0.0.0         255.255.255.255 UH    100    0        0 enX0
SIOCDELRT: No such process
Installing OpenVPN and dependencies

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

Hit:1 http://pt.archive.ubuntu.com/ubuntu noble InRelease
Hit:2 http://pt.archive.ubuntu.com/ubuntu noble-updates InRelease
Hit:3 http://pt.archive.ubuntu.com/ubuntu noble-backports InRelease
Hit:4 http://security.ubuntu.com/ubuntu noble-security InRelease
Reading package lists...
Building dependency tree...
Reading state information...
131 packages can be upgraded. Run 'apt list --upgradable' to see them.

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

Reading package lists...
Building dependency tree...
Reading state information...
iptables-persistent is already the newest version (1.0.20).
sqlite3 is already the newest version (3.45.1-1ubuntu2.1).
Suggested packages:
  openvpn-dco-dkms openvpn-systemd-resolved
The following NEW packages will be installed:
  easy-rsa openvpn
0 upgraded, 2 newly installed, 0 to remove and 131 not upgraded.
Preconfiguring packages ...
Need to get 0 B/746 kB of archives.
After this operation, 2,054 kB of additional disk space will be used.
Selecting previously unselected package openvpn.
(Reading database ... 157493 files and directories currently installed.)
Preparing to unpack .../openvpn_2.6.12-0ubuntu0.24.04.1_amd64.deb ...
Unpacking openvpn (2.6.12-0ubuntu0.24.04.1) ...
Selecting previously unselected package easy-rsa.
Preparing to unpack .../easy-rsa_3.1.7-2_all.deb ...
Unpacking easy-rsa (3.1.7-2) ...
Setting up openvpn (2.6.12-0ubuntu0.24.04.1) ...
Created symlink /etc/systemd/system/multi-user.target.wants/openvpn.service → /usr/lib/systemd/system/openvpn.service.
Setting up easy-rsa (3.1.7-2) ...
Processing triggers for man-db (2.12.0-4build2) ...

Running kernel seems to be up-to-date.

No services need to be restarted.

No containers need to be restarted.

No user sessions are running outdated binaries.

No VM guests are running outdated hypervisor (qemu) binaries on this host.
Creating OpenVPN directories...
Initializing PKI...

Notice
------
'init-pki' complete; you may now create a CA or requests.

Your newly created PKI dir is:
* /etc/openvpn/easy-rsa/pki

Using Easy-RSA configuration:
* undefined

No Easy-RSA 'vars' configuration file exists!

Using SSL:
* openssl OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
.+...+...+.......+.....................+......+.........+..+...+.+......+..+..........+.....+.......+......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+......+..+....+........+.+............+..+.+......+........+......+.+.....+..........+...........+.......+......+..+...+.......+.....+....+...+.....+..........+......+..+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*......+.....+...+............+......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
.+....+......+..+............+...+......+.+.....+...............+.+..+...+...+.+...+........+...+....+........+.........+...+.+..+...+....+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*....+.........+...+...+.....+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*......+.....+......+..........+...+......+.........+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Common Name (eg: your user, host, or server name) [Easy-RSA CA]:
Notice
------
CA creation complete. Your new CA certificate is at:
* /etc/openvpn/easy-rsa/pki/ca.crt

No Easy-RSA 'vars' configuration file exists!

Using SSL:
* openssl OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
Generating DH parameters, 2048 bit long safe prime
.........................................................................................................................................................................................................................................................................................................+..................+........+..+................................................................................................................................................................................................................................+.............+........................+....................+.....................................................................................................................................................+..............................................+........+...........................................................+..+..................................................................................+.................+.............................................................................................................................+.................................................................................................................................................................................................................................................................................................................................................+........+.....................................+......................................................................................................................................................................................................................................................................................................+................................................................................................................................................................................................................................................................................................................................................+........................................................................................................................................+..............................................................................................................................................................................................................................................+................................................................................................................................................................+...................+.....................................................................................................................................+...................+..............+............+...................................+...............................................................................................................................................................................................................................+........................................................................+.......................................+.....................................................................................................................................................................................................................................................................................................................................................................................................................................................................................+................................................................................................................................+....+.............................................+.......................................................................................................+.................................+...........................................................................+.........................................................................................+....................................................................................................................................................................................................................................................................................+..........................+.............................................................................................+.......................................................................................................................................................+.............................................................................................................................................................................+.........................................+....+...................................................................................................................................................................................................................+.......................................................................................................................................................................................+..............................................................................................+.......................................................+............................................................................................................................+..................................................................+.+............+.........................................................................+...................................................................................................................................+.....................................................+........................................................................................................+.....................................+.................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................+.................................................................................................................................................................................................................+..........+....................................................+...........................................................................................................................+...............................................+.............................................................................................................................................................................+.....................................................................+........................................................................................................................................................................................................................................................................+...........................................................+.................................+....................................................................................................................................+............................+............................................+..+..............................................................++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*++*
DH parameters appear to be ok.

Notice
------

DH parameters of size 2048 created at:
* /etc/openvpn/easy-rsa/pki/dh.pem

No Easy-RSA 'vars' configuration file exists!

Using SSL:
* openssl OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
Using configuration from /etc/openvpn/easy-rsa/pki/openssl-easyrsa.cnf

Notice
------
An updated CRL has been created:
* /etc/openvpn/easy-rsa/pki/crl.pem

No Easy-RSA 'vars' configuration file exists!

Using SSL:
* openssl OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
......+.....+...+.......+..+.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*....+..+.+..+..........+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.......+....+.........+..+...+.........................+........+.........+...+.+.....+................+...+..+.........+.+......+...+......+...+..+........................+.......+..+...+.......+..+.............+.....+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
.+.....+.+.....+....+......+..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*....+.....+...+......+.+...+...+...+..............+...+............+.+..+....+......+..+.+..+...+.+......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*................+....+.....+.+...........+....+....................+................+...+...........+......+.+.....+............+.+............+..+.+..+...+.+.....+..........+......+..+..........+...+..+................+..+...+.......+..+.......+........+...+............+.............+.........+...........+...+....+........+..........+...+..+...+....+..+.+..............+..................+.+.....+.+...+..+.........+.......+..+.......+...+...........+.....................+.+..+...+...............+...+.+......+..+.+..+.......+......+.....................+...+.................+.+............+...+.........+.........+.........+........+....+...+.....+.+......+.........+..+...+.+.....+......+....+.........+...........+...+...+.........+....+......+...+...+............+.....+.+...........+.+...............+............+...........+......+...............+...+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----

Notice
------
Private-Key and Public-Certificate-Request files created.
Your files are:
* req: /etc/openvpn/easy-rsa/pki/reqs/server.req
* key: /etc/openvpn/easy-rsa/pki/private/server.key

You are about to sign the following certificate:
Request subject, to be signed as a server certificate
for '825' days:

subject=
    commonName                = server

Type the word 'yes' to continue, or any other input to abort.
  Confirm request details:
Using configuration from /etc/openvpn/easy-rsa/pki/openssl-easyrsa.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'server'
Certificate is to be certified until Jun 29 02:04:31 2027 GMT (825 days)

Write out database with 1 new entries
Database updated

Notice
------
Certificate created at:
* /etc/openvpn/easy-rsa/pki/issued/server.crt

Notice
------
Inline file created:
* /etc/openvpn/easy-rsa/pki/inline/server.inline

Configuring OpenVPN Server...
Enabling IP forwarding...
Configuring firewall rules...
Created network uuid: a8a3bf62-b244-459f-d0a5-25fea902d34a
Creating teams rules
Creating team rules 1
Creating user team-1-1
No Easy-RSA 'vars' configuration file exists!

Using SSL:
* openssl OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
...+.+...............+...+.....+....+..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.........+......+.....+.......+..+.......+.....+.+..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.......+..+.........+...............+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
.+................+...+..+.......+...........+.+.....+......+...+....+...+............+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*...+..+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+..+.......+.....+...+....+...+...........+....+..+...+.+.....+.......+..+.+.........+.....+......+......+.+...+..+..........+..+.......+........+......+.+...+......+..+...+.+.....................+..+...+...+.+...+..+.+..+................+.........+..+.+...+...............+.........+.....+.............+...+......+....................+...+..........+..+.............+..+.+............+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----

Notice
------
Private-Key and Public-Certificate-Request files created.
Your files are:
* req: /etc/openvpn/easy-rsa/pki/reqs/team-1-1.req
* key: /etc/openvpn/easy-rsa/pki/private/team-1-1.key

You are about to sign the following certificate:
Request subject, to be signed as a client certificate
for '825' days:

subject=
    commonName                = team-1-1

Type the word 'yes' to continue, or any other input to abort.
  Confirm request details:
Using configuration from /etc/openvpn/easy-rsa/pki/openssl-easyrsa.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'team-1-1'
Certificate is to be certified until Jun 29 02:04:34 2027 GMT (825 days)

Write out database with 1 new entries
Database updated

Notice
------
Certificate created at:
* /etc/openvpn/easy-rsa/pki/issued/team-1-1.crt

Notice
------
Inline file created:
* /etc/openvpn/easy-rsa/pki/inline/team-1-1.inline

User team-1-1 successfully created!
Creating user team-1-2
No Easy-RSA 'vars' configuration file exists!

Using SSL:
* openssl OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*........+...+.........+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.........+..+.......+....................+...+...+...............+.........+......+...+....+..+.+...+...........+....+..+.............+....................+......+......+...+....+...............+..+.+........+.......+...+..+.............+..+...+.+...........+.......+..+...+.+............+.........+........+.......+.........+.........+..+......+.........+....+......+...+...+...+..+.......................................+.........+.+.....+.+...............+...+...........+................+...+......+........+.+......+.....+..........+...+........+...+.+...+...........+......+...+...+....+...+.....+..........+.....+.+..+.........+.+...+...........+...+...+.......+.....+..........+...+.....+.............+......+...........+.......+......+..+...+......+.+...+......+...........+......................+........+...+.......+.....+.......+.....+.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
..+.+...+.....+...............+...+...+............+.......+..+.........+......+.+..+..........+..+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.........+.......+........+.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+.........+......+...+.....+.+..+.......+......+............+..+..........+...........+..........+..+.........+....+......+...+...........+............+...+.+...+..+..........+.....+.+..+.......+...+...+..+.......+.........+..+..........+.....+.........+....+.........+...+..+............+.+..+.+......+...............+...+........+.......+..+....+..+...+....+.....+...+.........+..........+..............+.......+........+......+.+...+..+.......+.....+...+...+.......+............+..+....+......+.........+..+....+......+.........+...+......+..............+.+.....+.+...+..+..........+.........+.....+....+........+.........................+..+...+..........+...+.....+.+......+.....+.........+...+...+.......+..+.+............+........+.........+...+......+.......+.....+.......+.....+.+......+.....+...+.+..+...+.........................+..+.......+...+..+.......+...+.....+......+.+......+.........+...+.....+.+...............+.....+......+.+............+..+.........+..........+..+....+...+..+....+.....+.+...+........+.......+..+....+.....+.......+........+....+............+..................+...+.....+....+........+...+.......+...+..+.+.....+.+.....+...+......+.........+.......+...............+......+........+......+....+...........+....+......+...+.....+.+.....+......+...+...............+.......+...............+...+..+......+..........+.....+.......+..................+..+.+..+.......+...+...............+..+...+..........+..............+.........+......+...................+.....+....+......+..+...+....+..+.+..............+.+..+......+.......+.....+.........+....+.....+....+.......................+...+....+......+..............+......+......+......+..........+.....+...+.+...+...........+.........+.+.........+.....+...+..........+..+.......+....................+.+.........+.....+.+..+..........+.................+....+..+.........+...+.+......+...+......+...........+...+......+.+.....+.+...+......+...+..+.........+.+......+.................+...+.........+..........+...+......+............+........+.+......+....................+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----

Notice
------
Private-Key and Public-Certificate-Request files created.
Your files are:
* req: /etc/openvpn/easy-rsa/pki/reqs/team-1-2.req
* key: /etc/openvpn/easy-rsa/pki/private/team-1-2.key

You are about to sign the following certificate:
Request subject, to be signed as a client certificate
for '825' days:

subject=
    commonName                = team-1-2

Type the word 'yes' to continue, or any other input to abort.
  Confirm request details:
Using configuration from /etc/openvpn/easy-rsa/pki/openssl-easyrsa.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'team-1-2'
Certificate is to be certified until Jun 29 02:04:35 2027 GMT (825 days)

Write out database with 1 new entries
Database updated

Notice
------
Certificate created at:
* /etc/openvpn/easy-rsa/pki/issued/team-1-2.crt

Notice
------
Inline file created:
* /etc/openvpn/easy-rsa/pki/inline/team-1-2.inline

User team-1-2 successfully created!
Creating user team-1-3
No Easy-RSA 'vars' configuration file exists!

Using SSL:
* openssl OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
..+.........+...+.........+.+..................+......+.....+...+......+.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.....+...+......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*......................+...+............+...+..+.+......+........+.+............+.....+....+...+...+.....+...+....+.....+............+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
....+.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*..+.....+.......+..+.......+.....+.........+.+........+.+......+......+..+.......+.....+...+.+..+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*......+...+...+..+...+...+......+...+.......+.....+...+.+..+....+...+...+.....+...+.......+........+....+......+......+...+..+......+...+.+...+.....+...+.......+..+.+..+......+.......+...+..+...+.+......+..+.............+............+..+...+...+.............+..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----

Notice
------
Private-Key and Public-Certificate-Request files created.
Your files are:
* req: /etc/openvpn/easy-rsa/pki/reqs/team-1-3.req
* key: /etc/openvpn/easy-rsa/pki/private/team-1-3.key

You are about to sign the following certificate:
Request subject, to be signed as a client certificate
for '825' days:

subject=
    commonName                = team-1-3

Type the word 'yes' to continue, or any other input to abort.
  Confirm request details:
Using configuration from /etc/openvpn/easy-rsa/pki/openssl-easyrsa.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'team-1-3'
Certificate is to be certified until Jun 29 02:04:36 2027 GMT (825 days)

Write out database with 1 new entries
Database updated

Notice
------
Certificate created at:
* /etc/openvpn/easy-rsa/pki/issued/team-1-3.crt

Notice
------
Inline file created:
* /etc/openvpn/easy-rsa/pki/inline/team-1-3.inline

User team-1-3 successfully created!
Creating user team-1-4
No Easy-RSA 'vars' configuration file exists!

Using SSL:
* openssl OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
.....+.........+.....+.+..+....+.....+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.....+.........+.+..+...+.......+......+.....+.+...+......+.....+.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*..+.+...+.....+.+......+...+..+...+.+..............+...................+.....+.+......+.........+............+...+..+.......+............+.....+.+..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*...........+......+...+...+..+...+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*......+.............+......+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----

Notice
------
Private-Key and Public-Certificate-Request files created.
Your files are:
* req: /etc/openvpn/easy-rsa/pki/reqs/team-1-4.req
* key: /etc/openvpn/easy-rsa/pki/private/team-1-4.key

You are about to sign the following certificate:
Request subject, to be signed as a client certificate
for '825' days:

subject=
    commonName                = team-1-4

Type the word 'yes' to continue, or any other input to abort.
  Confirm request details:
Using configuration from /etc/openvpn/easy-rsa/pki/openssl-easyrsa.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'team-1-4'
Certificate is to be certified until Jun 29 02:04:36 2027 GMT (825 days)

Write out database with 1 new entries
Database updated

Notice
------
Certificate created at:
* /etc/openvpn/easy-rsa/pki/issued/team-1-4.crt

Notice
------
Inline file created:
* /etc/openvpn/easy-rsa/pki/inline/team-1-4.inline

User team-1-4 successfully created!
Creating user team-1-5
No Easy-RSA 'vars' configuration file exists!

Using SSL:
* openssl OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
...............+..+.+..+...+....+...+......+..+.......+...+..+......+.......+........+.+........+......+......+.........+.......+.....+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+..+....+.....+.........+.+..+...+......+.+.........+.........+..+...+....+..+...+..........+..+....+..+.......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*..+..........+..+......+......+.+.........+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
.......+.+.....+....+......+...+.........+.....+.+..............+...+...+....+........+....+......+...+......+.....+.+...+......+.....+...............+......+...+......+...+.+.........+......+.....+............+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.....+....+...............+......+..+..........+........+.+...+...........+.......+...+......+......+..+...+...+......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.........+..+......+.......+...+.........+...+......+......+......+.........+.........+..............+...+..........+..+............+.+.....+...+...................+..+...+.+......+..............+....+..+...+............+...+......+.......+..+...+...............+...+..........+.................+...+.......+...+......+...+..+....+.....+......+.+...+..+....+.....+.+.....+...+.+...+..+.........+.......+...+..+.......+...........+....+........+............+......+......+.+.........+...+..+.+.....+.......+......+..............+.+...........+....+......+...+...+...+..+...+.+.....+....+.....+......+....+..+.........+................+........+....+......+..+.........+....+..+...+.+...+...+........+......+...+............................+..+...+...............+...........................+.+.....+.+........+...+..................+..............................+....+..+....+..+.......+..+.+...+...............+..............+...+.........+..........+.....................+.........+.....+.................................+.+..+...+.+...+...........+.+...+.....+.+.....................+......+..+...+...+...................+.....+..........+............+.........+..+.......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----

Notice
------
Private-Key and Public-Certificate-Request files created.
Your files are:
* req: /etc/openvpn/easy-rsa/pki/reqs/team-1-5.req
* key: /etc/openvpn/easy-rsa/pki/private/team-1-5.key

You are about to sign the following certificate:
Request subject, to be signed as a client certificate
for '825' days:

subject=
    commonName                = team-1-5

Type the word 'yes' to continue, or any other input to abort.
  Confirm request details:
Using configuration from /etc/openvpn/easy-rsa/pki/openssl-easyrsa.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'team-1-5'
Certificate is to be certified until Jun 29 02:04:36 2027 GMT (825 days)

Write out database with 1 new entries
Database updated

Notice
------
Certificate created at:
* /etc/openvpn/easy-rsa/pki/issued/team-1-5.crt

Notice
------
Inline file created:
* /etc/openvpn/easy-rsa/pki/inline/team-1-5.inline

User team-1-5 successfully created!
RTNETLINK answers: File exists
Creating team rules 2
Creating user team-2-1
No Easy-RSA 'vars' configuration file exists!

Using SSL:
* openssl OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
.......+...+............+........+...+.+......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+....+...............+..+...+....+...........+.........+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*...........+.....+....+..+.+.....+....+.....+...+......................+...+......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
......+....+.........+...............+...+.....+.........+.+..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*..........+...+.........+.....+...+.............+...............+.....+.........+...+....+......+........+....+...........+...................+..+.........+.+...+......+..+....+...+...+...+............+..+............+......+....+.....+.+...+.........+.....+.+.........+...........+....+...............+.....+......+.+.........+..+......................+..+.+...+.........+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----

Notice
------
Private-Key and Public-Certificate-Request files created.
Your files are:
* req: /etc/openvpn/easy-rsa/pki/reqs/team-2-1.req
* key: /etc/openvpn/easy-rsa/pki/private/team-2-1.key

You are about to sign the following certificate:
Request subject, to be signed as a client certificate
for '825' days:

subject=
    commonName                = team-2-1

Type the word 'yes' to continue, or any other input to abort.
  Confirm request details:
Using configuration from /etc/openvpn/easy-rsa/pki/openssl-easyrsa.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'team-2-1'
Certificate is to be certified until Jun 29 02:04:48 2027 GMT (825 days)

Write out database with 1 new entries
Database updated

Notice
------
Certificate created at:
* /etc/openvpn/easy-rsa/pki/issued/team-2-1.crt

Notice
------
Inline file created:
* /etc/openvpn/easy-rsa/pki/inline/team-2-1.inline

User team-2-1 successfully created!
Creating user team-2-2
No Easy-RSA 'vars' configuration file exists!

Using SSL:
* openssl OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
.+..+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*...+.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*...+...........+.......+...+.....+.......+............+...........+...+.+......+.....+.........+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
....+.........+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.......+......+......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+.......+...+.....+...+....+..+.+.....+.........+....+..............+.......+...........+.........+.+........+.........+.+...........+.+..+.......+...+..+......+.......+...+..+...+.......+......+.....+..........+......+.........+...........+.+..+..........+...+..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----

Notice
------
Private-Key and Public-Certificate-Request files created.
Your files are:
* req: /etc/openvpn/easy-rsa/pki/reqs/team-2-2.req
* key: /etc/openvpn/easy-rsa/pki/private/team-2-2.key

You are about to sign the following certificate:
Request subject, to be signed as a client certificate
for '825' days:

subject=
    commonName                = team-2-2

Type the word 'yes' to continue, or any other input to abort.
  Confirm request details:
Using configuration from /etc/openvpn/easy-rsa/pki/openssl-easyrsa.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'team-2-2'
Certificate is to be certified until Jun 29 02:04:49 2027 GMT (825 days)

Write out database with 1 new entries
Database updated

Notice
------
Certificate created at:
* /etc/openvpn/easy-rsa/pki/issued/team-2-2.crt

Notice
------
Inline file created:
* /etc/openvpn/easy-rsa/pki/inline/team-2-2.inline

User team-2-2 successfully created!
Creating user team-2-3
No Easy-RSA 'vars' configuration file exists!

Using SSL:
* openssl OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
...+.+.........+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*...+...+.......+........+.......+...+.........+..+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*...+...+..............+...+.+..............+...+...+.........+.....................+.+.....+....+............+........+....+..+.+.....+............+...+....+.....+.........+....+...+.........+........+.+...........+...+......+.....................+...............+.+..+.+...........+....+..+...+.......+..+......+.......+..+.......+..............+....+..+...+..........+.................+...+.+.........+.......................+...+................+.....+......+..................+.+...+..+......+...+.........+...+.......+......+......+...+...........+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
......+........+............+...+...+....+...+.....+...+.........+......+.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*...+...+.......+.....+.+...+......+........+......+......+....+.....+....+..+.+.....+.............+.........+...........+....+......+...........+....+.........+..+.+.........+.....+.+........+.......+..+.+..............+...+............+.+.....+.+........+.......+......+.........+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*........+..+......+......+...+.......+.........+.........+........+...............+..........+...+...........+.+.........+......+...+..+.........+.............+......+.....+......+.+..+..........+.....+...+.......+......+..+...+.+.....+..........+........+......+.+......+.....+...+.+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----

Notice
------
Private-Key and Public-Certificate-Request files created.
Your files are:
* req: /etc/openvpn/easy-rsa/pki/reqs/team-2-3.req
* key: /etc/openvpn/easy-rsa/pki/private/team-2-3.key

You are about to sign the following certificate:
Request subject, to be signed as a client certificate
for '825' days:

subject=
    commonName                = team-2-3

Type the word 'yes' to continue, or any other input to abort.
  Confirm request details:
Using configuration from /etc/openvpn/easy-rsa/pki/openssl-easyrsa.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'team-2-3'
Certificate is to be certified until Jun 29 02:04:49 2027 GMT (825 days)

Write out database with 1 new entries
Database updated

Notice
------
Certificate created at:
* /etc/openvpn/easy-rsa/pki/issued/team-2-3.crt

Notice
------
Inline file created:
* /etc/openvpn/easy-rsa/pki/inline/team-2-3.inline

User team-2-3 successfully created!
Creating user team-2-4
No Easy-RSA 'vars' configuration file exists!

Using SSL:
* openssl OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
.+..+.......+..+......+....+...+.....+.+..+....+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+.........+..+....+..+.......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*............+.+......+...........+....+......+...+..............+.......+.....+.+.........+...+......+.........+...+..+.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
...+...+.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*......+..+......+.......+..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.....+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----

Notice
------
Private-Key and Public-Certificate-Request files created.
Your files are:
* req: /etc/openvpn/easy-rsa/pki/reqs/team-2-4.req
* key: /etc/openvpn/easy-rsa/pki/private/team-2-4.key

You are about to sign the following certificate:
Request subject, to be signed as a client certificate
for '825' days:

subject=
    commonName                = team-2-4

Type the word 'yes' to continue, or any other input to abort.
  Confirm request details:
Using configuration from /etc/openvpn/easy-rsa/pki/openssl-easyrsa.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'team-2-4'
Certificate is to be certified until Jun 29 02:04:49 2027 GMT (825 days)

Write out database with 1 new entries
Database updated

Notice
------
Certificate created at:
* /etc/openvpn/easy-rsa/pki/issued/team-2-4.crt

Notice
------
Inline file created:
* /etc/openvpn/easy-rsa/pki/inline/team-2-4.inline

User team-2-4 successfully created!
Creating user team-2-5
No Easy-RSA 'vars' configuration file exists!

Using SSL:
* openssl OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
.......+.....+......+....+...............+...+..+.+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+..+..........+..................+........+.......+.......................+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+.......+..+.+...+..............+...+...+.+...............+.....+....+.........+..+.............+.....+.+.....+....+...+..+.....................+......+....+...........+......+..........+.....+.......+.....................+..+...+.+...............+...+.....+.+...........+......+....+.....+..........+.....................+..+..........+......+............+........+.+......+........+......+.............+..+...+...+....+.....................+...+.........+.....+...+............+......+....+..+................+...+..+.........+......+....+...+...+...+..+...+......+...+..........+.....+......................+.....+..........+......+........+.+...+...........+.......+........+......+.+.........+.........+............+..+.+..+.......+..+.........+.+.........+.....+...............+.+...+..+......+.........+......+.......+..+....+.........+.....+...+....+.....+...+.......+........+.......+........+..................+..........+...+..+............+.+..+.......+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
..........+..+..........+...+.....+...+....+...+........+...+.........+.+...........+.+..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+...+....+...+..................+.....+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.....+.......+.....+..........+..+.+...........+.+............+.....+..........+...+..............+.+..+..................+....+...+.....+..........+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----

Notice
------
Private-Key and Public-Certificate-Request files created.
Your files are:
* req: /etc/openvpn/easy-rsa/pki/reqs/team-2-5.req
* key: /etc/openvpn/easy-rsa/pki/private/team-2-5.key

You are about to sign the following certificate:
Request subject, to be signed as a client certificate
for '825' days:

subject=
    commonName                = team-2-5

Type the word 'yes' to continue, or any other input to abort.
  Confirm request details:
Using configuration from /etc/openvpn/easy-rsa/pki/openssl-easyrsa.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'team-2-5'
Certificate is to be certified until Jun 29 02:04:50 2027 GMT (825 days)

Write out database with 1 new entries
Database updated

Notice
------
Certificate created at:
* /etc/openvpn/easy-rsa/pki/issued/team-2-5.crt

Notice
------
Inline file created:
* /etc/openvpn/easy-rsa/pki/inline/team-2-5.inline

User team-2-5 successfully created!
RTNETLINK answers: File exists
Starting OpenVPN service
Creating teams vms
Creating team vms 1
Initializing team 1 VMs (might take a while)
[Thread-2] Authenticating...
[Thread-0] Authenticating...
[Thread-1] Authenticating...
[Thread-0] [DEBUG] Created VM SHIFT_CTF-Team 1-Teste VM1 with ID 7c68d1e0-eb04-d7e4-2bf0-02b753cc843c
[Thread-2] [DEBUG] Created VM SHIFT_CTF-Team 1-Teste VM3 with ID f20f61d7-5d58-42da-2989-27d3f2c61b2f
[DEBUG] VM 7c68d1e0-eb04-d7e4-2bf0-02b753cc843c is running but no IP yet. Retrying (2/30)...
[Thread-1] [DEBUG] Created VM SHIFT_CTF-Team 1-Teste VM2 with ID 696753a2-c77a-0b87-a731-e349b4eb9fed
[DEBUG] VM f20f61d7-5d58-42da-2989-27d3f2c61b2f is running but no IP yet. Retrying (2/30)...
[DEBUG] VM 7c68d1e0-eb04-d7e4-2bf0-02b753cc843c is running but no IP yet. Retrying (3/30)...
[DEBUG] VM 696753a2-c77a-0b87-a731-e349b4eb9fed is running but no IP yet. Retrying (2/30)...
[DEBUG] VM f20f61d7-5d58-42da-2989-27d3f2c61b2f is running but no IP yet. Retrying (3/30)...
[DEBUG] VM 7c68d1e0-eb04-d7e4-2bf0-02b753cc843c is running but no IP yet. Retrying (4/30)...
[DEBUG] VM 696753a2-c77a-0b87-a731-e349b4eb9fed is running but no IP yet. Retrying (3/30)...
[DEBUG] VM f20f61d7-5d58-42da-2989-27d3f2c61b2f is running but no IP yet. Retrying (4/30)...
[DEBUG] VM 7c68d1e0-eb04-d7e4-2bf0-02b753cc843c is running but no IP yet. Retrying (5/30)...
[DEBUG] VM 696753a2-c77a-0b87-a731-e349b4eb9fed is running but no IP yet. Retrying (4/30)...
[DEBUG] VM f20f61d7-5d58-42da-2989-27d3f2c61b2f is running but no IP yet. Retrying (5/30)...
[DEBUG] VM 7c68d1e0-eb04-d7e4-2bf0-02b753cc843c is running but no IP yet. Retrying (6/30)...
[DEBUG] VM 696753a2-c77a-0b87-a731-e349b4eb9fed is running but no IP yet. Retrying (5/30)...
[DEBUG] VM f20f61d7-5d58-42da-2989-27d3f2c61b2f is running but no IP yet. Retrying (6/30)...
[DEBUG] VM 7c68d1e0-eb04-d7e4-2bf0-02b753cc843c is fully booted and IP assigned.
[DEBUG] VM 696753a2-c77a-0b87-a731-e349b4eb9fed is running but no IP yet. Retrying (6/30)...
[DEBUG] VM f20f61d7-5d58-42da-2989-27d3f2c61b2f is fully booted and IP assigned.
[DEBUG] VM 696753a2-c77a-0b87-a731-e349b4eb9fed is running but no IP yet. Retrying (7/30)...
[DEBUG] VM 696753a2-c77a-0b87-a731-e349b4eb9fed is fully booted and IP assigned.
[DEBUG] SSH is available on 10.3.3.28
[DEBUG] Connecting to 10.3.3.28 as kali...
[DEBUG] Initial Shell Output:
Linux kali 6.11.2-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.11.2-1kali1 (2024-10-15) x86_64

The programs included with the Kali GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Kali GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Mar 11 13:53:30 2025 from 10.16.0.64
kali@kali:~$
[DEBUG] Executing default command: echo 'Command started...' | sudo tee /tmp/command_config.log
[DEBUG] Command Output:
echo 'Command started...' | sudo tee /tmp/command_config.log
[sudo] password for kali:
[DEBUG] Detected sudo password prompt, entering password...
[DEBUG] Post-Password Output:

Command started...

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' ipv4.addresses 10.1.1.2/24 ipv4.method manual
[DEBUG] Command Output:
ipv4.method manual

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' ipv4.gateway 10.1.1.1
[DEBUG] Command Output:
sudo nmcli con mod 'Wired connection 1' ipv4.gateway 10.1.1.1

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' +ipv4.routes '10.1.0.0/24 10.1.1.1'
[DEBUG] Command Output:
0.1.1.1'

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con up 'Wired connection 1'
[DEBUG] Command Output:
sudo nmcli con up 'Wired connection 1'
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/8)

kali@kali:~$
[DEBUG] Executing default command: sudo systemctl restart NetworkManager
[DEBUG] SSH is available on 10.3.1.244
[DEBUG] Connecting to 10.3.1.244 as kali...
[DEBUG] Command Output:
sudo systemctl restart NetworkManager

kali@kali:~$
[DEBUG] Executing default command: echo 'Network configured successfully' | sudo tee /tmp/network_config.log
[DEBUG] Initial Shell Output:
Linux kali 6.11.2-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.11.2-1kali1 (2024-10-15) x86_64

The programs included with the Kali GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Kali GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Mar 11 13:53:30 2025 from 10.16.0.64
kali@kali:~$
[DEBUG] Executing default command: echo 'Command started...' | sudo tee /tmp/command_config.log
[DEBUG] Command Output:
ig.log
Network configured successfully

kali@kali:~$
[DEBUG] Executing challenge-specific command: echo 'Hello World'
[DEBUG] Command Output:
echo 'Command started...' | sudo tee /tmp/command_config.log
[sudo] password for kali:
[DEBUG] Detected sudo password prompt, entering password...
[DEBUG] Command Output:
echo 'Hello World'
Hello World

kali@kali:~$
[DEBUG] Executing challenge-specific command: touch teste.txt
[DEBUG] Post-Password Output:

Command started...

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' ipv4.addresses 10.1.1.4/24 ipv4.method manual
[DEBUG] Command Output:
touch teste.txt

kali@kali:~$
[DEBUG] Commands executed successfully!
[DEBUG] Removing Temporary VIF (1300e8c3-67b3-a911-373a-2825d81c613e) from VM 7c68d1e0-eb04-d7e4-2bf0-02b753cc843c
[DEBUG] Command Output:
ipv4.method manual

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' ipv4.gateway 10.1.1.1
[DEBUG] Command Output:
sudo nmcli con mod 'Wired connection 1' ipv4.gateway 10.1.1.1

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' +ipv4.routes '10.1.0.0/24 10.1.1.1'
[DEBUG] Command Output:
0.1.1.1'

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con up 'Wired connection 1'
[DEBUG] Command Output:
sudo nmcli con up 'Wired connection 1'
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/8)

kali@kali:~$
[DEBUG] Executing default command: sudo systemctl restart NetworkManager
[DEBUG] Command Output:
sudo systemctl restart NetworkManager

kali@kali:~$
[DEBUG] Executing default command: echo 'Network configured successfully' | sudo tee /tmp/network_config.log
[DEBUG] Command Output:
ig.log
Network configured successfully

kali@kali:~$
[DEBUG] Executing challenge-specific command: echo 'Hello World'
[DEBUG] Command Output:
echo 'Hello World'
Hello World

kali@kali:~$
[DEBUG] Executing challenge-specific command: touch teste.txt
[DEBUG] Command Output:
touch teste.txt

kali@kali:~$
[DEBUG] Commands executed successfully!
[DEBUG] Removing Temporary VIF (d741d262-556d-7a4f-a0ac-0a4d3379f2f8) from VM f20f61d7-5d58-42da-2989-27d3f2c61b2f
[DEBUG] SSH is available on 10.3.1.146
[DEBUG] Connecting to 10.3.1.146 as kali...
[DEBUG] Initial Shell Output:
Linux kali 6.11.2-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.11.2-1kali1 (2024-10-15) x86_64

The programs included with the Kali GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Kali GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Mar 11 13:53:30 2025 from 10.16.0.64
kali@kali:~$
[DEBUG] Executing default command: echo 'Command started...' | sudo tee /tmp/command_config.log
[DEBUG] Command Output:
echo 'Command started...' | sudo tee /tmp/command_config.log
[sudo] password for kali:
[DEBUG] Detected sudo password prompt, entering password...
[DEBUG] Post-Password Output:

Command started...

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' ipv4.addresses 10.1.1.3/24 ipv4.method manual
[DEBUG] Command Output:
ipv4.method manual

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' ipv4.gateway 10.1.1.1
[DEBUG] Command Output:
sudo nmcli con mod 'Wired connection 1' ipv4.gateway 10.1.1.1

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' +ipv4.routes '10.1.0.0/24 10.1.1.1'
[DEBUG] Command Output:
0.1.1.1'

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con up 'Wired connection 1'
[DEBUG] Command Output:
sudo nmcli con up 'Wired connection 1'
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/8)

kali@kali:~$
[DEBUG] Executing default command: sudo systemctl restart NetworkManager
[DEBUG] Command Output:
sudo systemctl restart NetworkManager

kali@kali:~$
[DEBUG] Executing default command: echo 'Network configured successfully' | sudo tee /tmp/network_config.log
[DEBUG] Command Output:
ig.log
Network configured successfully

kali@kali:~$
[DEBUG] Executing challenge-specific command: echo 'Hello World'
[DEBUG] Command Output:
echo 'Hello World'
Hello World

kali@kali:~$
[DEBUG] Executing challenge-specific command: touch teste.txt
[DEBUG] Command Output:
touch teste.txt

kali@kali:~$
[DEBUG] Commands executed successfully!
[DEBUG] Removing Temporary VIF (d2696ecf-53ef-9020-ecae-bc5d113a05c7) from VM 696753a2-c77a-0b87-a731-e349b4eb9fed
End Of Script

real    4m5.923s
user    0m0.710s
sys     0m0.192s
Creating team vms 2
Initializing team 2 VMs (might take a while)
[Thread-1] Authenticating...
[Thread-0] Authenticating...
[Thread-2] Authenticating...
[Thread-0] [DEBUG] Created VM SHIFT_CTF-Team 2-Teste VM1 with ID afe772a8-663d-4261-71ac-a76d0afea6d5
[Thread-2] [DEBUG] Created VM SHIFT_CTF-Team 2-Teste VM3 with ID 4554cd51-e65d-9681-c601-f1186e98b108
[Thread-1] [DEBUG] Created VM SHIFT_CTF-Team 2-Teste VM2 with ID 096ff98c-9b4a-b5d9-993f-13ec64e48dfe
[DEBUG] VM afe772a8-663d-4261-71ac-a76d0afea6d5 is running but no IP yet. Retrying (2/30)...
[DEBUG] VM 4554cd51-e65d-9681-c601-f1186e98b108 is running but no IP yet. Retrying (2/30)...
[DEBUG] VM 096ff98c-9b4a-b5d9-993f-13ec64e48dfe is running but no IP yet. Retrying (2/30)...
[DEBUG] VM afe772a8-663d-4261-71ac-a76d0afea6d5 is running but no IP yet. Retrying (3/30)...
[DEBUG] VM 4554cd51-e65d-9681-c601-f1186e98b108 is running but no IP yet. Retrying (3/30)...
[DEBUG] VM 096ff98c-9b4a-b5d9-993f-13ec64e48dfe is running but no IP yet. Retrying (3/30)...
[DEBUG] VM afe772a8-663d-4261-71ac-a76d0afea6d5 is running but no IP yet. Retrying (4/30)...
[DEBUG] VM 4554cd51-e65d-9681-c601-f1186e98b108 is running but no IP yet. Retrying (4/30)...
[DEBUG] VM 096ff98c-9b4a-b5d9-993f-13ec64e48dfe is running but no IP yet. Retrying (4/30)...
[DEBUG] VM afe772a8-663d-4261-71ac-a76d0afea6d5 is running but no IP yet. Retrying (5/30)...
[DEBUG] VM 4554cd51-e65d-9681-c601-f1186e98b108 is running but no IP yet. Retrying (5/30)...
[DEBUG] VM 096ff98c-9b4a-b5d9-993f-13ec64e48dfe is running but no IP yet. Retrying (5/30)...
[DEBUG] VM afe772a8-663d-4261-71ac-a76d0afea6d5 is running but no IP yet. Retrying (6/30)...
[DEBUG] VM 4554cd51-e65d-9681-c601-f1186e98b108 is running but no IP yet. Retrying (6/30)...
[DEBUG] VM 096ff98c-9b4a-b5d9-993f-13ec64e48dfe is running but no IP yet. Retrying (6/30)...
[DEBUG] VM afe772a8-663d-4261-71ac-a76d0afea6d5 is fully booted and IP assigned.
[DEBUG] VM 4554cd51-e65d-9681-c601-f1186e98b108 is fully booted and IP assigned.
[DEBUG] VM 096ff98c-9b4a-b5d9-993f-13ec64e48dfe is running but no IP yet. Retrying (7/30)...
[DEBUG] VM 096ff98c-9b4a-b5d9-993f-13ec64e48dfe is fully booted and IP assigned.
[DEBUG] SSH is available on 10.3.3.139
[DEBUG] Connecting to 10.3.3.139 as kali...
[DEBUG] Initial Shell Output:
Linux kali 6.11.2-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.11.2-1kali1 (2024-10-15) x86_64

The programs included with the Kali GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Kali GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Mar 11 13:53:30 2025 from 10.16.0.64
kali@kali:~$
[DEBUG] Executing default command: echo 'Command started...' | sudo tee /tmp/command_config.log
[DEBUG] Command Output:
echo 'Command started...' | sudo tee /tmp/command_config.log
[sudo] password for kali:
[DEBUG] Detected sudo password prompt, entering password...
[DEBUG] Post-Password Output:

Command started...

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' ipv4.addresses 10.2.1.2/24 ipv4.method manual
[DEBUG] Command Output:
ipv4.method manual

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' ipv4.gateway 10.2.1.1
[DEBUG] Command Output:
sudo nmcli con mod 'Wired connection 1' ipv4.gateway 10.2.1.1

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' +ipv4.routes '10.1.0.0/24 10.2.1.1'
[DEBUG] Command Output:
0.2.1.1'

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con up 'Wired connection 1'
[DEBUG] SSH is available on 10.3.1.184
[DEBUG] Connecting to 10.3.1.184 as kali...
[DEBUG] Command Output:
sudo nmcli con up 'Wired connection 1'
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/8)

kali@kali:~$
[DEBUG] Executing default command: sudo systemctl restart NetworkManager
[DEBUG] Initial Shell Output:
Linux kali 6.11.2-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.11.2-1kali1 (2024-10-15) x86_64

The programs included with the Kali GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Kali GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Mar 11 13:53:30 2025 from 10.16.0.64
kali@kali:~$
[DEBUG] Executing default command: echo 'Command started...' | sudo tee /tmp/command_config.log
[DEBUG] Command Output:
sudo systemctl restart NetworkManager

kali@kali:~$
[DEBUG] Executing default command: echo 'Network configured successfully' | sudo tee /tmp/network_config.log
[DEBUG] Command Output:
echo 'Command started...' | sudo tee /tmp/command_config.log
[sudo] password for kali:
[DEBUG] Detected sudo password prompt, entering password...
[DEBUG] Command Output:
ig.log
Network configured successfully

kali@kali:~$
[DEBUG] Executing challenge-specific command: echo 'Hello World'
[DEBUG] Post-Password Output:

Command started...

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' ipv4.addresses 10.2.1.4/24 ipv4.method manual
[DEBUG] Command Output:
echo 'Hello World'
Hello World

kali@kali:~$
[DEBUG] Executing challenge-specific command: touch teste.txt
[DEBUG] Command Output:
ipv4.method manual

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' ipv4.gateway 10.2.1.1
[DEBUG] Command Output:
touch teste.txt

kali@kali:~$
[DEBUG] Commands executed successfully!
[DEBUG] Removing Temporary VIF (62fcda9a-7b28-5633-9f96-a0c9e37c6622) from VM afe772a8-663d-4261-71ac-a76d0afea6d5
[DEBUG] Command Output:
sudo nmcli con mod 'Wired connection 1' ipv4.gateway 10.2.1.1

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' +ipv4.routes '10.1.0.0/24 10.2.1.1'
[DEBUG] Command Output:
0.2.1.1'

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con up 'Wired connection 1'
[DEBUG] Command Output:
sudo nmcli con up 'Wired connection 1'
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/8)

kali@kali:~$
[DEBUG] Executing default command: sudo systemctl restart NetworkManager
[DEBUG] Command Output:
sudo systemctl restart NetworkManager

kali@kali:~$
[DEBUG] Executing default command: echo 'Network configured successfully' | sudo tee /tmp/network_config.log
[DEBUG] Command Output:
ig.log
Network configured successfully

kali@kali:~$
[DEBUG] Executing challenge-specific command: echo 'Hello World'
[DEBUG] Command Output:
echo 'Hello World'
Hello World

kali@kali:~$
[DEBUG] Executing challenge-specific command: touch teste.txt
[DEBUG] Command Output:
touch teste.txt

kali@kali:~$
[DEBUG] Commands executed successfully!
[DEBUG] Removing Temporary VIF (60ebf89c-6f7c-4674-1430-09bd5eb0067e) from VM 4554cd51-e65d-9681-c601-f1186e98b108
[DEBUG] SSH is available on 10.3.3.121
[DEBUG] Connecting to 10.3.3.121 as kali...
[DEBUG] Initial Shell Output:
Linux kali 6.11.2-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.11.2-1kali1 (2024-10-15) x86_64

The programs included with the Kali GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Kali GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Mar 11 13:53:30 2025 from 10.16.0.64
kali@kali:~$
[DEBUG] Executing default command: echo 'Command started...' | sudo tee /tmp/command_config.log
[DEBUG] Command Output:
echo 'Command started...' | sudo tee /tmp/command_config.log
[sudo] password for kali:
[DEBUG] Detected sudo password prompt, entering password...
[DEBUG] Post-Password Output:

Command started...

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' ipv4.addresses 10.2.1.3/24 ipv4.method manual
[DEBUG] Command Output:
ipv4.method manual

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' ipv4.gateway 10.2.1.1
[DEBUG] Command Output:
sudo nmcli con mod 'Wired connection 1' ipv4.gateway 10.2.1.1

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con mod 'Wired connection 1' +ipv4.routes '10.1.0.0/24 10.2.1.1'
[DEBUG] Command Output:
0.2.1.1'

kali@kali:~$
[DEBUG] Executing default command: sudo nmcli con up 'Wired connection 1'
[DEBUG] Command Output:
sudo nmcli con up 'Wired connection 1'
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/8)

kali@kali:~$
[DEBUG] Executing default command: sudo systemctl restart NetworkManager
[DEBUG] Command Output:
sudo systemctl restart NetworkManager

kali@kali:~$
[DEBUG] Executing default command: echo 'Network configured successfully' | sudo tee /tmp/network_config.log
[DEBUG] Command Output:
ig.log
Network configured successfully

kali@kali:~$
[DEBUG] Executing challenge-specific command: echo 'Hello World'
[DEBUG] Command Output:
echo 'Hello World'
Hello World

kali@kali:~$
[DEBUG] Executing challenge-specific command: touch teste.txt
[DEBUG] Command Output:
touch teste.txt

kali@kali:~$
[DEBUG] Commands executed successfully!
[DEBUG] Removing Temporary VIF (506af47d-de39-c5cb-81a6-cf6230d58d0a) from VM 096ff98c-9b4a-b5d9-993f-13ec64e48dfe
End Of Script

real    3m58.783s
user    0m0.715s
sys     0m0.201s
Script finished