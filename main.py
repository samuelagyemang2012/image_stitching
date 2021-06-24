from stitch import stitch

# video_path = 'mapVideo.mp4'
# output_folder = "frames"
# Convert a video to individual frames
# video_to_frames(video_path, output_folder)
# -----

image_dir = "test_images"
output_dir = "stitch_output"
stitch(image_dir, output_dir + "/result.jpg", output_dir + "/cropped.jpg", False)
