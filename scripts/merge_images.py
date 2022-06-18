from PIL import Image

import sys	
import glob
import os
import re

import subprocess

MAPS_DIR = 'tmp/map_images/'
SKY_DIR = 'tmp/sky_images/'
SKY_MAP_DIR = 'tmp/sky_and_map_images/'

def cleanup_images():
	image_list = glob.glob(os.path.join(SKY_MAP_DIR, "*.png"))
	for image_path in image_list:
		os.remove(image_path)
		subprocess.run(["git", "rm", image_path])
	os.makedirs(SKY_MAP_DIR, exist_ok=True)

def main(args):
    cleanup_images()

    map_files = glob.glob(os.path.join(MAPS_DIR, "*.png"))
    sky_files = glob.glob(os.path.join(SKY_DIR, "*.jpeg"))

    for map_file in map_files:
        m = re.search('images/map_(.+?).png', map_file)
        timestamp = m.group(1)

        sky_file = [s for s in sky_files if timestamp in s][0]

        im1 = Image.open(sky_file)
        im2 = Image.open(map_file)

        position = ((im1.width - im2.width), (im1.height - im2.height))
        im1.paste(
            im2, 
            position,
        )

        im1.save(
            SKY_MAP_DIR + 'sky_map_' + timestamp + '.png', 
            quality=50
        )

        im1.close()
        im2.close()

        break

if __name__ == "__main__":
    main(sys.argv[1:])