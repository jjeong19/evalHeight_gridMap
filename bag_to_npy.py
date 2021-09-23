import rosbag
import argparse
#from grid_map_msg.msg import GridMap
import numpy as np
import pdb
import os
import matplotlib.pyplot as plt
import glob

parser = argparse.ArgumentParser(description = "Parser for file name input")

parser.add_argument('--dir', default = "")
args = parser.parse_args()

files = glob.glob(args.dir + "*.bag")
files = sorted(files)

for name in files:
    bag = rosbag.Bag(name)
    for topic, msg, t in bag.read_messages(topics = "/elevation_mapping_light/elevation_map_raw"):
        print(1)
        seq_no = msg.info.header.seq
        a = np.array(msg.data)
        #print(msg.deserialize_numpy())
        row = msg.outer_start_index
        col = msg.inner_start_index
        col_size = a[0].layout.dim[0].size
        row_size = a[0].layout.dim[1].size
        
        b = np.array(a[0].data) #we only use the first layer since its the elevation layer, all others are variance, timestamp etc.,
        print(b.shape)
        offset = row + col*row_size
        print(offset)
        b_offset = b[offset::]
        c = np.empty((40000))
        c[:] = np.nan
        print(c.shape)
        c[0:-offset] = b_offset
        c[-offset::] = b[0:offset]
        c = c.reshape(200,200)

        if not os.path.exists(name[:-4]):
            os.makedirs(name[:-4])
        np.save(name[:-4] + "/" + str(seq_no) + ".npy", c)
    #pdb.set_trace()

    bag.close()

