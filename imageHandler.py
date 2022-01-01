import os
import base64

def imagedecode(data,fpath):
    '''Decodes image from base64 and stores it in path as image file'''
    try:
        with open(fpath, "wb") as fimage:
            #fimage.write(base64.decodebytes(data))
            fimage.write(data)
    except Exception as e:
        raise Exception("Failed to decode image.\n" + str(e))

def imagecode(fpath):
    '''Encodes image from path and returns as base64 string'''
    try:
        with open(fpath, "rb") as imageFile:
            i = base64.b64encode(imageFile.read())
            return(i)
    except Exception as e:
        raise Exception("Failed to encode image.\n" + str(e))



