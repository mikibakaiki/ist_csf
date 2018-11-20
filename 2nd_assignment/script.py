from Crypto.Cipher import AES
from Crypto.Util import Counter
import binascii
from os import walk



filename_list = []
path = "/encrypted_files"

for(dirpath, dirnames, filenames) in walk(path):
    filename_list.extend(filenames)

#filename = "images/image6_enc.png"

for i in filename_list:

    key = binascii.unhexlify("47683b9a9663c065353437b35c5d8519")
    f = open(i,'r')

    iv = int(binascii.hexlify(f.read(16)),16)
    ctr = Counter.new(128, initial_value=iv)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

    d = open(i[:-8] + "_decrypted" + s[-4:],'w+')

    data = f.read(16)
    
    while data:
	d.write(cipher.decrypt(data))
	data = f.read(16)

