from imutils import paths
from shutil import copy

SRC = "D:/map stitching/all_imgs/all_imgs/"
DEST = "C:/Users/ftl/Desktop/ImageStitch/frames"

results = sorted(paths.list_images((SRC)))
NUM = 300
c= 0

for i, r in enumerate(results):
    if i % NUM == 0:
        print("Moving "+r+" to "+DEST)
        copy(r, DEST)
        c += 1

print("done. "+str(c)+" images copied")
