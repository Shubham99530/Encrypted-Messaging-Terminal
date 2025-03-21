#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
import time
import zmq
from datetime import datetime
import json
import random as rand
import threading

context = zmq.Context()


PKDA_PU_key = 269
p = 61
q = 53
phi = (p-1) * (q-1)
n = p * q 
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
# PUa =0
def listen(PUa,PRb):
    socket_UserB = context.socket(zmq.REP)
    socket_UserB.bind("tcp://*:5567")
    while True:

        req = socket_UserB.recv_string()
        req = json.loads(req)

        time.sleep(1)
        print("Encrypted Recieved :",req)
        req = decrypt(PRb,req,n)
        print("Decrypted message :",req)
        # print(req)
        req = req.split()
        nonce_A = req[-1]
        if PUa > 0 and len(req) > 1 and not isinstance(req[0],int):
            nonce_B = rand.randint(100,999)
            message =  str(nonce_A) + " "+ str(nonce_B)
            message = encrypt(PUa,message,n)
            message = json.dumps(message)
            socket_UserB.send_string(message)
        elif len(req) == 1:
            # print("end")
            socket_UserB.send_string("")
        else:
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://localhost:5555")
            current_time = now.strftime("%H:%M:%S")
            request = "UserA" +" "+str(current_time)
            # print(request)
            socket.send_string(request)
            time.sleep(1)
    #  Get the reply.
            message = socket.recv_string()
            # print(message)
            message = json.loads(message)
            message = decrypt(PKDA_PU_key,message,n)
            message = message.split()
            PUa = int(message[0])
            # print("Public Key of A :" ,PUa)
            # print(f"Received reply: [ {message} ]")
            nonce_B = rand.randint(100,999)
            message =  str(nonce_A) + " "+ str(nonce_B)
            print(message)

            message = encrypt(PUa,message,n)
            message = json.dumps(message)
            # socket_UserB.recv()
            time.sleep(1)
            
            socket_UserB.send_string(message)
#  Socket to talk to server


PUa = 0
nonce_A = 0
PRb = 2453
# lock = threading.Lock()
user2_recv_thread = threading.Thread(target=listen, args=(PUa,PRb))
user2_recv_thread.start()
#  requesting server for User B public key
while True:
    
    print(f"Sending request …")
    request = input("Enter the request for the PKDA server : \
                                1) UserA \
                                2) UserB \
                                3) Connect with Other User \
                    : ")
    now = datetime.now()
    if request == '3':
        socket_UserA = context.socket(zmq.REQ)
        socket_UserA.connect("tcp://localhost:5566")
        nonce_B = rand.randint(100,999)
        message = input("Enter the Message you want to send UserA :")
        
        message = message + " " + str(nonce_B)
        # print(PUa)
        message = encrypt(PUa,message,n)
        message = json.dumps(message)
        socket_UserA.send_string(message)
        # print(message)
        time.sleep(1)
        message = socket_UserA.recv_string()
        message = json.loads(message)
        message = decrypt(PRb,message,n)
        print("Recieved Nonce 2 :",message)
        non = str(message.split()[-1])
        non = encrypt(PUa,non,n)
        non = json.dumps(non)
        socket_UserA.send_string(non)
        socket_UserA.recv_string()

    elif request == '2':
        print("Connecting to PKDA server…")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")
        current_time = now.strftime("%H:%M:%S")
        request = "UserB"+" "+str(current_time)
        print(request)
        socket.send_string(request)

    #  Get the reply.
        message = socket.recv_string()
        print(message)
        message = json.loads(message)
        message = decrypt(PKDA_PU_key,message,n)
        message = message.split()

        print(f"Received reply: [ {message} ]")
        s = 2
    elif request == '1':
        s=1
        print("Connecting to PKDA server…")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")
        current_time = now.strftime("%H:%M:%S")
        request = "UserA" +" "+str(current_time)
        print(request)
        socket.send_string(request)

    #  Get the reply.
        message = socket.recv_string()
        print(message)
        message = json.loads(message)
        message = decrypt(PKDA_PU_key,message,n)
        message = message.split()
        
        PUa = int(message[0])
        print(f"Received reply: [ {message} ]")
    # user2_recv_thread.join()
