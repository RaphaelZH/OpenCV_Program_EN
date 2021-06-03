import cv2

img_path = 'img/OpenCV_Logo.png'


def main():

    # read an image and assign it to the variable 'img'
    img = cv2.imread(img_path, 0)

    # display the image with an image name as the first parameter
    cv2.imshow('OpenCV Logo', img)

    # assign a wait time for a key-stroke to the variable 'exitOnKeyStroke'
    exitOnKeyStroke = cv2.waitKey(0)

    # if the key-stroke is equal to 27 (the 'esc' key), close all opencv windows
    if exitOnKeyStroke == 27:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
