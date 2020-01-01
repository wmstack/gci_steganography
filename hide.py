#!/usr/bin/env python3

#the magic is added to the beginning of the text to verify that LSB is not random
MAGIC = "GCISTEG"

import argparse
import sys

#editing filenames
from os.path import basename, splitext

from PIL import Image

#numpy to represent image as array
#to do pixel manipulation
import numpy as np

def parse_args():
    
    parser = argparse.ArgumentParser(
        description='Hide text inside a file using steganography(LSB)'
    )

    #one of -e or -d option must be picked
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e','--encode',action='store_const',const=True,default=False,
        help='hide text in image')
    group.add_argument('-d','--decode',action='store_const',const=True,default=False,
        help='get text hidden in image')
    
    #image path
    parser.add_argument('image',metavar='path_to_image',type=str)

    args = parser.parse_args()
    return args

def steg_hide(text, flat_image):

    #add magic header before the text and null to indicate end of the text.
    text_bytes = (MAGIC + text + '\0').encode('utf-8')
    
    #check if text can fit in the image
    if len(text_bytes)*8 > flat_image.size:
        print('Text file too big to embed in image')
        sys.exit(1)

    #loop through the bytes in text_bytes
    for i,text_byte in enumerate(text_bytes):

        #loop through bits in the i-th byte of text_bytes
        for j in range(8):
            # get jth bit from the left
            text_bit = ( text_byte >> (7-j) ) & 1
            #set the LSB of np_image_flat to the bit
            flat_image[8*i+j] = (flat_image[8*i+j] & -2) | text_bit

def steg_show(image):
    
    #container for bytes
    text_bytes = bytearray()

    for i in range(0,image.size,8):

        byte_builder = 0

        #loop through all bits and build the byte
        for j in range(8):

            #shift left and add the corresponding bit
            byte_builder = (byte_builder<<1) + (image[i+j] & 1)
        
        #if found null character stop
        if byte_builder==0:
            break

        text_bytes.extend(bytes([byte_builder]))
    
    try:
        text=text_bytes.decode('utf-8')
    except:
        print('Text not found in image.')
        sys.exit(1)
        
    if text.startswith(MAGIC):
        #remove MAGIC from beginning
        text = text[len(MAGIC):]
        print('The hidden text is :', text)
    else:
        print('Text not found in image')

def main():

    args = parse_args()
    
    base = basename(args.image)
    filename, extension = splitext(base)
    
    #open the file args.image
    try:
        image = Image.open(args.image)
    except FileNotFoundError:
        print('File is not found')
    except PermissionError:
        print('No permission')

    #turn image into flat numpy array
    np_image = np.asarray(image)
    np_image_flat= np_image.flatten()
    
    if args.encode:
        
        #prompt the user for input
        text = input('Text to hide in image: ')
        
        steg_hide(text, np_image_flat)
        
        #saving the image
        new_image = np_image_flat.reshape(np_image.shape)
        pil_new_image = Image.fromarray(new_image)
        pil_new_image.save(filename+'.new'+'.png',quality=100)

        print('Sucessfully hidden text in file!')      
    else:
        steg_show(np_image_flat)

if __name__ == '__main__':
    main()
