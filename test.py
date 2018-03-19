import binascii


# 0xDC,0xDC,0xDC,0xDC,0xDC,0xDC,0xDC,0xDC,0xDC,0xDC,/*"F:\代码\AB221\新建文件夹 (3)\表盘1\number_0.bmp",0*/

# 打开文件
file_name = "pic/number_10.bmp"
infile = open(file_name, "rb")
print(infile.read())

outfile = open("array.txt", "w")


# seek移动文件读取指针
infile.seek(0xA, 0)
start = int.from_bytes(infile.read(2), byteorder='little')
print("start:",start)

infile.seek(0x12, 0)
width = int.from_bytes(infile.read(4), byteorder='little')
print("width:", width)

height = int.from_bytes(infile.read(4), byteorder='little')
print("height:", height)


infile.seek(0x1C, 0)
bytesperpixel = int(int.from_bytes(infile.read(4), byteorder='little') / 8)
print("bytesperpixel:", bytesperpixel)


infile.seek(start, 0)
array = []
temp = []
for h in range(height):
    for w in range(width * bytesperpixel):
        temp.append(int.from_bytes(infile.read(1), byteorder='little'))
    temp.reverse()
    array.extend(temp)
    temp.clear()

array.reverse()
sixteenbit = []
for i in range(len(array)):
    if (i % 3 == 0):
        sixteenbit.append((array[i + 2] >> 3) << 3 | array[i + 1] >> 5)
        sixteenbit.append((array[i + 1] & 0x7) | array[i] >> 3)
# if form=="24":
#    outfile.write("const uint8_t {0}[{1}] ={{".format(file_name, len(array)))
#    for i in range(len(array)-1):
#        if (i%(width*bytesperpixel)==0):
#            outfile.write("\n")
#        outfile.write("0x{:02x},".format(array[i]))

#    outfile.write("0x{:02x}\n}};".format(array[len(array)-1]))
# else:
outfile.write("const uint8_t {0}[{1}] ={{".format(file_name, len(sixteenbit)))
for i in range(len(sixteenbit) - 1):
    if (i % (width * bytesperpixel * 2 / 3) == 0):
        outfile.write("\n")
    outfile.write("0x{:02x},".format(sixteenbit[i]))

outfile.write("0x{:02x}\n}};".format(sixteenbit[len(sixteenbit) - 1]))

infile.close()
outfile.close()

input("Byte array created as {}array.c!".format(file_name))
