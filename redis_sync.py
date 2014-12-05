import OpenOPC
import logging
import threading
import time
import os

from redis import Redis
import json

def connect():
    global local
    global remote
    try:
        local = Redis(host=local_redis_server)
        remote = Redis(host=remote_redis_server, port=remote_redis_port, password=remote_redis_password)
    except Exception as e:
        print e, "failed connect"
        time.sleep(poll_rate)
        connect()
        pass
    finally:
        pass

def run():
    try:
        for item in local.keys():
            remote.set(item, local.get(item))
    except Exception as e:
        print e, "failed run"
        time.sleep(poll_rate)
        connect()
        pass
    finally:
        time.sleep(poll_rate)
        pass

# CONFIG
print "starting up!"

local_redis_server = 'localhost'
remote_redis_password = "hjrDouFuQPhNuhmL"
remote_redis_server = "pub-redis-19711.us-east-1-4.4.ec2.garantiadata.com"
remote_redis_port = 19711
poll_rate = 0.3

local = None
remote = None

logging.basicConfig()
log = logging.getLogger(__name__)

#attempt to connect
connect()

# start service
while True:
    run()