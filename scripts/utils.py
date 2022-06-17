#!/usr/bin/python

import gpxpy
import pyproj

from dateutil import tz

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

	def setAzimuth(self, az):
		self.az = az

	def __str__(self):
		return "date: '{0}', timestamp: {1}, lat: {2}, lon: {3}, alt: {4}, az: {5}".format(
			self.date,
			self.timestamp,
			self.lat,
			self.lon,
			self.alt,
			self.az
		)

	def to_dict(self):
		return {
			'date': self.date,
			'timestamp': self.timestamp,
			'lat': self.lat,
			'lon': self.lon,
			'az': self.az,
		}


class GPXData:
	LOCAL_TZ = 'Asia/Singapore'

	def __init__(
		self,
		filename
	):
		self.points = []

		gpx_file = open(filename, 'r')
		gpx = gpxpy.parse(gpx_file)

		for track in gpx.tracks:
			for segment in track.segments:
				for point in segment.points:
					dt = point.time.replace(
						tzinfo=tz.gettz('UTC')
					)
					local_time = dt.astimezone(
						tz.gettz(GPXData.LOCAL_TZ)
					)

					self.points.append(
						Point(
							local_time.strftime('%Y-%m-%dT%H:%M:%S'), 
							local_time.strftime('%s'), 
							point.latitude, 
							point.longitude, 
							point.elevation					
						)
					)

	def sample_points(self):
		self.points = self.points[::50]

	def set_azimuth(self):
		G = pyproj.Geod(ellps='WGS84')

		for idx, point in enumerate(self.points, start=1):
			previous_point = self.points[
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

	def get_points(self):
		return self.points	