import numpy as np
import argparse
import scipy.linalg
from mpl_toolkits.mplot3d import Axes3D
from skimage.draw import polygon
import matplotlib.pyplot as plt
import glob
from sklearn import datasets, linear_model
import pdb
import time

parser = argparse.ArgumentParser()
parser.add_argument('--folder', default = "")
args = parser.parse_args()

files = glob.glob(args.folder + "/*.npy")
files = sorted(files)
total_count = len(files)
RMSE_sum_count = 0


for i in range(total_count):
    if not i % 3 == 0:
        continue
    print(files[i])
    sample = np.load(files[i])

    plt.figure(figsize=(20,20))
    plt.imshow(sample,interpolation='none')    
    plt.colorbar()
    plt.show(block=False)
    plt.pause(0.2)
    plt.close()