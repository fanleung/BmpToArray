from PIL import Image
import sys
import os

# 黑底白字
# 0->黑 1->白

# 需要用到的中间变量
DataArray = []  # 每个图片的数组
DataIndex = 0   # 数组当前的写坐标
temp = 0        # 一个字节

# 输出文件
if os.path.exists("array.txt"):
  os.remove("array.txt")
outfile = open("array.txt", "w")

# 读取文件
# file_path = r"pic/"
file_path = r"./"
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
        row = width // 8 + 1
        # print("实际宽，高:" , width,",", height)

        # 实际数据宽度（即要加上补零的位数）
        w_ = (width // 8 + 1) * 8
        # print(w_)

        for h in range(height):
            for w in range(w_):
                if((w+1) > width):  #(w > 32)
                    temp |= 0 << (7 - w % 8)
                    # print("w > width", w)
                    # todo 直接补零

                else:
                    # todo black 写0
                    # print("w <= width", w)
                    pixel = img.getpixel((w, h))
                    if (pixel[0] == pixel[1] == pixel[2] == 0): #白色字
                        # TODO white 写1
                        temp |= 1 << (7 - w % 8)

                    else:
                        temp |= 0 << (7 - w % 8)


                # 一个字节了
                if((w + 1)%8 == 0 and w != 0):
                    # print("output temp: ", temp)
                    DataArray.insert(DataIndex, temp)
                    DataIndex += 1
                    temp = 0
        outfile.write("const uint8_t {0}[] = {{".format(filename))

        for i in range(DataIndex - 1):
            if(i % row == 0):
                outfile.write("\n")
            outfile.write("0x{:02x},".format(DataArray[i]))

    if((DataIndex - 1)%row == 0):
        outfile.write("\n0x{:02x},\n}};\n\n".format(DataArray[DataIndex - 1]))
    else:
        outfile.write("0x{:02x},\n}};\n\n".format(DataArray[DataIndex - 1]))

outfile.close()

