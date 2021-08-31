import argparse
import cv2 as cv
from itertools import product
from braille_dict import get_bin_braille_dict


def read_and_thresh(filepath, val, auto=True, inv=False):
    '''
    Reads an input image and converts it into a binary image.
    :param filepath: input image filepath.
    :param val: threshold value for creating binary image; set by user.
    :param auto: flag on whether to use automatic thresholding.
    :param inv: flag on whether to invert the binary image.
    :return:
    '''
    bgr = cv.imread(filepath)
    gray = cv.cvtColor(bgr, cv.COLOR_BGR2GRAY)

    # Use Otsu's method for automatic thresholding: https://en.wikipedia.org/wiki/Otsu%27s_method
    # Otherwise perform ordinary binary segmentation.
    if auto:
        threshold, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU) if not inv else cv.threshold(
            gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    else:
        threshold, thresh = cv.threshold(gray, val, 255, cv.THRESH_BINARY) if not inv else cv.threshold(
            gray, val, 255, cv.THRESH_BINARY_INV)

    return thresh


def shave_img(img):
    '''
    Shaves off select rows/columns if the dimensions do not allow for the grouping of pixels into 3x2 blocks. The edges
    of the image are shaved off because it is assumed the ROI is towards the center of the image.
    :param img: input image matrix.
    :return: image matrix that is "cropped" to allow for clean blocking.
    '''
    height = img.shape[0]
    width = img.shape[1]

    if height % 3 != 0:
        img = img[:-(height % 3), :]
    if width % 2 != 0:
        img = img[:, :-(width % 2)]

    return img


def bin2braille(img):
    '''
    Accumulates braille characters in a list based on values in each pixel block.
    :param img: input image matrix.
    :return: list containing braille glyphs to be used for printing.
    '''
    # https://en.wikipedia.org/wiki/Braille_ASCII
    # Braille dot binary string corresponds to specific braille glyph:
    # Every three digits corresponds to each column of the glyph.
    bin_braille_dict = get_bin_braille_dict()

    height = img.shape[0]
    width = img.shape[1]

    ascii_list = []
    # The image matrix is segmented into 3x2 blocks.
    for blockrow, blockcol in product(range(0, height, 3), range(0, width, 2)):
        bin_str = ''
        # Next, iterate through each pixel within the block.
        for col, row in product(range(2), range(3)):
            # Obtain the binary string that corresponds to each glyph.
            if img[row + blockrow, col + blockcol] > 0:
                bin_str += '1'
            else:
                bin_str += '0'
        # Convert the string to int and get its corresponding value from the bin_braille_dict.
        braille_char = bin_braille_dict.get(int(bin_str, 2))
        ascii_list.append(braille_char)

    return ascii_list


def print_braille(ascii_list, width, height):
    '''
    Print the ASCII art given the dimensions.
    :param ascii_list: list containing braille glyphs.
    :param width: width of ASCII art.
    :param height: height of ASCII art.
    :return: nothing; print ASCII art.
    '''
    # Dimensions are shortened because the pixels are "grouped together" as braille glyphs.
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
    '''
    Does the same as print_braille() but saves to a file instead of printing.
    :param ascii_list: list containing braille glyphs.
    :param width: width of ASCII art.
    :param height: height of ASCII art.
    :param outFile: file to save ASCII art text to.
    :return: nothing; save ASCII art.
    '''
    height //= 3
    width //= 2
    count = 0

    file = open(outFile, 'w', encoding='utf-8')
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
    parser.add_argument('--thresh', dest='threshVal', required=False)
    parser.add_argument('--inv', dest='invFlag', action='store_true')

    # Set argument parameter defaults.
    args = parser.parse_args()

    filepath = args.filepath

    width = 2 * int(args.width) if args.width else 60
    invFlag = args.invFlag if args.invFlag else False

    outFile = args.outFile if args.outFile else 'braille_ascii_out.txt'
    outFlag = True if args.outFile else False

    threshVal = int(args.threshVal) if args.threshVal else 150
    autoFlag = False if args.threshVal else True

    img = read_and_thresh(filepath, threshVal, autoFlag, invFlag)
    # Half the width seemed like a good height that didn't "strech" the art too much.
    img = cv.resize(img, (width, width // 2), interpolation=cv.INTER_AREA)
    img = shave_img(img)
    height = img.shape[0]
    width = img.shape[1]
    ascii_list = bin2braille(img)

    if outFlag:
        save_braille(ascii_list, width, height, outFile)
    else:
        print_braille(ascii_list, width, height)


if __name__ == '__main__':
    main()
