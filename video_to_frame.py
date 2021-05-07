import cv2


def video_to_frames(video_path,output_folder):
    video = cv2.VideoCapture(video_path)
    success, image = video.read()
    count = 0
    while success:
        cv2.imwrite(output_folder+"/frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = video.read()
        print('Reading a new frame: ', success)
        count += 1

    print("done")
