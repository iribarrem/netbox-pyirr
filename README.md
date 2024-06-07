# Netbox-PyIRR - Netbox Prefix-list updates from IRR

## Features
Netbox-PyIRR retrivies BGP Prefixes based on IRR objects using BGPq4, then it creates IPv4 and IPv6 prefix-lists in Netbox.

## Requirements
The server running this script **must** have BGPq4 package installed.

Debian example:
```
apt-get install bgpq4
```

## Installation
1. Clone git repository
2. Adjust NETBOX_URL and NETBOX_TOKEN variables in .env file
3. Install required packages (virtualenv recommended)
```
pip install -r local-requirements.txt
```

## Usage
The command takes as arguments ASNs or AS-SETs.

```
> python3 pyirr.py AS-DNS-BR AS26162                  
2024-06-06 22:09:20,020 root         INFO     Prefix-list AS-DNS-BR_IPv4 created!
2024-06-06 22:09:20,105 root         INFO     Prefix-list AS-DNS-BR_IPv6 created!
2024-06-06 22:09:22,358 root         INFO     All prefix-list rules were updated!
2024-06-06 22:10:39,728 root         INFO     Prefix-list AS26162_IPv4 created!
2024-06-06 22:10:39,809 root         INFO     Prefix-list AS26162_IPv6 created!
2024-06-06 22:10:39,897 root         INFO     All prefix-list rules were updated!
```