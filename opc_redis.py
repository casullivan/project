import OpenOPC
import logging
import threading
import time
import os

from sh import grep
from sh import ping
from sh import nmap
from sh import opc

from redis import Redis
import json

def connect():
    global opc 
    global list
    opc = None
    list = None
    r.set("connected", "BAD")
    while list is None:
            try:
                opc = OpenOPC.open_client(opc_server)
                opc.connect(opc_server_name, opc_server)
                list = opc.list('Brave.calendar.opc_group')
                r.set("connected", "OK")
                r.set("opc_server", opc_server)
                r.set("opc_server_name", opc_server_name)
                r.set("plc", plc)
                r.set("redis_server", redis_server)
            except Exception as e:
                try:
                    ping(plc, c=1)
                    print {'error': 'Cannot connect to ' + opc_server_name, 'val': 0}
                except Exception as e:
                    print {'error': 'Cannot connect to network', 'val': 0}
                    pass
                pass
            finally:
                time.sleep(poll_rate)

def run():    
    tags = None
    while tags is None:
        time.sleep(poll_rate)
        try:
            tags = opc.read(list)
        except Exception as e:
            try:
                ping(plc, c=1)
                print {'error': 'Cannot connect to ' + opc_server_name, 'val': 0}
                connect()
            except Exception as e:
                print {'error': 'Cannot connect to network', 'val': 0}
                connect()
                pass
            pass
        finally:
            pass
    for item in tags:
        r.set(item[0], item[1])
    if debug: print r.get(item[0])
    if debug: print r.get("registry")


# CONFIG
debug = False
opc_server = '192.168.1.80'
opc_server_name = 'Kepware.KEPServerEX.V5'
redis_server = 'localhost'
plc = '192.168.1.2'
poll_rate = 0.3

r = Redis(host=redis_server)

logging.basicConfig()
log = logging.getLogger(__name__)

#init vars
opc = None
list = None

#attempt to connect
connect()

r.set("registry", json.dumps(list))

# start service
while True:
    run()