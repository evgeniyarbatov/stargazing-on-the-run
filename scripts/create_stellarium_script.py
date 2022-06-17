#!/usr/bin/python

from utils import GPXData

import sys	

# python3 create_stellarium_script.py data/Morning_Run.gpx 

class StellariumScript:
	SCREENSHOT_LOCATION = '/Users/arbatov/gitRepo/stargazing-on-the-run/sky_maps'

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

StelMovementMgr.zoomTo(40, 1);

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

core.quitStellarium();
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
			StellariumScript.SCREENSHOT_LOCATION
		)

		file = open("script/script.ssc", "w")
		file.write(script)
		file.close()

def main(args):
	gpx_file = args[0]

	gpx_data = GPXData(gpx_file)

	gpx_data.sample_points()
	gpx_data.set_azimuth()

	script = StellariumScript(
		gpx_data.get_points()
	)
	script.create_script()
	
if __name__ == "__main__":
    main(sys.argv[1:])