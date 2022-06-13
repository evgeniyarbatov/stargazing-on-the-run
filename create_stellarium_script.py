#!/usr/bin/python

import gpxpy
import pyproj

import pandas as pd
import matplotlib.pyplot as plt

import random
import sys	
import glob
import os

from dateutil import tz

LOCAL_TZ = 'Asia/Singapore'
SCREENSHOT_LOCATION = '/Users/arbatov/Downloads/stellarium_screens'

# python3 create_stellarium_script.py data/Morning_Run.gpx 

class Point:
	def __init__(
		self, 
		time,
		lat,
		lon,
		alt
	):
		self.time = time

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
		return "date: '{0}', lat: {1}, lon: {2}, alt: {3}, az: {4}, dist: {5}".format(
			self.time,
			self.lat,
			self.lon,
			self.alt,
			self.az,
			self.dist
		)

	def to_dict(self):
		return {
			'date': self.time,
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

SpecialMarkersMgr.setFlagCompassMarks(true);

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
			"screenshot_", 
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

def plot_run(points_df):
	for index, point in points_df.iterrows():
		fig, ax = plt.subplots(figsize = (8,7))

		ax.scatter(point['lon'], point['lat'], zorder=1, alpha=1, c='r', s=60, marker='o')
		ax.plot(points_df['lon'], points_df['lat'])

		fig.savefig('images/location_'+ point['date'] +'.png') 
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

	points_df = pd.DataFrame.from_records([
		p.to_dict() for p in points
	])

	plot_run(points_df)

if __name__ == "__main__":
    main(sys.argv[1:])