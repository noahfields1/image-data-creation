import os
import Model_class
import util

"""
This is the main file to run.
We assume that the models are stored in the './models' directory.
"""
util.create_directories("./models")
#print("1")
util.create_images()
#print("2")
util.summary()
