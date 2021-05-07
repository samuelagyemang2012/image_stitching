from video_to_frame import video_to_frames
from stitch import stitch as s1

if __name__ == '__main__':

   # video_path = 'mapVideo.mp4'
    # output_folder = "frames"
    # Convert a video to individual frames

    # video_to_frames(video_path, output_folder)
    # -----

    # Start stitching
    image_dir = "test_images"
    output_dir = "stitch_output/final.jpg"

    # alg1
    s1(image_dir,output_dir)


