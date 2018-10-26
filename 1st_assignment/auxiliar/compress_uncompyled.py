# uncompyle6 version 3.2.3
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.15 (default, Jul 28 2018, 11:29:29) 
# [GCC 8.1.0]
# Embedded file name: csfsteg/csfsteghide.py
# Compiled at: 2018-10-13 10:57:39
import sys, struct, numpy, PIL as pillow
from PIL import Image

def decompose(data):
    v = []
    fSize = len(data)
    bytes = [ ord(b) for b in struct.pack('i', fSize) ]
    bytes += [ ord(b) for b in data ]
    for b in bytes:
        for i in range(7, -1, -1):
            v.append(b >> i & 1)

    return v


def set_bit(n, i, x):
    mask = 1 << i
    n &= ~mask
    if x:
        n |= mask
    return n


def embed(imgFile, payload, password):
    img = Image.open(imgFile)
    width, height = img.size
    conv = img.convert('RGBA').getdata()
    print '[*] Input image size: %dx%d pixels.' % (width, height)
    max_size = width * height * 3.0 / 8 / 1024
    print '[*] Usable payload size: %.2f KB.' % max_size
    f = open(payload, 'rb')
    data = f.read()
    f.close()
    print '[+] Payload size: %.3f KB ' % (len(data) / 1024.0)
    v = decompose(data)
    while len(v) % 6:
        v.append(0)

    payload_size = len(v) / 8 / 1024.0
    print '[+] Embedded payload size: %.3f KB ' % payload_size
    if payload_size > max_size - 4:
        print '[-] Cannot embed. File too large'
        sys.exit()
    steg_img = Image.new('RGBA', (width, height))
    data_img = steg_img.getdata()
    idx = 0
    displacement = 0
    for h in range(height):
        for w in range(width):
            if displacement < password:
                displacement = displacement + 1
                continue
            r, g, b, a = conv.getpixel((w, h))
            if idx < len(v):
                r = set_bit(r, 0, v[idx])
                r = set_bit(r, 1, v[idx + 1])
                g = set_bit(g, 0, v[idx + 2])
                g = set_bit(g, 1, v[idx + 3])
                b = set_bit(b, 0, v[idx + 4])
                b = set_bit(b, 1, v[idx + 5])
            idx = idx + 6
            data_img.putpixel((w, h), (r, g, b, a))

    steg_img.save(imgFile + '-stego.png', 'PNG')
    print '[+] %s embedded successfully!' % payload


def usage(progName):
    print 'Ciber Securanca Forense - Instituto Superior Tecnico / Universidade Lisboa'
    print 'LSB steganography tool: hide files within least significant bits of images.\n'
    print ''
    print 'Usage:'
    print '  %s <img_file> <payload_file> [password]' % progName
    print ''
    print '  The password is optional and must be a number.'
    sys.exit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage(sys.argv[0])
    password = int(sys.argv[3]) % 13 if len(sys.argv) > 3 else 0
    embed(sys.argv[1], sys.argv[2], password)
# okay decompiling compress.pyc
