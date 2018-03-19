from PIL import Image
import sys
import os

# 黑底白字
# 0->黑 1->白


## 读取文件
# file_path = r"pic/"
# dirs = os.listdir(file_path)
# for i in dirs:
#     if os.path.splitext(i)[1] == ".bmp":
#         print(os.path.splitext(i)[0])



# 打开文件
filename = "number_10"
img=Image.open("pic/hour_1.bmp")

# 输出文件
outfile = open("array.txt", "w")

width=img.size[0]
height=img.size[1]
row = width // 8 + 1
print("实际宽，高:" , width,",", height)


DataArray = []
DataLength = 0
temp = 0
index = 0

w_ = (width // 8 + 1) * 8 #实际数据宽度（即要加上补零）
print(w_)

# width = 6
# height = 10
# 从0开始
for h in range(height):
    for w in range(w_):
        if((w+1) > width):  #(w > 32)
            print("w > width", w)
            # todo 直接补零

        else:
            # todo black 写0
            print("w <= width", w)
            pixel = img.getpixel((w, h))
            if (pixel[0] == pixel[1] == pixel[2] == 0): #白色字
                temp |= 0 << (7 - w % 8)


            else:
                # TODO white 写1
                temp |= 1 << (7 - w % 8)


        # 一个字节了
        if((w + 1)%8 == 0 and w != 0):
            print("output temp: ", temp)
            DataArray.append(temp)
            DataLength += 1
            temp = 0
outfile.write("const uint8_t {0}[] = {{".format(filename))

for i in range(DataLength -1):
    if(i % row == 0):
        outfile.write("\n")
    outfile.write("0x{:02x},".format(DataArray[i]))

outfile.write("0x{:02x}\n}}".format(DataArray[DataLength - 1]))

outfile.close()
