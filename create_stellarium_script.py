#!/usr/bin/python

import random
import gpxpy
import pyproj
import sys	
from dateutil import tz

LOCAL_TZ = 'Asia/Singapore'

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

	def setAzimuth(self, az):
		self.az = az

	def __str__(self):
		return "time: {0} lat: {1} lon: {2} alt: {3} az: {4}".format(
			self.time,
			self.lat,
			self.lon,
			self.alt,
			self.az
		)

class StellariumScript:
	__args = None
	__script = """
    // Author: Evgeny Arbatov
    // Version: 1.0
    // License: Public Domain
    // Name: GPX to Stellarium images
    // Description: Convert GPX files to Stellarium images

    param_az = $AZ$
    param_alt = $ALT$
    param_lat = $LAT$
    param_long = $LONG$
    param_date = "$DATE$"

    core.setTimeRate(0); 
    core.setGuiVisible(false);
    core.setMilkyWayVisible(true);
    core.setMilkyWayIntensity(4);
    SolarSystem.setFlagPlanets(true);
    SolarSystem.setMoonScale(6);
    SolarSystem.setFlagMoonScale(true);
    SolarSystem.setFontSize(25);
    
    StelSkyDrawer.setAbsoluteStarScale(1.5);
    StelSkyDrawer.setRelativeStarScale(1.65);
    StarMgr.setFontSize(20);
    StarMgr.setLabelsAmount(3);
    ConstellationMgr.setFlagLines(true);
    ConstellationMgr.setFlagLabels(true);
    ConstellationMgr.setArtIntensity(0.1);
    ConstellationMgr.setFlagArt(true);
    ConstellationMgr.setFlagBoundaries(false);
    ConstellationMgr.setConstellationLineThickness(3);
    ConstellationMgr.setFontSize(18);

    LandscapeMgr.setFlagAtmosphere(true);
    StelMovementMgr.zoomTo(70, 0);
    core.wait(0.5);

	core.setDate(date, "local");
	core.setObserverLocation(long, lat, 0, 0, "Singapore", "Earth");
	core.wait(0.5);
	core.moveToAltAzi(alt, azi)
	core.wait(0.5);

	core.setDate('+' + param_dt + ' seconds');
	core.screenshot(file_prefix);

    core.setGuiVisible(true);
    core.quitStellarium();
	"""

	def __init__(self, args):
		self.__args = args

	def create_script(self):
		script = self.__script
		script = script.replace("$LAT$", self.__args['lat'])
		script = script.replace("$LONG$", self.__args['long'])
		script = script.replace("$DATE$", self.__args['date'])
		script = script.replace("$AZ$", self.__args['az'])
		script = script.replace("$ALT$", self.__args['alt'])

		file = open("script.ssc", "w")
		file.write(script)
		file.close()

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
						local_time, 
						point.latitude, 
						point.longitude, 
						point.elevation					
					)
				)

	return points

def sample_points(points):
	return points[::20]

def get_azimuth(points):
	for idx, point in enumerate(points, start=1):
		previous_point = points[
			idx - random.randint(5, 10)
		]

		G = pyproj.Geod(ellps='WGS84')
		fwd_azimuth = G.inv(
			previous_point.lon,
			previous_point.lat,
			point.lon,
			point.lat
		)[0]

		point.setAzimuth(fwd_azimuth)

def main(args):
	gpx_file = args[0]

	points = parse_gpx_file(gpx_file)
	points = sample_points(points)
	get_azimuth(points)

	# script = StellariumScript(dict[
	# 	'lat': points_with_bearing[0][2],
	# 	'long': points_with_bearing[0][1],
	# 	'date': points_with_bearing[0][0],
	# 	'az': points_with_bearing[0][4],
	# 	'alt': points_with_bearing[0][3],
	# ])
	# script.create_script()

if __name__ == "__main__":
    main(sys.argv[1:])