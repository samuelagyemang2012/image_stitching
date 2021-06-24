# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2
import shutil


def stitch(image_path, output_path, output_path1, crop):
    print("[INFO] loading images...")
    imagePaths = sorted(list(paths.list_images(image_path)))
    images = []
    # loop over the image paths, load each one, and add them to our
    # images to stitch list
    for imagePath in imagePaths:
        image = cv2.imread(imagePath)
        images.append(image)
    # initialize OpenCV's image sticher object and then perform the image
    # stitching
    print("[INFO] stitching images...")
    stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
    (status, stitched) = stitcher.stitch(images)
    if status == 0:
        if crop:
            print("cropping")
            cropped = crop(stitched)
            cv2.imwrite(output_path, stitched)
            cv2.imwrite(output_path1, cropped)
        else:
            cv2.imwrite(output_path, stitched)

        print('done')
    else:
        print('not enough features')
        # cv2.imwrite(output_path, stitched)
        # print('done')


def private_stitch(image_list):
    print("[INFO] stitching images...")
    stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
    (status, stitched) = stitcher.stitch(image_list)
    return status, stitched


def stitch_timer(image_dir, output_path, image_range, timer):
    start = 0
    end = image_range
    temp_path = "temp"
    # output_path = "stitch_output"
    image_list = []
    count = 1

    result = sorted(paths.list_images(image_dir))
    img_paths = sorted(paths.list_images(image_dir))
    # if there n or more images
    if len(img_paths) >= image_range:
        # get the first n images
        if len(result) == 0:
            for p in img_paths[start:image_range]:
                image = cv2.imread(p)
                image_list.append(image)

            # stitch first n images
            private_stitch(image_list)
            count += 1
            start = end
            end += image_range
        else:
            for p in img_paths[start:end]:
                image = cv2.imread(p)
                image_list.append(image)
            # 	include result of the last stitch
            image_list.append(cv2.imread(result[count - 1]))
            private_stitch(image_list)
            count += 1
            start = end
            end += image_range
    else:
        print("Not enough images to stitch")
        return


def crop(stitched):
    stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))
    # convert the stitched image to grayscale and threshold it
    # such that all pixels greater than zero are set to 255
    # (foreground) while all others remain 0 (background)
    gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    # allocate memory for the mask which will contain the
    # rectangular bounding box of the stitched image region
    mask = np.zeros(thresh.shape, dtype="uint8")
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
    # create two copies of the mask: one to serve as our actual
    # minimum rectangular region and another to serve as a counter
    # for how many pixels need to be removed to form the minimum
    # rectangular region
    minRect = mask.copy()
    sub = mask.copy()
    # keep looping until there are no non-zero pixels left in the
    # subtracted image
    while cv2.countNonZero(sub) > 0:
        # erode the minimum rectangular mask and then subtract
        # the thresholded image from the minimum rectangular mask
        # so we can count if there are any non-zero pixels left
        minRect = cv2.erode(minRect, None)
        sub = cv2.subtract(minRect, thresh)

    cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    (x, y, w, h) = cv2.boundingRect(c)
    # use the bounding box coordinates to extract the our final
    # stitched image
    stitched = stitched[y:y + h, x:x + w]
    return stitched
