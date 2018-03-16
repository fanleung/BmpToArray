import operator
from PIL import Image
import numpy as np
import os

#[R,G,B]
color_red = [255, 0, 0]
color_green = [0, 255, 0]
color_blue = [0, 0, 255]
color_yellow = [255, 255, 0]
color_purple = [255, 0, 255]
color_skyBlue = [0, 255, 255]
color_white = [255, 255, 255]
color_black = [0, 0, 0]

path = r"C:\Users\k\Desktop\8colors"
for filename in os.listdir(r"C:\Users\k\Desktop\8colors"):
    pic_path = os.path.join(path, filename)
    array_name = filename.replace(".bmp", "")
    #print(pic_path)
    print(array_name)
    im = Image.open(pic_path)
    width, height = im.size
    # 宽高
    #print(im.size, "width = %d, heigth = %d" % (width, height))
    # 格式，以及格式的详细描述
    #print(im.format, im.format_description)
    im = im.convert('RGB')
    src_strlist = im.load()
    pix_array = np.zeros((height, width))

    for y_index in range(0, height):
        for x_index in range(0, width):
            data = src_strlist[x_index, y_index]
            if operator.eq(list(data), color_red) == 1:
                pix_array[y_index][x_index] = 8
            elif operator.eq(list(data), color_green) == 1:
                pix_array[y_index][x_index] = 4
            elif operator.eq(list(data), color_blue) == 1:
                pix_array[y_index][x_index] = 2
            elif operator.eq(list(data), color_yellow) == 1:
                pix_array[y_index][x_index] = 12
            elif operator.eq(list(data), color_purple) == 1:
                pix_array[y_index][x_index] = 10
            elif operator.eq(list(data), color_skyBlue) == 1:
                pix_array[y_index][x_index] = 6
            elif operator.eq(list(data), color_white) == 1:
                pix_array[y_index][x_index] = 14
            elif operator.eq(list(data), color_black) == 1:
                pix_array[y_index][x_index] = 0

    w_index = 0
    h_index = 0

    if width % 2 == 0:
        #print("even number")
        length = width//2
        for h_index in range(height):
            for w_index in range(0, width, 2):
                pix_array[h_index][w_index//2] = (int(pix_array[h_index][w_index]) << 4) + (int(pix_array[h_index][w_index + 1]) & 15)
    else:
        #print("odd number")
        length = width // 2 + 1
        for h_index in range(height):
            for w_index in range(0, (width - 1), 2):
                pix_array[h_index][w_index//2] = (int(pix_array[h_index][w_index]) << 4) + (int(pix_array[h_index][w_index + 1]) & 15)
            pix_array[h_index][(w_index + 2)//2] = (int(pix_array[h_index][w_index+2]) << 4) & 240

    fp = open(r'C:\Users\k\Desktop\picture\uidata.txt', 'a')

    print("const uint8_t picture_%s_%dx%d[%d] = {" % (array_name, height, width, height*length), file=fp)

    count_print = 0
    count_row = 0

    for y_index in range(height):
        if width % 2 == 0:
            for x_index in range(width//2):
                print(hex(int(pix_array[y_index][x_index])), end=',', file=fp)
                count_print += 1
            print('\n', file=fp)
        else:
            for x_index in range(width//2+1):
                print(hex(int(pix_array[y_index][x_index])), end=',', file=fp)
                count_print += 1
            print('\n', file=fp)
    print('};\n', file=fp)

    fp.close()
    print(count_print)


