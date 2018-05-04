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

pb_conn,pb_addr=s.accept()
i_conn,i_addr=s.accept()
print pb_addr, i_addr

data = ""
payload_size = struct.calcsize("L")
next_seen = -2
cur_seen = 9999999
pb_queue = collections.deque()

def process(frame):
    print frame[2]

# Server end of dual-stream modified TCP.

# I stream. Read in the I frame and return
# the current time so the client can keep
# track of lag.
def i_stream(iframes):
    i_data = ""
    while True:
        # Read in streamed data
        start_time = time.time()
        data_len_start = len(i_data)
        while len(i_data) < payload_size:
            i_data += i_conn.recv(128)
        packed_msg_size = i_data[:payload_size]
        i_data = i_data[payload_size:]
        msg_size = struct.unpack_from("L", packed_msg_size)[0]
        while len(i_data) < msg_size:
            i_data += i_conn.recv(128)
        receipt_time = time.time()
        frame_data = i_data[:msg_size]
        i_data = i_data[msg_size:]

        # Get frame
        frame=cPickle.loads(frame_data)
        iframes.append(frame)
        i_conn.sendall(str(receipt_time - frame[0]))
        process(frame)

# P/B stream. Read in the P/B frame and return
# the current time so the client can keep
# track of lag. Don't process the P/B frame if
# we've seen a more recent I frame.
def pb_stream(iframes):
    pb_data = ""
    while True:
        while len(pb_data) < payload_size:
            pb_data += pb_conn.recv(128)
        packed_msg_size = pb_data[:payload_size]
        pb_data = pb_data[payload_size:]
        msg_size = struct.unpack_from("L", packed_msg_size)[0]
        while len(pb_data) < msg_size:
            pb_data += pb_conn.recv(128)
        receipt_time = time.time()
        frame_data = pb_data[:msg_size]
        pb_data = pb_data[msg_size:]

        # Get frame
        frame=cPickle.loads(frame_data)
        pb_conn.sendall(str(receipt_time - frame[0]))
        if frame[2] > iframes[-1][2]:
            process(frame)

# Set up two threads so the
# server can process both streams.
print('here')
i_frames = [0]
threads = []
i_thread = threading.Thread(target = i_stream, args=[i_frames])
pb_thread = threading.Thread(target = pb_stream, args=[i_frames])
threads.append(i_thread)
threads.append(pb_thread)
i_thread.start()
pb_thread.start()
