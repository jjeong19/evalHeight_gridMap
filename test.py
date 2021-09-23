import numpy as np
import matplotlib.pyplot as plt
import time
import rosbag
import argparse
#from grid_map_msg.msg import GridMap
import pdb
import os
import matplotlib.pyplot as plt
import glob

sample = np.load("data_0824/circle50cm_d30cm_2021-08-24-16-27-55/50.npy")
plt.figure(figsize=(20,20))
plt.imshow(sample,interpolation='none')
plt.colorbar()
plt.show()
name = "data_0824/circle50cm_d30cm_2021-08-24-16-27-55.bag"

bag = rosbag.Bag(name)
for topic, msg, t in bag.read_messages(topics = "/elevation_mapping_light/elevation_map_raw"):
    print(1)
    # pdb.set_trace()
    seq_no = msg.info.header.seq
    a = np.array(msg.data)
    #print(msg.deserialize_numpy())
    row = msg.outer_start_index
    col = msg.inner_start_index
    col_size = a[0].layout.dim[0].size
    row_size = a[0].layout.dim[1].size
    
    if(col > 100):
        col = 200 - col


    b = np.array(a[0].data) #we only use the first layer since its the elevation layer, all others are variance, timestamp etc.,
    print(b.shape)
    offset = row + col*row_size
    b = b[offset::]
    c = np.empty((40000))
    c[:] = np.nan
    print(c.shape)
    c[0:-offset] = b
    c = c.reshape(200,200)

    if not os.path.exists(name[:-4]):
        os.makedirs(name[:-4])
    np.save(name[:-4] + "/" + str(seq_no) + ".npy", c)
#pdb.set_trace()

bag.close()