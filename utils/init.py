# create a folder call src if not exist 
import os

folder = ["src","media/images"]

for i in folder:
    if not os.path.exists(i):
        os.makedirs(i)
