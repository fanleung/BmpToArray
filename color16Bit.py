from PIL import Image
import sys
import os

# 取高位的数据

# 需要用到的中间变量
DataArray = []  # 每个图片的数组
DataLength = 0  # 数组的长度
DataIndex = 0   # 数组的当前写坐标
temp = 0        # 一个字节


path = r"./"
allFile = os.listdir(path) #列出文件夹下所有的目录与文件

for i in range(len(allFile)):
    if(os.path.isdir(allFile[i])):  # 是文件夹
        print(allFile[i])      # 打印所有文件夹名

        #创建和文件夹同名的C文件
        if os.path.exists(allFile[i] + ".c"):
            os.remove(allFile[i] + ".c")
        outfileC = open(allFile[i] + ".c", "w")

        # 创建和文件夹同名的C文件
        if os.path.exists(allFile[i] + ".h"):
            os.remove(allFile[i] + ".h")
        outfileH = open(allFile[i] + ".h", "w")
        # 写H文件
        outfileH.write("#ifndef __" + allFile[i].upper() + "_H\n")
        outfileH.write("#define __" + allFile[i].upper() + "_H\n")
        outfileH.write("#include <stdint.h>\n")


        folder = os.listdir(allFile[i])  # 进入文件夹
        for j in folder:
            DataIndex = 0
            if os.path.splitext(j)[1] == ".bmp":
                # 打开文件
                filename = os.path.splitext(j)[0]
                fileType = ".bmp"
                img=Image.open(allFile[i] + '/' +filename + fileType)

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


                # 写C文件
                for h in range(height):
                    for w in range(width):
                        pixel = img.getpixel((w, h))

                        temp = (pixel[0] & 0xF8) | ((pixel[1] & 0xE0) >> 5)  #高5 + 高3
                        DataArray.insert(DataIndex, temp)
                        DataIndex += 1

                        temp = ((pixel[1] & 0x1c) << 3) | ((pixel[2] & 0xF8) >> 3);
                        DataArray.insert(DataIndex, temp)
                        DataIndex += 1
                outfileC.write("const uint8_t {0}_{1}X{2}[{3}] = {{".format(filename.upper(), width, height, DataLength))


                for k in range(DataLength):
                    if(k % (16) == 0):
                        outfileC.write("\n")
                    outfileC.write("0x{:02x},".format(DataArray[k]))
                outfileC.write("\n};\n")

                outfileH.write("\nextern const uint8_t {0}_{1}X{2}[{3}];\n".format(filename.upper(), width, height, DataLength))


        outfileC.close()
        outfileH.write("\n\n#endif\n")
        outfileH.close()

# if os.path.exists("array.txt"):
#     os.remove("array.txt")
# outfile = open("array.txt", "w")
#
# # 读取文件
# file_path = r"color/"
# # file_path = r"./"
# dirs = os.listdir(file_path)
# for i in dirs:
#     DataIndex = 0
#     if os.path.splitext(i)[1] == ".bmp":
#         # 打开文件
#         filename = os.path.splitext(i)[0]
#         fileType = ".bmp"
#         img=Image.open(file_path + filename + fileType)
#         print(file_path + filename + fileType)
#
#         # 读取文件信息
#         width=img.size[0]
#         height=img.size[1]
#         DataLength = width * height * 2
#         row = width // 8 + 1
#         print("实际宽，高:" , width,",", height)
#         print("数组大小:", DataLength)
#
#         # 实际数据宽度（即要加上补零的位数）
#         w_ = (width // 8 + 1) * 8
#         # print(w_)
#
#         for h in range(height):
#             for w in range(width):
#                 pixel = img.getpixel((w, h))
#
#                 temp = (pixel[0] & 0xF8) | ((pixel[1] & 0xE0) >> 5)  #高5 + 高3
#                 DataArray.insert(DataIndex, temp)
#                 DataIndex += 1
#
#                 temp = ((pixel[1] & 0x1c) << 3) | ((pixel[2] & 0xF8) >> 3);
#                 DataArray.insert(DataIndex, temp)
#                 DataIndex += 1
#         outfile.write("const uint8_t {0}[{1}] = {{".format(filename, DataLength))
#
#
#         for i in range(DataLength):
#             if(i % (16) == 0):
#                 outfile.write("\n")
#             outfile.write("0x{:02x},".format(DataArray[i]))
#
#         outfile.write("\n};\n")
#
# outfile.close()