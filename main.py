import os
import Model_class
import util

#Removes all unneseccary files
# os.system("find ./ -type d -name 'Simulations' -exec rm -r {} +")
# os.system("find ./ -type d -name 'Segmentations' -exec rm -r {} +")
# os.system("find ./ -type d -name 'flow-files' -exec rm -r {} +")

"""
This is the main file to run.
We assume that the models are stored in the './models' directory.
"""
#util.create_directories("./models")
#util.create_images()
util.write_files_txt("./files")
util.summary()

os.system("find ./ -name '.DS_Store' -type f -delete")
#os.system("find results/ -type f -delete")
#os.system("find 3D_points/ -type f -delete")

