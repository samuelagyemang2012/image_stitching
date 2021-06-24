from stitch import private_stitch
from imutils import paths
import cv2
import time

COUNT = 1
IMAGE_RANGE = 3
IMAGE_DIR = "frames"
OUTPUT_PATH = "result"
START = 0
END = IMAGE_RANGE
TEMP_PATH = "temp"
TIMER = 5
# output_path = "stitch_output"
image_list = []

while True:
    # images must be inputed in an orderly manner
    result_path = sorted(paths.list_images(OUTPUT_PATH))
    imgs_path = sorted(paths.list_images(IMAGE_DIR))

    # if there n or more images in main folder
    if len(imgs_path) >= IMAGE_RANGE:
        # check if the results folder is empty, 0 means no stitching has been done yet (if is first stitch)
        if len(result_path) == 0:
            for p in imgs_path[START:IMAGE_RANGE]:
                image = cv2.imread(p)
                image_list.append(image)

            # stitch first n images
            print("Round: " + str(COUNT) + " stitching started")
            status, stitched = private_stitch(image_list)
            if status == 0:
                cv2.imwrite(OUTPUT_PATH + "/result" + str(COUNT) + ".jpg", stitched)
                print("Round: " + str(COUNT) + " stitching ended")
                COUNT += 1
                START = END
                END += IMAGE_RANGE
                image_list.clear()
            else:
                print("not enough features to perform a stitch")
                break
        else:
            # if the results folder is not empty, stitching has already began
            # check if new images have been added
            l = imgs_path[START:END]
            if len(l) == 0:
                print("No new images added!")
                break
            else:
                for p in imgs_path[START:END]:
                    image = cv2.imread(p)
                    image_list.append(image)
            # 	include result of the last stitch
            image_list.append(cv2.imread(result_path[len(result_path) - 1]))
            print("Round: " + str(COUNT) + " stitching started")
            status, stitched = private_stitch(image_list)
            if status == 0:
                cv2.imwrite(OUTPUT_PATH + "/result" + str(COUNT) + ".jpg", stitched)
                print("Round: " + str(COUNT) + " stitching ended")
                COUNT += 1
                START = END
                END += IMAGE_RANGE
                image_list.clear()
            else:
                print("not enough features to perform a stitch")
                break
    else:
        print("Not enough images to stitch")
        break

    time.sleep(TIMER)
