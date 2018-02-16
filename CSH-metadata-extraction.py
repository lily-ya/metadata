#!/usr/bin/python3
####### Python Package #############
import os
from subprocess import call
from mongoengine import *
from pymongo import MongoClient
###### Auxiliary functions written by me ###########
import dbinfo
import extract_func


#build mongodb connection
mongoConn = MongoClient(dbinfo.dbServer + ":" + str(dbinfo.dbPort))
db = mongoConn[dbinfo.dbName]
db.authenticate( dbinfo.dbUser, dbinfo.dbPwd)
#If a collection does not exists, mongodb will automatically create a new one
my_collection = db[dbinfo.myCollection]


for root, dirs, files in os.walk(".", topdown=False):
    for filename in files:
        #print(os.path.join(root, name))
        if filename.endswith('.tif'):
            filename_full = os.path.join(root, filename)
            filename = os.path.splitext(filename)[0]
            print('Processing file %s' %filename_full)
            #ask mongodb if this tif file is already existed
            document = my_collection.find_one({"sourceResource.technical.fileName": filename})
            #print(document)
            # if this tif file doesn't exist, parse metadata and insert it to database
            if not document:
                #Store the output of technical metadata into a temporary text file
                metadata_file = filename + ".txt"
                os.system("identify -verbose " + filename_full + " >> " + metadata_file)
                #Use the extract_metadata function to extract metadata and arrange the output into JSON format
                new_document = extract_func.extract_metadata(metadata_file)
                #Delete the temporary text file
                os.system("rm " + metadata_file)
                #Insert the new_document into database
                post_id = my_collection.insert(new_document)
                #Check whether the insertion succeeds
                if not my_collection.find_one({"_id": post_id}):
                    print ('Insert document fail for %s' %filename)
                    exit()
                #else:
                #    print(my_collection.find_one({"_id": post_id}))
            else:
                print('Find file in the MongoDB. %s' %filename)             

