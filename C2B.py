#coding=utf-8

# 通过bin2Hex


import struct
import os
import sys
import re


#打开文件



readfile = open("UI.c")
binfile = open("UI.bin", 'wb')

list = re.findall(r"(?:0X|0x|0a)(\w\w)",readfile.read())
print(list)

for j in list:
    binfile.write(int(j, 16).to_bytes(1, byteorder='big'))



# list = ['0f', '10'];
# print(int(list[0],16).to_bytes(1,byteorder='big'))
# binfile = open('test.bin', 'wb')
# binfile.write(int(list[0],16).to_bytes(1,byteorder='big'))



