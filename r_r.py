import OpenOPC
import logging
import threading
import time
import os

from redis import Redis
import json

def connect():
    try:
        remote.set("registry", local.get("registry"))
    except Exception as e:
        print e, "failed connect"
        connect()
        pass
    finally:
        pass

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
        print e, "failed run"
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

local = Redis(host=local_redis_server)
remote = Redis(host=remote_redis_server, port=remote_redis_port, password=remote_redis_password)
logging.basicConfig()
log = logging.getLogger(__name__)


#attempt to connect
connect()

tags = json.loads(local.get("registry"))

# start service
while True:
    run()