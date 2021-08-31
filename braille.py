import argparse
import cv2 as cv
from itertools import product

bin_braille_dict = {
    0b000000: '⠂',
    0b100000: '⠁',
    0b010000: '⠂',
    0b110000: '⠃',
    0b001000: '⠄',
    0b101000: '⠅',
    0b011000: '⠆',
    0b111000: '⠇',
    0b000100: '⠈',
    0b100100: '⠉',
    0b010100: '⠊',
    0b110100: '⠋',
    0b001100: '⠌',
    0b101100: '⠍',
    0b011100: '⠎',
    0b111100: '⠏',
    0b000010: '⠐',
    0b100010: '⠑',
    0b010010: '⠒',
    0b110010: '⠓',
    0b001010: '⠔',
    0b101010: '⠕',
    0b011010: '⠖',
    0b111010: '⠗',
    0b000110: '⠘',
    0b100110: '⠙',
    0b010110: '⠚',
    0b110110: '⠛',
    0b001110: '⠜',
    0b101110: '⠝',
    0b011110: '⠞',
    0b111110: '⠟',
    0b000001: '⠠',
    0b100001: '⠡',
    0b010001: '⠢',
    0b110001: '⠣',
    0b001001: '⠤',
    0b101001: '⠥',
    0b011001: '⠦',
    0b111001: '⠧',
    0b000101: '⠨',
    0b100101: '⠩',
    0b010101: '⠪',
    0b110101: '⠫',
    0b001101: '⠬',
    0b101101: '⠭',
    0b011101: '⠮',
    0b111101: '⠯',
    0b000011: '⠰',
    0b100011: '⠱',
    0b010011: '⠲',
    0b110011: '⠳',
    0b001011: '⠴',
    0b101011: '⠵',
    0b011011: '⠶',
    0b111011: '⠷',
    0b000111: '⠸',
    0b100111: '⠹',
    0b010111: '⠺',
    0b110111: '⠻',
    0b001111: '⠼',
    0b101111: '⠽',
    0b011111: '⠾',
    0b111111: '⠿'
}


def read_and_thresh(filepath, val, auto=True, inv=False):
    bgr = cv.imread(filepath)
    gray = cv.cvtColor(bgr, cv.COLOR_BGR2GRAY)
    if auto:
        threshold, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU) if not inv else cv.threshold(
            gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    else:
        threshold, thresh = cv.threshold(gray, val, 255, cv.THRESH_BINARY) if not inv else cv.threshold(
            gray, val, 255, cv.THRESH_BINARY_INV)

    return thresh


def shave_img(img):
    height = img.shape[0]
    width = img.shape[1]

    if height % 3 != 0:
        img = img[:-(height % 3), :]
    if width % 2 != 0:
        img = img[:, :-(width % 2)]

    return img


def bin2braille(img):
    height = img.shape[0]
    width = img.shape[1]

    ascii_list = []
    for blockrow, blockcol in product(range(0, height, 3), range(0, width, 2)):
        bin_str = ''
        for col, row in product(range(2), range(3)):
            if img[row + blockrow, col + blockcol] > 0:
                bin_str += '1'
            else:
                bin_str += '0'
        braille_char = bin_braille_dict.get(int(bin_str, 2))
        ascii_list.append(braille_char)

    return ascii_list


def print_braille(ascii_list, width, height):
    height //= 3
    width //= 2
    count = 0

    for rows in range(height):
        line_str = ''
        sublist = ascii_list[count:count + width - 1]
        count += width
        line_str = line_str.join(sublist)
        print(line_str)


def save_braille(ascii_list, width, height, outFile):
    height //= 3
    width //= 2
    count = 0

    file = open(outFile, 'w')
    for rows in range(height):
        line_str = ''
        sublist = ascii_list[count:count + width - 1]
        count += width
        line_str = line_str.join(sublist)
        file.write(line_str + '\n')
    file.close()


def main():
    desc = 'Groups image pixels to braille ASCII.'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--img', dest='filepath', required=True)
    parser.add_argument('--width', dest='width', required=False)
    parser.add_argument('--save', dest='outFile', required=False)
    parser.add_argument('--inv', dest='invFlag', required=False)
    parser.add_argument('--thresh', dest='threshVal', required=False)

    args = parser.parse_args()

    filepath = args.filepath

    width = 60
    if args.width:
        width = args.width

    outFile = 'braille_ascii_out.txt'
    outFlag = False
    if args.outFile:
        outFile = args.outFile
        outFlag = True

    invFlag = False
    if args.invFlag:
        invFlag = True

    threshVal = 150
    autoFlag = True
    if args.threshVal:
        threshVal = args.threshVal
        autoFlag = False

    img = read_and_thresh(filepath, threshVal, autoFlag, invFlag)
    img = cv.resize(img, ((width * 4) // 3, width), interpolation=cv.INTER_AREA)
    height = img.shape[0]
    width = img.shape[1]
    ascii_list = bin2braille(img)

    if outFlag:
        save_braille(ascii_list, width, height, outFile)
    else:
        print_braille(ascii_list, width, height)


if __name__ == '__main__':
    main()
