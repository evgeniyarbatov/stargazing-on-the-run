# Stargazing on the Run

Plotting images of stars and planets to learn about what I could have seen in the sky during my early morning runs. It's rare that I get to spot something bright in the sky. When I do, I do not have any way to remember exactly where I was. Luckily, I always carry my GPS watch with me. This is a collection of scripts I have used to plot my location on the map and plot the stars in the sky with Stellarium.

## How to use

Get GPX traces:

```
make gpx
```

Create Stellarium scripts:

```
make scripts
```

Update Stellarium config.ini:

```
# ~/Library/Application\ Support/Stellarium/config.ini
[scripts]
flag_allow_screenshots_dir             = true
```

Run Stellarium scripts to create screenshots:

```
make screenshots
```

Create images with 1) map of the entire map 2) my current location on the map and 3) direction of where I am looking at:

```
make maps
```

Merge Stellarium screenshots and maps into a single image:

```
make merge
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
