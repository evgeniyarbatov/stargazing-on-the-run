#!/usr/bin/python

from utils import GPXData

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from numpy import pi

import os
import subprocess
import glob
import sys

# python3 make_maps.py data/Morning_Run.gpx 

def cleanup_images():
	image_list = glob.glob(os.path.join("images/", "*.png"))
	for image_path in image_list:
		os.remove(image_path)
		subprocess.run(["git", "rm", image_path])
	os.makedirs("images", exist_ok=True)

def get_compass_data(degrees):
	values = [0, 0, 0, 0, 0, 0, 0, 0]
	values[int(degrees / 45)] = 1

	compass_data = pd.DataFrame({
		'value': values,
		'bearing': range(0, 360, 45),
		'compass': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
	})
	compass_data.index = compass_data['bearing'] * 2*pi / 360

	return compass_data

def plot_run(points):
	points_df = pd.DataFrame.from_records([
		p.to_dict() for p in points
	])

	for index, point in points_df.iterrows():
		compass_data = get_compass_data(point['az'])

		fig = plt.figure(figsize=(8, 4))
		gs = GridSpec(nrows=1, ncols=2, width_ratios=[1, 1])
		
		ax1 = fig.add_subplot(gs[0, 0])
		ax1.scatter(point['lon'], point['lat'], zorder=1, alpha=1, c='r', s=60, marker='o')
		ax1.plot(points_df['lon'], points_df['lat'])

		ax2 = fig.add_subplot(gs[0, 1], projection='polar')
		ax2.set_theta_zero_location('N')
		ax2.set_theta_direction(-1)
		ax2.bar(x=compass_data.index, height=compass_data['value'], width=pi/4)
		ax2.set_xticklabels(compass_data.compass)
		ax2.set_rgrids([])

		fig.savefig('images/location_'+ point['timestamp'] +'.png') 
		plt.close(fig) 

def main(args):
	gpx_file = args[0]

	gpx_data = GPXData(gpx_file)

	gpx_data.sample_points()
	gpx_data.set_azimuth()

	cleanup_images()
	plot_run(
		gpx_data.get_points()
	)

if __name__ == "__main__":
    main(sys.argv[1:])