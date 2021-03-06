# Stargazing on the Run

Plotting images of stars and planets to learn about what I could have seen in the sky during my early morning runs. It's rare that I get to spot something bright in the sky. When I do, I do not have any way to remember exactly where I was. Luckily, I always carry my GPS watch with me. This is a collection of scripts I have used to plot my location on the map and plot the stars in the sky with Stellarium.

## How to use

I use Stellarium to generate images of the sky. With Stellarium scripts I can specify the time / location / bearing and take a screenshot. The first step is to create generate Stellarium script for a given GPX file:

```
python3 \
scripts/create_stellarium_script.py \
gpx_data/Morning_Run.gpx \
/Users/arbatov/gitRepo/stargazing-on-the-run/tmp/sky_images
```

Create images with 1) map of the entire map 2) my current location on the map and 3) direction of where I am looking at:

```
python3 \
scripts/make_maps.py \
gpx_data/Morning_Run.gpx
```

Run Stellarium script to create screenshots:

```
/Applications/Stellarium.app/Contents/MacOS/stellarium \
--startup-script /Users/arbatov/gitRepo/stargazing-on-the-run/tmp/StellariumScript.ssc \
--screenshot-dir /Users/arbatov/gitRepo/stargazing-on-the-run/tmp/sky_images
```

Merge Stellarium screenshots and maps into a single image:

```
python3 \
scripts/merge_images.py
```

Create video

```
cd tmp/sky_and_map_images
ffmpeg \
-framerate 5 \
-pattern_type glob -i '*.png' \
-c:v libx264 \
-pix_fmt yuv420p \
../video/sky_video.mp4
```
