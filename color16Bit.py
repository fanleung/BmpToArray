from PIL import Image
import sys
import os

# 取高位的数据

# 需要用到的中间变量
DataArray = []  # 每个图片的数组
DataLength = 0  # 数组的长度
DataIndex = 0   # 数组的当前写坐标
temp = 0        # 一个字节

SkipCount = 1
startAddress = "(UI_EXFLASH_BASE_ADDR)"

PreFilename = ""
PreWidth = 0
PreHeight = 0

# 创建ui.txt
if os.path.exists("UI.txt"):
  os.remove("UI.txt")
outfileTXT = open("UI.txt", "w")

# 创建ui.c
if os.path.exists("UI.c"):
  os.remove("UI.c")
outfileC = open("UI.c", "w")
outfileC.write("#include \"UI.h\" \n\n" )

# 创建ui.h
if os.path.exists("UI.h"):
    os.remove("UI.h")
outfileH = open("UI.h", "w")
outfileH.write("#ifndef UI_H_\n")
outfileH.write("#define UI_H_\n\n")

# 创建ui_exflash_address_map.h
if os.path.exists("ui_exflash_address_map.h"):
    os.remove("ui_exflash_address_map.h")
outfileMap = open("ui_exflash_address_map.h", "w")
outfileMap.write("#include \"UI.h\" \n\n" )
outfileMap.write("#define UI_EXFLASH_BASE_ADDR              10\r\n" )
outfileMap.write("#define UI_ADDR(UI_ID)			        (UI_ID##_ADDR)\n" )
outfileMap.write("#define UI_END_ADDR(UI_ID)		        (UI_ID##_ADDR + sizeof(UI_ID))\n" )
outfileMap.write("#define UI_ADDR_ARRAY(UI_ID, INDEX)   	(UI_ID##_ADDR + sizeof(UI_ID##[0])*(INDEX))\r\n" )

# 创建ui_save_exflash.c
if os.path.exists("ui_save_exflash.c"):
    os.remove("ui_save_exflash.c")
outfileSave = open("ui_save_exflash.c", "w")
outfileSave.write("#include \"application.h\"\n")
outfileSave.write("#include \"ui_exflash_address_map.h\"\n")
outfileSave.write("#include \"nrf_delay.h\"\n\n")
outfileSave.write("#define SAVE_UI(X)    		app_flash_write(X,X##_ADDR,sizeof(X))\n\n")
outfileSave.write("void save_ui2flash(void)\n{\n")
outfileSave.write("\tflash_device_power_down_set(false);\n")


# 读取文件
# file_path = r"color/"
# file_path = r"Time/"
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
        outfileC.write("const uint8_t {0}_{1}X{2}[{3}] = {{\n".format(filename, width, height, DataLength))
        outfileTXT.write("const uint8_t {0}_{1}X{2}[{3}] = {{\n".format(filename, width, height, DataLength))

        for i in range(DataLength):
            if(i % (16) == 0):
                outfileC.write("\n")
            outfileC.write("0x{:02x},".format(DataArray[i]))
            outfileTXT.write("0x{:02x},".format(DataArray[i]))

        outfileC.write("\n};\n")
        outfileTXT.write("\n};\n")
        outfileH.write("\nextern const uint8_t {0}_{1}X{2}[{3}];\n".format(filename, width, height, DataLength))

        # todo 写map文件
        if(SkipCount == 1):
            SkipCount = 0
            outfileMap.write("#define {0}_{1}X{2}_ADDR     {3}\n".format(filename, width, height, startAddress))
        else:
            outfileMap.write("#define {0}_{1}X{2}_ADDR     ({3}_{4}X{5}_ADDR + sizeof({6}_{7}X{8}))\n".format(
                filename, width, height, PreFilename, PreWidth, PreHeight, PreFilename, PreWidth, PreHeight))

        # todo 写save.c文件
        outfileSave.write("\tSAVE_UI({0}_{1}X{2})\n".format(filename, width, height))


        PreFilename = filename
        PreWidth = width
        PreHeight = height


outfileC.close()
outfileTXT.close()
outfileH.write("\n\n#endif\n")
outfileH.close()
outfileMap.write("#define UI_FINISH_ADDR    ({0}_{1}X{2}_ADDR + sizeof({3}_{4}X{5}))\n".format(filename, width, height, filename, width, height))
outfileMap.close()
outfileSave.write("\tend_addr = UI_FINISH_ADDR / 1024;\n")
outfileSave.write("\tapp_flash_write(flash_id,UI_EXFLASH_BASE_ADDR-10,10);\n")
outfileSave.write("\n}\n")
outfileSave.close()