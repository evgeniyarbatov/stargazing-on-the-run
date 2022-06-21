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

        with open(sky_file, 'rb') as s, open(map_file, 'rb') as m:
            im1 = Image.open(s)
            im2 = Image.open(m)

            position = ((im1.width - im2.width), (im1.height - im2.height))
            im1.paste(
                im2, 
                position,
            )

            im1.save(
                SKY_MAP_DIR + 'sky_map_' + timestamp + '.png', 
                optimize=True,
                quality=95
            )

            im1.close()
            im2.close()

            del im1
            del im2

if __name__ == "__main__":
    main(sys.argv[1:])