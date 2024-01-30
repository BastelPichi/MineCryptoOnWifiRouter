#!/usr/bin/env python3
# Duino-Coin Router Miner. Heavily based on the duino-coin Minimal PC Miner by BastelPichi 2022.
# Originally by Revox

import hashlib
import os
from socket import socket
import sys  # Only python3 included libraries
import time
import requests

username = "Pichi"  # add your username here.
mining_key = "None"  # change this to your mining key, or leave as is.

leds = True  # True if led notifications should be enabled, if not, False.
accepted = "fritz4040:amber:info"  # Name of the LED that should blink on an accepted share.
rejected = "fritz4040:red:info"  # Name of the LED that should blink on a rejected share.

soc = socket()
session = requests.Session()
current_time_format = "%H:%M:%S"

def current_time():
    return time.strftime(current_time_format, time.localtime())

def fetch_pools():
    while True:
        try:
            response = session.get("https://server.duinocoin.com/getPool").json()
            NODE_ADDRESS, NODE_PORT = response["ip"], response["port"]
            return NODE_ADDRESS, NODE_PORT
        except Exception as e:
            print(f"{current_time()}: Error retrieving mining node, retrying in 15s")
            time.sleep(15)

def led(status):
    if leds:
        led_path = f"/sys/class/leds/{accepted if status else rejected}/brightness"
        with open(led_path, "w") as f:
            f.write("1")
            time.sleep(0.3)
            f.write("0")
    else:
        pass

while True:
    try:
        print(f"{current_time()}: Searching for the fastest connection to the server")
        try:
            NODE_ADDRESS, NODE_PORT = fetch_pools()
        except Exception as e:
            NODE_ADDRESS, NODE_PORT = "server.duinocoin.com", 2813
            print(f"{current_time()}: Using default server port and address")
        soc.connect((str(NODE_ADDRESS), int(NODE_PORT)))
        print(f"{current_time()}: Fastest connection found")
        server_version = soc.recv(100).decode()
        print(f"{current_time()}: Server Version: {server_version}")
        
        # Mining section
        while True:
            soc.send(bytes(f"JOB,{username},LOW,{mining_key}", encoding="utf8"))

            # Receive work
            job = soc.recv(1024).decode().rstrip("\n")
            # Split received data to job and difficulty
            job = job.split(",")
            difficulty = job[2]

            hashingStartTime = time.time()
            base_hash = hashlib.sha1(job[0].encode("ascii"))
            temp_hash = None

            for result in range(100 * int(difficulty) + 1):
                # Calculate hash with difficulty
                temp_hash = base_hash.copy()
                temp_hash.update(str(result).encode("ascii"))
                ducos1 = temp_hash.hexdigest()

                # If hash is even with expected hash result
                if job[1] == ducos1:
                    hashingStopTime = time.time()
                    timeDifference = hashingStopTime - hashingStartTime
                    hashrate = result / timeDifference

                    # Send numeric result to the server
                    soc.send(bytes(f"{result},{hashrate},Router Miner", encoding="utf8"))

                    # Get feedback about the result
                    feedback = soc.recv(1024).decode().rstrip("\n")
                    # If the result was good
                    if feedback == "GOOD":
                        print(f"{current_time()}: Accepted share",
                              result,
                              "Hashrate",
                              int(hashrate/1000),
                              "kH/s",
                              "Difficulty",
                              difficulty)
                        led(True)
                        break
                    # If the result was incorrect
                    elif feedback == "BAD":
                        print(f"{current_time()}: Rejected share",
                              result,
                              "Hashrate",
                              int(hashrate/1000),
                              "kH/s",
                              "Difficulty",
                              difficulty)
                        led(False)
                        break

    except Exception as e:
        print(f"{current_time()}: Error occurred: {e}, restarting in 5s.")
        time.sleep(5)
        os.execl(sys.executable, sys.executable, *sys.argv)
