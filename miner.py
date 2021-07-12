#!/usr/bin/env python3
# Router Miner, created by BastelPichi.
# Modifications made by ihyoudou
import hashlib
import os
import socket
import sys
import time
import urllib.request
import json

soc = socket.socket()
soc.settimeout(10)

username = "Pichi"  # Edit this to your username, mind the quotes

enableLEDNotification = False # Edit this to enable or disable LED notification (True/False)
ledaccepted = "fritz4040:amber:info" # Edit this to your first LED name, leave as is if you disabled led notifications above.
ledrejected = "fritz4040:red:info" # Edit this to your second LED, leave as is if you disabled led notifications above.

def retrieve_server_ip():
    print("Retrieving Pool Address And Port")
    pool_obtained = False
    while not pool_obtained:
        try:
            serverip = ("https://server.duinocoin.com/getPool")
            # Loading pool address from API as json array
            poolInfo = json.loads(urllib.request.urlopen(serverip).read())
            
            global pool_address, pool_port
            # Line 1 = IP
            pool_address = poolInfo['ip']
            # Line 2 = port
            pool_port = poolInfo['port']
            pool_obtained =  True
        except:
            print("> Failed to retrieve Pool Address and Port, Retrying.")
            continue

retrieve_server_ip()
while True:
    try:
        # This section connects and logs user to the server
        soc.connect((str(pool_address), int(pool_port)))
        server_version = soc.recv(3).decode()  # Get server version
        print("Server is on version", server_version)

        # Mining section
        while True:
            # Send job request 
            soc.send(bytes(
                "JOB,"
                + str(username)
                + ",LOW",
                encoding="utf8"))

            # Receive work
            job = soc.recv(1024).decode().rstrip("\n")
            # Split received data to job and difficulty
            job = job.split(",")
            difficulty = job[2]
            
            hashingStartTime = time.time()
            base_hash = hashlib.sha1(str(job[0]).encode('ascii'))
            temp_hash = None
            
            for result in range(100 * int(difficulty) + 1):
                # Calculate hash with difficulty
                temp_hash =  base_hash.copy()
                temp_hash.update(str(result).encode('ascii'))
                ducos1 = temp_hash.hexdigest()

                # If hash is even with expected hash result
                if job[1] == ducos1:
                    hashingStopTime = time.time()
                    timeDifference = hashingStopTime - hashingStartTime
                    hashrate = result / timeDifference

                    # Send numeric result to the server
                    soc.send(bytes(
                        str(result)
                        + ","
                        + str(hashrate)
                        + ",Router_Miner"
                        + "2.45",
                        encoding="utf8"))

                    # Get feedback about the result
                    feedback = soc.recv(1024).decode().rstrip("\n")
                    # If result was good
                    if feedback == "GOOD":
                        # If LED notification is enabled
                        if enableLEDNotification:
                            file = open(f'/sys/class/leds/{ledaccepted}/brightness','w')
                            file.write('1')
                            file.close()
                            time.sleep(0.3)
                            file = open(f'/sys/class/leds/{ledaccepted}/brightness','w')
                            file.write('0')
                            file.close()
                        print("Accepted share",
                              result,
                              "Hashrate",
                              int(hashrate/1000),
                              "kH/s",
                              "Difficulty",
                              difficulty)
                        break
                    # If result was incorrect
                    elif feedback == "BAD":
                        # If LED notification is enabled
                        if enableLEDNotification:
                            file = open(f'/sys/class/leds/{ledrejected}/brightness','w')
                            file.write('1')
                            file.close()
                            time.sleep(0.3)
                            file = open(f'/sys/class/leds/{ledrejected}/brightness','w')
                            file.write('0')
                            file.close()

                        print("Rejected share",
                              result,
                              "Hashrate",
                              int(hashrate/1000),
                              "kH/s",
                              "Difficulty",
                              difficulty)
                        break

    except Exception as e:
        print("Error occured: " + str(e) + ", restarting in 5s.")
        retrieve_server_ip()
        time.sleep(5)
        os.execl(sys.executable, sys.executable, *sys.argv)
