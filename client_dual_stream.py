from multiprocessing import Process
import threading
import cv2
import numpy as np
import socket
import sys
import pickle
import cPickle
import json
import math
import struct
import pandas as pd
import math
import time

# Set up socket
vid = '6'
cap = cv2.VideoCapture('dataset/' + vid + '.avi')
pb_clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
pb_clientsocket.connect(('localhost',8089))
i_clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
i_clientsocket.connect(('localhost',8089))
first_frame_seen = False
caplen = 200

# Read in all the frames and
# set up dictionaries/lists to access
# information about the type of frame
# (I vs P/B frame).
def get_frames():
    frames = []
    for i in range(caplen):
        ret, frame = cap.read()
        frames.append(frame)
    return frames

frames = get_frames()
assert(len(frames) == caplen)
df = pd.read_excel('dataset/' + vid + 'frames.xlsx')
pre_cleaned_i_indices = list(df['I'])
pre_cleaned_pb_indices = list(df['PB'])

i_indices = []
for i in range(len(pre_cleaned_i_indices)):
    if not math.isnan(pre_cleaned_i_indices[i]):
        i_indices.append(int(pre_cleaned_i_indices[i]))
print i_indices
pb_indices = []
for i in range(len(pre_cleaned_pb_indices)):
    if not math.isnan(pre_cleaned_pb_indices[i]):
        pb_indices.append(int(pre_cleaned_pb_indices[i]))

pb_after_i = {}
for i in range(caplen):
    if i in i_indices:
        pb = -1
        for j in range(i+1, caplen):
            if j in pb_indices:
                pb = j
                break
        pb_after_i[i] = pb

global_index_to_pb_index = {}
for i in range(caplen):
    for j in range(len(pb_indices)):
        if i == pb_indices[j]:
            global_index_to_pb_index[i] = j

# Collect the data that will be streamed
raw_data = []
for i in range(len(frames)):
    size = sys.getsizeof(frames[i])

    # first element 1 means I frame
    # first element 2 means P/B frame
    if i in i_indices:
        data_pt = [1]
        for j in range(i+1, len(frames)):
            if j in i_indices:
                data_pt.append(j)
                break
        if len(data_pt) == 1: data_pt.append(-1)
    else:
        data_pt = [2, -1]

    # make our data_pt the same size as a video frame
    while sys.getsizeof(data_pt) < size:
        data_pt.append(i)
    data_pt = data_pt[:-1]

    print(sys.getsizeof(data_pt), sys.getsizeof(frames[i]))
    raw_data.append(data_pt)

# Modified dual-stream TCP client.
# Stream the frames as they come in;
# If our stream is significantly behind
# real-time (as measured by lags returned from server)
# and the current frame is a P/B frame, skip the frame.
# Stream the I frames via the I socket and the
# P/B frames via the P/B scoket.
def stream():
    lag = 0.0
    threshold = 0.33
    for i in range(caplen):
        print i, lag
        new_frame_processing_start_time = time.time()
        if i in i_indices:
            raw_data[i][0] = new_frame_processing_start_time
            data = cPickle.dumps(raw_data[i])
            i_clientsocket.sendall(struct.pack("L", len(data))+data)
            msg = i_clientsocket.recv(64)
            lag += float(msg)
        else:
            if lag > threshold:
                lag = max(lag - 1.0/15, 0)
                continue
            raw_data[i][0] = new_frame_processing_start_time
            data = cPickle.dumps(raw_data[i])
            pb_clientsocket.sendall(struct.pack("L", len(data))+data)
            msg = pb_clientsocket.recv(64)
            lag += float(msg)

print('here')
stream()
