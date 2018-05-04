import socket
import sys
import pickle
import cPickle
import numpy as np
import struct
import json
import collections
import signal
import time
from multiprocessing import Process
import threading

# Set up the socket
HOST=''
PORT=8089

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = ""
payload_size = struct.calcsize("L")
next_seen = -2
cur_seen = 9999999
pb_queue = collections.deque()

def process(frame):
    print frame[2]

# Server end of the stream. Read in
# the frame and return the current time
# to the client so that it can
# keep track of the lag.
def stream(iframes):
    data = ""
    while True:
        while len(data) < payload_size:
            data += conn.recv(128)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack_from("L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += conn.recv(128)
        receipt_time = time.time()
        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Get frame
        frame=cPickle.loads(frame_data)
        conn.sendall(str(receipt_time - frame[1]))
        if frame[0] == 1:
            process(frame)
            iframes.append(frame)
        elif frame[2] > iframes[-1][2]:
            process(frame)
        #pb_conn.sendall(str(frame[1]) + str('.'))

print('here')
i_frames = [0]
stream(i_frames)
