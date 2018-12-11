#!/usr/bin/env python 

from Crypto.Cipher import AES
from Crypto.Util import Counter
import binascii
from os import walk
import os


filename_list = []
path = os.path.dirname(os.path.realpath(__file__))

#print(path)

#path = "/encrypted_files"
#path = scriptpath + path

for(dirpath, dirnames, filenames) in walk(path):
    #print(filenames)
    filename_list.extend(filenames)

#print(filename_list)
#filename = "images/image6_enc.png"

for i in filename_list:
    if ".py" in i:
        continue
    if "_decrypted" in i:
        continue
    
    print(i)
    key = binascii.unhexlify("47683b9a9663c065353437b35c5d8519")
    f = open(i,'r')

    iv = int(binascii.hexlify(f.read(16)),16)
    ctr = Counter.new(128, initial_value=iv)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

    d = open(i[:-8] + "_decrypted" + i[-4:],'w+')

    data = f.read(16)
    
    while data:
	d.write(cipher.decrypt(data))
	data = f.read(16)

