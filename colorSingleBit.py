from PIL import Image
import sys
import os

# 黑底白字
# 0->黑 1->白

# 需要用到的中间变量
DataArray = []  # 每个图片的数组
DataLength = 0  # 数组的长度
DataIndex = 0   # 数组当前的写坐标
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
                img=Image.open(allFile[i] + '/' + filename + fileType)

                # 读取文件信息
                width=img.size[0]
                height=img.size[1]
                row = width // 8 + 1
                DataLength = row * height
                print("实际宽，高:" , width,",", height)
                print("Datalength: ",DataLength)


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
                            outfileC.write("const uint8_t {0}[] = {{".format(filename))

                for k in range(DataIndex - 1):
                    if(k % row == 0):
                        outfileC.write("\n")
                    outfileC.write("0x{:02x},".format(DataArray[k]))

            if((DataIndex - 1)%row == 0):
                outfileC.write("\n0x{:02x},\n}};\n\n".format(DataArray[DataIndex - 1]))
            else:
                outfileC.write("0x{:02x},\n}};\n\n".format(DataArray[DataIndex - 1]))
            outfileH.write("\nextern const uint8_t {0}_{1}X{2}[{3}];\n".format(filename.upper(), width, height, DataLength))

        outfileC.close()
        outfileH.write("\n\n#endif\n")
        outfileH.close()

