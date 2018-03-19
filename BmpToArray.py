import os
import numpy as np
from PIL import Image

# 1. 文件信息头
# 2. 位图信息头
# 3. 调色板
# 4. 像素信息

# 文件信息头
class BmpFileHeader:
    def __init__(self):
        self.bfType = i_to_bytes(0, 2)  # 0x4d42 对应BMP
        self.bfSize = i_to_bytes(0, 4)  # file size
        self.bfReserved1 = i_to_bytes(0, 2)
        self.bfReserved2 = i_to_bytes(0, 2)
        self.bfOffBits = i_to_bytes(0, 4)  # header info offset

# BMP信息头
class BmpStructHeader:
    def __init__(self):
        self.biSize = i_to_bytes(0, 4)  # bmpheader size
        self.biWidth = i_to_bytes(0, 4)
        self.biHeight = i_to_bytes(0, 4)
        self.biPlanes = i_to_bytes(0, 2)  # default 1
        self.biBitCount = i_to_bytes(0, 2)  # one pixel occupy how many bits
        self.biCompression = i_to_bytes(0, 4)
        self.biSizeImage = i_to_bytes(0, 4)
        self.biXPelsPerMeter = i_to_bytes(0, 4)
        self.biYPelsPerMeter = i_to_bytes(0, 4)
        self.biClrUsed = i_to_bytes(0, 4)
        self.biClrImportant = i_to_bytes(0, 4)

# BMP类
class Bmp(BmpFileHeader, BmpStructHeader):
    def __init__(self):
        BmpFileHeader.__init__(self)
        BmpStructHeader.__init__(self)
        self.__bitSize = 0  # pixels size
        self.bits = []  # pixel array

    @property
    def width(self):
        return bytes_to_i(self.biWidth)

    @property
    def height(self):
        return bytes_to_i(self.biHeight)

    # unit is byte
    @property
    def bit_count(self):
        return bytes_to_i(self.biBitCount) // 8

    @property
    def width_step(self):
        return self.bit_count * self.width

# load BMP文件
def load_bmp(self, file_name):
    # BmpFileHeader
    self.bfType = file.read(2)
    self.bfSize = file.read(4)
    self.bfReserved1 = file.read(2)
    self.bfReserved2 = file.read(2)
    self.bfOffBits = file.read(4)
    # BmpStructHeader
    self.biSize = file.read(4)
    self.biWidth = file.read(4)
    self.biHeight = file.read(4)
    self.biPlanes = file.read(2)
    self.biBitCount = file.read(2)
    # pixel size
    self.__bitSize = (int.from_bytes(self.bfSize,
                                     'little') -
                      int.from_bytes(self.bfOffBits, 'little')) \
                     // (int.from_bytes(self.biBitCount, 'little') // 8)
    self.biCompression = file.read(4)
    self.biSizeImage = file.read(4)
    self.biXPelsPerMeter = file.read(4)
    self.biYPelsPerMeter = file.read(4)
    self.biClrUsed = file.read(4)
    self.biClrImportant = file.read(4)
    #  load pixel info
    count = 0
    while count < self.__bitSize:
        bit_count = 0
        while bit_count < (int.from_bytes(self.biBitCount, 'little') // 8):
            self.bits.append(file.read(1))
            bit_count += 1
        count += 1
    file.close()


file = open("pic/number_0.bmp", 'rb')
print(file.read())

# load_bmp("pic/numnber_0.bmp");