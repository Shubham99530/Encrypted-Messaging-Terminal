#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import json

def string_to_acsii(str):
    l = []
    for i in str:
        l.append(ord(i))
    return l

def encrypt(e, plain_text,n):
    m = string_to_acsii(plain_text)
    c = [pow(ch,e,n) for ch in m]
    return c
    
def decrypt(d,cipher,n):
    p = [pow(ch,d,n) for ch in cipher]
    ans = "".join(chr(ch) for ch in p)
    return ans


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
PKDA_PR_key = 1589

keys={"UserA" : '1727', "UserB" : '1277'}
p = 61
q = 53
phi = (p-1) * (q-1)
n = p * q 
while True:
    #  Wait for next request from client
    message = socket.recv_string()
    print(f"Received request: {message}")

    #  Do some 'work'
    time.sleep(1)
    if message.startswith("UserB") :
        message = keys["UserB"]+" " + message
        message = encrypt(PKDA_PR_key,message,n)
        # print(message)
        message = json.dumps(message)
        # print(message)
        socket.send_string(message)
    elif message.startswith("UserA") : 
        message = keys["UserA"]+ " "+ message
        message = encrypt(PKDA_PR_key,message,n)
        message = json.dumps(message)
        # print(message)
        socket.send_string(message)
    #  Send reply back to client
    
