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
    try:
        remote.set("registry", local.get("registry"))
    except Exception as e:
        pass
    finally:
        time.sleep(poll_rate)

def run():
    time.sleep(poll_rate)
    try:
        for item in tags:
            remote.set(item, local.get(item))

        remote.set('opc_server', local.get('opc_server'))
        remote.set('connected', local.get('connected'))
        remote.set('opc_server', local.get('opc_server'))
        remote.set('plc', local.get('plc'))
        remote.set('opc_server_name', local.get('opc_server_name'))
    
    except Exception as e:
        connect()
        pass
    finally:
        pass

# CONFIG

local_redis_server = 'localhost'
remote_redis_password = "hjrDouFuQPhNuhmL"
remote_redis_server = "pub-redis-19711.us-east-1-4.4.ec2.garantiadata.com"
remote_redis_port = 19711
poll_rate = 0.3

local = Redis(host=redis_server)
remote = Redis(host=remote_redis_server, port=remote_redis_server, password=remote_redis_password)
logging.basicConfig()
log = logging.getLogger(__name__)


#attempt to connect
connect()

# start service
while True:
    run()