#!/usr/bin/python

from utils import GPXData

import sys	

# python3 create_stellarium_script.py data/Morning_Run.gpx 

class StellariumScript:
	SCRIPT = """
// Author: Evgeny Arbatov
// Version: 1.0
// License: Public Domain
// Name: GPX to Stellarium images
// Description: Convert GPX files to Stellarium images

points = [
	$POINTS$
];

SolarSystem.setFlagPlanets(true);

SolarSystem.setFlagLabels(true);
SolarSystem.setLabelsAmount(10);

SolarSystem.setMoonScale(true);
SolarSystem.setFlagMoonScale(20);

SolarSystem.setFlagMinorBodyScale(true);
SolarSystem.setMinorBodyScale(20);

SolarSystem.setFlagPlanetScale(true);
SolarSystem.setPlanetScale(20);

core.clear("natural");
core.setGuiVisible(false);

StelMovementMgr.zoomTo(180, 1);

GridLinesMgr.setFlagEquatorGrid(false);

LandscapeMgr.setFlagLandscape(false);
LandscapeMgr.setFlagAtmosphere(true);

ConstellationMgr.setFlagLines(true);
ConstellationMgr.setFlagLabels(true);
ConstellationMgr.setFlagArt(true);

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
			"sky_" + point.timestamp, 
			false,
			"$SCREENSHOT_DIR$",
			true,
			"jpeg"
		);
	}
);

core.quitStellarium();
	"""

	def __init__(
		self, 
		points,
		screenshot_dir
	):
		self.points = points
		self.screenshot_dir = screenshot_dir

	def create_script(self):
		script = self.SCRIPT

		script = script.replace(
			"$POINTS$", 
			",\n".join('{ ' + str(point) + ' }' for point in self.points)
		)
		script = script.replace(
			"$SCREENSHOT_DIR$", 
			self.screenshot_dir
		)

		file = open("tmp/StellariumScript.ssc", "w")
		file.write(script)
		file.close()

def main(args):
	gpx_file = args[0]
	screenshot_dir = args[1]

	gpx_data = GPXData(gpx_file)

	gpx_data.sample_points()
	gpx_data.set_azimuth()

	script = StellariumScript(
		gpx_data.get_points(),
		screenshot_dir,
	)
	script.create_script()
	
if __name__ == "__main__":
    main(sys.argv[1:])