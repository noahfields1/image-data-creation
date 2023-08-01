import os
import Model_class
import util
import tidy

#Removes all unneseccary files
# os.system("find ./ -type d -name 'Simulations' -exec rm -r {} +")
# os.system("find ./ -type d -name 'Segmentations' -exec rm -r {} +")
# os.system("find ./ -type d -name 'flow-files' -exec rm -r {} +")

"""
This is the main file to run.
We assume that the models are stored in the './models' directory.
"""
util.create_directories("./models")
util.create_images()

#This creates files which will be used for filtering images and displaying them
os.system("python3 perimeter.py") #This file creates a file with just the perimeter outlined
os.system("python3 Xo.py") #This file creates a 'Xo' file with the perimeter overlayed on top of the original image.

#Filtering to only include good photos
tidy.filter()


#util.write_files_txt("./files")
#util.summary()

#This is meant to remove some of the files that would take up lots of storage
os.system("find ./ -name '.DS_Store' -type f -delete")
# os.system("find results/ -type f -delete")
# os.system("find 3D_points/ -type f -delete")

