import cv2
import numpy as np

img_path = 'img/OpenCV_Logo.png'


def main():

    # read an image and assign it to the variable 'img'
    img = cv2.imread(img_path)

    # resize the image to a quarter of its original size
    img_resized = cv2.resize(img, (0, 0), None, .25, .25)

    # convert the image to the HSV color model
    img_HSV = cv2.cvtColor(img_resized, cv2.COLOR_BGR2HSV)

    # convert the image to the gray degree
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

    # convert the greyed image to the BGR color model
    img_BGR = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

    # stack arrays in sequence vertically (row-wise)
    numpy_vertical = np.vstack((img_resized, img_HSV, img_BGR))

    # stack arrays in sequence horizontally (column-wise)
    numpy_horizontal = np.hstack((img_resized, img_HSV, img_BGR))

    # join a sequence of arrays along an existing axis
    numpy_vertical_concat = np.concatenate(
        (img_resized, img_HSV, img_BGR), axis=0)
    numpy_horizontal_concat = np.concatenate(
        (img_resized, img_HSV, img_BGR), axis=1)

    cv2.imshow('Main', img)
    cv2.imshow('Numpy Vertical', numpy_vertical)
    cv2.imshow('Numpy Horizontal', numpy_horizontal)
    cv2.imshow('Numpy Vertical Concat', numpy_vertical_concat)
    cv2.imshow('Numpy Horizontal Concat', numpy_horizontal_concat)

    # assign a wait time for a key-stroke to the variable 'exitOnKeyStroke'
    exitOnKeyStroke = cv2.waitKey(0)

    # if the key-stroke is equal to 27 (the 'esc' key), close all opencv windows
    if exitOnKeyStroke == 27:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
