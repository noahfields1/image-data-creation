import os
import numpy as np
import util

#Determine if a vessel is circular enough (arbitrary, but good threshold of 0.75)
def is_non_circular_vessel(image_data, threshold=0.75):
    # Compute the eccentricity of the binary image
    white_pixels = np.where(image_data == 1)
    if len(white_pixels[0]) == 0:
        return False
    centroid_x = np.mean(white_pixels[0])
    centroid_y = np.mean(white_pixels[1])
    distance = np.sqrt((white_pixels[0] - centroid_x)**2 + (white_pixels[1] - centroid_y)**2)
    semi_major_axis = np.max(distance)
    semi_minor_axis = np.min(distance)
    eccentricity = np.sqrt(1 - (semi_minor_axis / semi_major_axis)**2)

    # Check if the eccentricity exceeds the threshold
    return eccentricity > threshold

def find_circular_vessels():
    i = 0
    circular_vessels = []
    non_circular_vessels = []
    files = util.find_files_with_suffix("Yp.npy")
    for filename in files:
        if i % 10000 == 0:
            print(str(i) + "/" + str(len(files)))
        image_data = np.load(filename)
        if is_non_circular_vessel(image_data):
            non_circular_vessels.append(filename.replace('Yp.npy',''))
        else:
            circular_vessels.append(filename.replace('Yp.npy',''))
        i += 1
    return circular_vessels,non_circular_vessels

#Filter the images to make sure the gradient (sobel filter) is high enough
def filter_sobel(files,gradient_threshold=0.2):
    # Initialize arrays to store Sobel-filtered images and white pixel coordinates
    X_sobel_list = []
    Y_white_pixels_list = []
    #f = open("/Users/noah/Desktop/gradients.txt","w")
    for file in files:
        # Load X and Y images
        X = np.load(file + 'X.npy',allow_pickle=True)
        if X.max() != X.min():
            X = (2 * (X - X.min()) / (X.max() - X.min())) - 1  #between -1 and 1
        Y = np.load(file + 'Yp.npy')

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

    #Deleting images that are no good (low-threshold)
    store_indices = []
    for index,grad in enumerate(averages):
        if grad < gradient_threshold:
            store_indices.append(index)

    new_files = [elem for index, elem in enumerate(files) if index not in store_indices]


    return new_files

def filter():
    # Example usage
    circular_vessels,non_circular_vessels = find_circular_vessels()
    clear_circular_vessels = filter_sobel(circular_vessels)
    clear_circular_vessels_yaml = util.add_file_extensions(clear_circular_vessels,"yaml")
    output_file = "files_clean.txt"
    util.write_array_to_file(clear_circular_vessels_yaml, output_file)
    




