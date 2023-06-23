import numpy as np
import os
import matplotlib.pyplot as plt
import glob

def sobel_average(files, output_file):
    # Loop through all .npy files in the directory
    #files = glob.glob(os.path.join(input_dir, '**', '*.npy'), recursive=True)

    # Initialize arrays to store Sobel-filtered images and white pixel coordinates
    X_sobel_list = []
    Y_white_pixels_list = []

    for file in files:
        # Load X and Y images
        X = np.load(file,allow_pickle=True)
        X = (2 * (X - X.min()) / (X.max() - X.min())) - 1  #between -1 and 1
        Y = np.load(file.replace('X.npy', 'Yp.npy'))

        # Apply Sobel filter to X image
        X_sobel = np.abs(np.gradient(X.astype(np.float32), axis=0)) + np.abs(np.gradient(X.astype(np.float32), axis=1))
        X_sobel_list.append(X_sobel)

        # Find white pixels in Y image
        Y_white_pixels = np.argwhere(Y == 1)
        Y_white_pixels_list.append(Y_white_pixels)

    # Combine X_sobel and Y_white_pixels (boundary) into one array of tuples
    XY_tuples = list(zip(X_sobel_list, Y_white_pixels_list))

    # Compute average Sobel values for white pixels in each image
    averages = []
    
    for xy in XY_tuples:
        X_sobel = xy[0]
        Y_white_pixels = xy[1]
        if len(Y_white_pixels) > 0:
            averages.append(np.mean(X_sobel[Y_white_pixels[:, 0], Y_white_pixels[:, 1]]))

    # Write averages to output file
    # print(np.mean(averages),np.std(averages))
    # plt.hist(averages, bins=20)
    # plt.show()
    # target_mean = 120
    # current_mean = sum(averages) / len(averages)
    # while current_mean < target_mean:
    #     min_index = averages.index(min(averages))
    #     del averages[min_index]
    #     del files[min_index]
    #     current_mean = sum(averages) / len(averages)
    print(len(files),averages)
    # with open(output_file, 'w') as f:
    #     for file in files:
    #         f.write(file + '\n')



files = glob.glob(os.path.join('./files', '**', '0*', '*X.npy'), recursive=True) + glob.glob(os.path.join('./files', '**', '[!0]*', '*X.npy'), recursive=True)
#files = ["./files/0081_0001/LPA_36/260.X.npy"]
# Example usage
sobel_average(files, 'output120.txt')
