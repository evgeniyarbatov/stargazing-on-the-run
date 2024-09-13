include ../api-secrets/gpxdata.env
export $(shell sed 's/=.*//' ../api-secrets/gpxdata.env)

PROJECT_NAME := $(shell basename $(PWD))
VENV_PATH = ~/.venv/$(PROJECT_NAME)

GPX_DIR = gpx
STELLARIUM_SCRIPTS_DIR = stellarium-scripts

SCREENSHOT_DIR = ~/Downloads/stellarium
MAPS_DIR = ~/Downloads/stellarium-maps

MERGED_DIR = ~/Downloads/stellarium-with-maps
VIDEO_DIRS := $(wildcard $(MERGED_DIR)/*)

TIMEZONE = Asia/Ho_Chi_Minh

STELLARIUM_SCRIPTS := $(wildcard $(STELLARIUM_SCRIPTS_DIR)/*.ssc)

all: venv install jupyter

venv:
	@python3 -m venv $(VENV_PATH)

install: venv
	@source $(VENV_PATH)/bin/activate && \
	pip install --disable-pip-version-check -q -r requirements.txt

jupyter: install
	@source $(VENV_PATH)/bin/activate && \
	python3 -m ipykernel install \
	--user \
	--name "$(PROJECT_NAME)" \
	--display-name "$(PROJECT_NAME)" \
	> /dev/null 2>&1

gpx:
	@mkdir -p $(GPX_DIR)

	@echo "*" > $(GPX_DIR)/.gitignore
	@echo "!.gitignore" >> $(GPX_DIR)/.gitignore

	@gdown --folder https://drive.google.com/drive/folders/$(GPX_FOLDER_ID) -O $(GPX_DIR)

scripts:
	@source $(VENV_PATH)/bin/activate && \
	python3 scripts/create-scripts.py \
	$(GPX_DIR) \
	$(TIMEZONE) \
	$(STELLARIUM_SCRIPTS_DIR) \
	$(SCREENSHOT_DIR)

screenshots:
	@for file in $(STELLARIUM_SCRIPTS); do \
		script_path=$$(realpath $$file); \
		/Applications/Stellarium.app/Contents/MacOS/stellarium --startup-script $$script_path; \
	done

maps:
	@source $(VENV_PATH)/bin/activate && \
	python3 scripts/make-maps.py \
	$(GPX_DIR) \
	$(TIMEZONE) \
	$(MAPS_DIR)

merge:
	@source $(VENV_PATH)/bin/activate && \
	python3 scripts/merge.py \
	$(GPX_DIR) \
	$(SCREENSHOT_DIR) \
	$(MAPS_DIR) \
	$(MERGED_DIR)

videos: $(VIDEO_DIRS)

$(VIDEO_DIRS):
	@cd $@ && \
	echo "Processing $@..." && \
	ffmpeg \
	-framerate 5 \
	-pattern_type glob -i '*.png' \
	-c:v libx264 \
	-pix_fmt yuv420p \
	video.mp4

.PHONY: venv install jupyter gpx scripts screenshots maps merge videos