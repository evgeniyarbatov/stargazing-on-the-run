#!/usr/bin/python

import gpxpy
import pyproj

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from numpy import pi

import random
import sys	
import glob
import os
import subprocess

from dateutil import tz

LOCAL_TZ = 'Asia/Singapore'
SCREENSHOT_LOCATION = '/Users/arbatov/gitRepo/stargazing-on-the-run/sky_maps'

# python3 create_stellarium_script.py data/Morning_Run.gpx 

class Point:
	def __init__(
		self, 
		date,
		timestamp,
		lat,
		lon,
		alt
	):
		self.date = date
		self.timestamp = timestamp

		self.lat = float(lat)
		self.lon = float(lon)
		self.alt = float(alt)

		self.az = None
		self.dist = None

	def setAzimuth(self, az):
		self.az = az

	def setDistance(self, distance):
		self.dist = distance

	def __str__(self):
		return "date: '{0}', timestamp: {1}, lat: {2}, lon: {3}, alt: {4}, az: {5}, dist: {6}".format(
			self.date,
			self.timestamp,
			self.lat,
			self.lon,
			self.alt,
			self.az,
			self.dist
		)

	def to_dict(self):
		return {
			'date': self.date,
			'timestamp': self.timestamp,
			'lat': self.lat,
			'lon': self.lon,
			'az': self.az,
		}

class StellariumScript:
	__script = """
// Author: Evgeny Arbatov
// Version: 1.0
// License: Public Domain
// Name: GPX to Stellarium images
// Description: Convert GPX files to Stellarium images

points = [
	$POINTS$
];

core.clear("natural");
core.setGuiVisible(false);

GridLinesMgr.setFlagEquatorGrid(false);

LandscapeMgr.setFlagLandscape(true);
LandscapeMgr.setFlagAtmosphere(true);

ConstellationMgr.setFlagLines(true);
ConstellationMgr.setFlagLabels(true);
ConstellationMgr.setFlagArt(true);

SolarSystem.setFlagPlanets(true);
SolarSystem.setFlagLabels(true);

StarMgr.setFlagStars(true);
StarMgr.setFlagLabels(true);

MilkyWay.setFlagShow(true);
MilkyWay.setIntensity(5);

SporadicMeteorMgr.setFlagShow(true);

NebulaMgr.setFlagShow(true);

points.forEach(
	function(point) {
		core.moveToAltAzi(point.alt, point.az)
		core.wait(0.01);

		core.setObserverLocation(
			point.long, 
			point.lat, 
			point.alt
		);

		core.setDate(point.date, "local");

		core.setTimeRate(0);
		core.wait(1);

		core.screenshot(
			"stellarium_" + point.timestamp, 
			false,
			"$SCREENSHOT_LOCATION$",
			false,
			"png"
		);
	}
);
	"""

	def __init__(self, points):
		self.points = points

	def create_script(self):
		script = self.__script
		script = script.replace(
			"$POINTS$", 
			",\n".join('{ ' + str(point) + ' }' for point in self.points)
		)
		script = script.replace(
			"$SCREENSHOT_LOCATION$", 
			SCREENSHOT_LOCATION
		)

		file = open("script/script.ssc", "w")
		file.write(script)
		file.close()

def cleanup_images():
	image_list = glob.glob(os.path.join("images/", "*.png"))
	for image_path in image_list:
		os.remove(image_path)
		subprocess.run(["git", "rm", image_path])
	os.makedirs("images", exist_ok=True)

def get_local_time(dt):
	local_tz = tz.gettz(LOCAL_TZ)
	dt = dt.replace(tzinfo=tz.gettz('UTC'))
	return dt.astimezone(tz.gettz(LOCAL_TZ))

def parse_gpx_file(filename):
	points = []

	gpx_file = open(filename, 'r')
	gpx = gpxpy.parse(gpx_file)

	for track in gpx.tracks:
		for segment in track.segments:
			for point in segment.points:
				local_time = get_local_time(point.time)

				points.append(
					Point(
						local_time.strftime('%Y-%m-%dT%H:%M:%S'), 
						local_time.strftime('%s'), 
						point.latitude, 
						point.longitude, 
						point.elevation					
					)
				)

	return points

def sample_points(points):
	return points[::50]

def set_azimuth(points):
	G = pyproj.Geod(ellps='WGS84')

	for idx, point in enumerate(points, start=1):
		previous_point = points[
			idx - 2
		]

		fwd_azimuth = G.inv(
			previous_point.lon,
			previous_point.lat,
			point.lon,
			point.lat
		)[0]

		if fwd_azimuth < 0:
			fwd_azimuth += 360

		point.setAzimuth(fwd_azimuth)

def set_distance(points):
	G = pyproj.Geod(ellps='WGS84')

	for idx, point in enumerate(points, start=1):
		previous_point = points[
			idx - 2
		]

		distance = G.inv(
			previous_point.lon,
			previous_point.lat,
			point.lon,
			point.lat
		)[2]

		point.setDistance(distance)

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

	cleanup_images()

	points = parse_gpx_file(gpx_file)
	points = sample_points(points)

	set_azimuth(points)
	set_distance(points)

	script = StellariumScript(points)
	script.create_script()

	plot_run(points)

if __name__ == "__main__":
    main(sys.argv[1:])