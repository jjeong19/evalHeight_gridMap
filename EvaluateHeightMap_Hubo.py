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
parser.add_argument('--numObj', type=int, default = 1)
args = parser.parse_args()

RMSE_sum = np.zeros(args.numObj)

files = glob.glob(args.folder + "/*.npy")
files = sorted(files)
total_count = len(files)
RMSE_sum_count = 0

results_txt = open(args.folder + "/results.txt", "w")

r_obj = []
c_obj = []


for i in range(total_count):
    if not i % 15 == 0:
        continue
    print(files[i])
    results_txt.write(files[i] + "\n")
    sample = np.load(files[i])

    # if i == 0:
    plt.figure(figsize=(20,20))
    plt.imshow(sample,interpolation='none')
    plt.colorbar()

    print("Enter values for ground plane:")
    points = plt.ginput(0)
    plt.close()
    points = np.array(points)
    if points.size == 0:
        continue
    r_ground, c_ground  = polygon(points[:,0], points[:,1])
        # [row_s, col_s] = np.rint([points[0][0], points[0][1]]).astype(np.uint16)
        # [row_e, col_e] = np.rint([points[1][0], points[1][1]]).astype(np.uint16)

    data = np.array([c_ground, r_ground, sample[c_ground,r_ground].flatten()]).T
    data = data[np.invert(np.isnan(data[:,2]))]

    X_train = data[:,:2]
    y_train = data[:,2]

    ransac = linear_model.RANSACRegressor(residual_threshold=0.0005, max_trials=10000)
    ransac.fit(X_train, y_train)

    a, b = ransac.estimator_.coef_
    d = ransac.estimator_.intercept_

    # a, b, d = C
#     print(a, b, d)

    X,Y = np.meshgrid(np.arange(0, 200, 1), np.arange(0, 200, 1))
    XX = X.flatten()
    YY = Y.flatten()
    data = np.array([XX, YY, sample.flatten()]).T


#     print (data)
    d = abs((a * data[:,0] + b * data[:,1] + -1 * data[:,2] + d))
    e = np.sqrt(a*a + b*b + 1)
#     print(data)
    height = d/e
#     print(height)

    # plt.imshow(np.reshape(height, (200, 200)), vmax=0.50)
    # plt.colorbar()
    # plt.pause(0.5)
    # plt.close()

    # if i == 0:
    while points.size != 0:
        plt.figure(figsize=(20,20))
        plt.imshow(np.reshape(height, (200, 200)), vmax=0.50)
        plt.colorbar()
        print("Enter values for ground plane:")
        points = plt.ginput(0)
        points = np.array(points)
        if points.size == 0:
            break
        plt.close()
        # pdb.set_trace()
        GT_txt = str(input("Type height GT, idx of obj: "))
        GT_idx_pair = GT_txt.split(",")
        GT_idx_pair = [int(x) for x in GT_idx_pair]
        obj_height = GT_idx_pair[0]
        idxObj = GT_idx_pair[1]

        r, c  = polygon(points[:,0], points[:,1])
        # r_obj.append(r)
        # c_obj.append(c)
        pdb.set_trace()
        target_array = np.reshape(height, (200, 200))[c, r]*100
        # print(target_array)
        target_bool = np.invert(np.isnan(target_array))
        target_array = target_array[target_bool]
        c = c[target_bool]
        r = r[target_bool]
        # print(target_array)
        target_array_bool = (target_array < obj_height + 10) * (target_array > obj_height - 10)
        target_array = target_array[target_array_bool]
        r = r[target_array_bool]
        c = c[target_array_bool]
        print(target_array)
        
        # if obj_distance[0] == 0:
        # pdb.set_trace()
        RMSE = np.sqrt(np.sum(((target_array-obj_height)/ (0.02*np.sqrt((c-100)**2 + (r-100)**2)))**2)/np.count_nonzero(target_array))
        # 2 is to multiple the resolution 2cm
        print(np.min((0.02*np.sqrt((c-100)**2 + (r-100)**2))))
        # else:
        #     # pdb.set_trace()
        #     RMSE = np.sqrt(np.sum((target_array-obj_height[idxObj])**2)/np.count_nonzero(target_array))
        #     RMSE = RMSE / obj_distance[idxObj]
        # print(target_array)
        print(RMSE)
        print("----------")
        results_txt.write(str(RMSE) + "\n")
        results_txt.write("----------" + "\n")
        if np.invert(np.isnan(RMSE)):
            RMSE_sum[idxObj] += RMSE**2
            RMSE_sum_count += 1

for idxObj in range(args.numObj):
    print("Final RMSE:")
    print(np.sqrt(RMSE_sum[idxObj]/RMSE_sum_count))
    results_txt.write("Final RMSE:\n")
    results_txt.write(str(np.sqrt(RMSE_sum[idxObj]/RMSE_sum_count)) + "\n")

