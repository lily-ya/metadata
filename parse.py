#!/usr/bin/python3
import os
from subprocess import call

# Gather metadata from tiff files and save metadata in the metadata_dir
def gather_metadata( metadata_dir):
    if not os.path.exists(metadata_dir):
        os.makedirs(metadata_dir)

    for root, dirs, files in os.walk(".", topdown=False):
        for filename in files:
            #print(os.path.join(root, name))
            if filename.endswith('.tif'):
                print(filename)
                filename_full = os.path.join(root, filename)
                output_name = os.path.splitext(filename)[0] + ".txt"
                output_name = metadata_dir + '/' + output_name
                output = open(output_name,'w')
                output.write('Path: %s' %(filename_full));
                output.close()
                #return_code = call("identify -verbose " + name + " >> " + output_name)
                os.system("identify -verbose " + filename_full + " >> " + output_name)
           

########main################
metadata_dir = "metadata"
gather_metadata(metadata_dir);

