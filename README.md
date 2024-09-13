# Stargazing on the Run

Plotting images of stars and planets to learn about what I could have seen in the sky during my early morning and late night runs. 

I have used Stellarium scripts to render stars and planets based on GPX file location and my direction.

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

Create Stellarium screenshots:

```
make screenshots
```

Create images with the map:

```
make maps
```

Merge Stellarium screenshots and maps into a single image:

```
make merge
```

Create videos:

```
make videos
```
