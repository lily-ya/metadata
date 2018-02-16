#!/usr/bin/python3
import os
from subprocess import call
import re
import json

def extract_metadata(metadata_file):
    #f=open("01_37_0001.txt")
    f = open(metadata_file)
    #print('Filename: %s' %metadata_file)
    for line in f:
        if "Geometry" in line:
            numbers = []
            for num in re.findall('[0-9]*',line):
                if num.isdigit():
                    numbers.append(num)
            imageWidth=int(numbers[0])
            imageLength=int(numbers[1])
            #print ('imageWidth: %d' %imageWidth)
            #print ('imageLength: %d' %imageLength)
            
        elif "Compression" in line:
            words = line.split(':')
            compression = words[1].rstrip()
            #print ('compression :%s' %compression)

        elif "tiff:photometric" in line:
            words = line.split(':')
            photometric = words[2].rstrip()
            #print ('Photometrics :%s' %photometric)
     
        elif "Channel depth" in line: ##TODO:further discussion
            red_line = f.next()        
            if "red" in red_line:
                samplesPerPixel="RGB"
                bitsPerSample="8 8 8"
            else:
                samplesPerPixel="GrayScale"
                bitsPerSample="8"

        elif "Resolution" in line: 
            numbers = []
            for num in re.findall('[0-9]*',line):
                if num.isdigit():
                    numbers.append(num)
            xresolution=int(numbers[0])
            yresolution=int(numbers[1])
            #print ('Xresolution: %d' %xresolution)
            #print ('Yresolution: %d' %yresolution)

        elif "Units" in line:
            words = line.split("Per")
            units = words[1].rstrip()
            #print ('ResolutionUnit: %s' %units)

        elif "tiff:timestamp" in line:
            words = line.split("timestamp:")
            datetime = words[1].rstrip()
            #print ('Datetime: %s' %datetime)
             
        elif "Colorspace" in line: 
            words = line.split(':')
            colorspace = words[1].rstrip()
            #print ('ColorSpace: %s' %colorspace)

        elif "tiff:software" in line: 
            words = line.split('software:')
            software = words[1].rstrip()
            #print ('Software: %s' %software)

        #elif "Manufacturer" in line: 
        #    words = line.split(':')
        #    manufacturer = words[1].rstrip()
        #    #print ('Manufacturer: %s' %manufacturer)

        elif "tiff:artist" in line: 
            words = line.split('artist:')
            artist = words[1].rstrip()
            #print ('Make: %s' %artist)

        elif "Model" in line: 
            words = line.split(':')
            model = words[1].rstrip()
            #print ('Model: %s' %model)

        elif "Filesize" in line: 
            words = line.split(':')
            size = words[1].rstrip()
            #print ('File size: %s' %size)

        elif "Format" in line: 
            words = line.split(':')
            _format = (words[1].split('('))[0].rstrip()
            #print ('Format: %s' %_format)

        elif "Version" in line: 
            words = line.split('Version:')
            version = words[1].rstrip()
            #print ('Version: %s' %version)

        #elif "Copyright" in line: 
        #    words = line.split(':')
        #    copyright = words[1].rstrip()
        #    #print ('Copyright: %s' %copyright)
    #document'{"ImageWidth":"%d","ImageLength":"%d"}' %(imageWidth,imageLength)
    document= dict()
    document['sourceResource']= {}
    document['sourceResource']['technical'] = {}
    document['sourceResource']['technical']['imageLength'] = imageLength
    document['sourceResource']['technical']['imageWidth'] = imageWidth
    document['sourceResource']['technical']['compression'] = compression
    document['sourceResource']['technical']['photometricInterpretation'] = photometric
    document['sourceResource']['technical']['samplesPerPixel'] = samplesPerPixel 
    document['sourceResource']['technical']['bitsPerSample'] = bitsPerSample
    document['sourceResource']['technical']['xResolution'] = xresolution
    document['sourceResource']['technical']['yResolution'] = yresolution
    document['sourceResource']['technical']['resolutionUnit'] = units
    document['sourceResource']['technical']['dateTime'] = datetime
    document['sourceResource']['technical']['colorSpace'] = colorspace
    document['sourceResource']['technical']['software'] = software
    document['sourceResource']['technical']['make'] = artist
    document['sourceResource']['technical']['model'] = model
    document['sourceResource']['technical']['fileSize'] = size
    document['sourceResource']['technical']['encodingFormat'] = _format
    document['sourceResource']['technical']['fileName'] = os.path.splitext(metadata_file)[0]
    document['sourceResource']['technical']['version'] = version 
    json_str = json.dumps(document)
    #type(json_str)
    print json_str
    return document
##########################################################
metadata_file="01_37_0001.txt"
extract_metadata(metadata_file)
