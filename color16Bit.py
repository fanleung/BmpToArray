from PIL import Image
import sys
import os

# 取高位的数据

# 需要用到的中间变量
DataArray = []  # 每个图片的数组
DataLength = 0  # 数组的长度
DataIndex = 0   # 数组的当前写坐标
temp = 0        # 一个字节


# 输出文件
if os.path.exists("array.txt"):
  os.remove("array.txt")
outfile = open("array.txt", "w")

# 读取文件
file_path = r"color/"
dirs = os.listdir(file_path)
for i in dirs:
    DataIndex = 0
    if os.path.splitext(i)[1] == ".bmp":
        # 打开文件
        filename = os.path.splitext(i)[0]
        fileType = ".bmp"
        img=Image.open(file_path + filename + fileType)
        print(file_path + filename + fileType)

        # 读取文件信息
        width=img.size[0]
        height=img.size[1]
        DataLength = width * height * 2
        row = width // 8 + 1
        print("实际宽，高:" , width,",", height)
        print("数组大小:", DataLength)

        # 实际数据宽度（即要加上补零的位数）
        w_ = (width // 8 + 1) * 8
        # print(w_)

        for h in range(height):
            for w in range(width):
                pixel = img.getpixel((w, h))

                temp = (pixel[0] & 0xF8) | ((pixel[1] & 0xE0) >> 5)  #高5 + 高3
                DataArray.insert(DataIndex, temp)
                DataIndex += 1

                temp = ((pixel[1] & 0x1c) << 3) | ((pixel[2] & 0xF8) >> 3);
                DataArray.insert(DataIndex, temp)
                DataIndex += 1
        outfile.write("const uint8_t {0}[{1}] = {{".format(filename, DataLength))


        for i in range(DataLength):
            if(i % (16) == 0):
                outfile.write("\n")
            outfile.write("0x{:02x},".format(DataArray[i]))

        outfile.write("\n};\n")

outfile.close()