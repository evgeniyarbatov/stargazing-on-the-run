from PIL import Image

import sys	
import glob
import os
import re

def main(args):
    maps_files = glob.glob(os.path.join("images/", "*.png"))
    sky_maps_files = glob.glob(os.path.join("sky_maps/", "*.png"))

    for map_file in maps_files:
        m = re.search('_(.+?).png', map_file)
        timestamp = m.group(1)

        sky_map_file = [s for s in sky_maps_files if timestamp in s][0]

        im1 = Image.open(sky_map_file)
        im2 = Image.open(map_file)
        im1.paste(im2)

        im1.save(
            'combined_maps/result_' + timestamp + '.png', 
            quality=95
        )

if __name__ == "__main__":
    main(sys.argv[1:])