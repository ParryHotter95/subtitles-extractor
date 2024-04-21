#!/usr/bin/env python3

import logging
import os
import re
import shutil
import sys
import zipfile

VIDEO_FORMATS = [".mp4", ".mkv", ".avi", ".mov"]
SUBTITLES_FORMATS = [".srt", ".sub", ".txt"]
# it's not being remembered!:
REPLACE_ALL = False


class File:
    def __init__(self, path):
        self.path = path
        self.name, self.extension = os.path.splitext(os.path.basename(path))
        self.is_video = self.extension in VIDEO_FORMATS
        self.is_subtitle = self.extension in SUBTITLES_FORMATS
        self.is_archive = self.extension == ".zip"
        self.episode_number = (
            self._find_episode_number() if self.is_video or self.is_subtitle else None
        )

    def __str__(self):
        return self.path

    def move_to(self, destination):
        old_path = self.path
        new_path = os.path.join(destination, self.name + self.extension)
        # if the file already exists
        if os.path.exists(new_path):
            logging.warning("file %s already exists", new_path)
            global REPLACE_ALL
            logging.debug("replace all: %s", REPLACE_ALL)
            answer = "n"
            if not REPLACE_ALL:
                print("replace existing file? ([y]es / [n]o  /[a]ll)")
                answer = input()
            if answer.lower() == "a":
                REPLACE_ALL = True
            if answer.lower() == "y" or REPLACE_ALL:
                os.remove(new_path)
                shutil.move(old_path, new_path)
            else:
                return
        shutil.move(old_path, new_path)
        self.path = new_path
        logging.debug("moved %s to %s", old_path, new_path)

    def rename(self, new_name):
        # changes the name of the file keeping the extension and path
        old_path = self.path
        new_path = os.path.join(os.path.dirname(old_path), new_name + self.extension)
        # if the file already exists
        if os.path.exists(new_path):
            logging.warning("file %s already exists", new_path)
            global REPLACE_ALL
            logging.debug("replace all: %s", REPLACE_ALL)
            answer = "n"
            if not REPLACE_ALL:
                print("replace existing file? ([y]es / [n]o  /[a]ll)")
                answer = input()
                print("")
            if answer.lower() == "a":
                REPLACE_ALL = True
            if answer.lower() == "y" or REPLACE_ALL:
                logging.info("replacing existing file %s", new_path)
            else:
                # remove extracted file
                logging.debug("removing %s", old_path)
                os.remove(old_path)
                return
        os.replace(old_path, new_path)
        self.path = new_path
        logging.debug("renamed %s to %s", old_path, new_path)

    def _find_episode_number(self):
        # find season number and episode number by matching S<season number> and E<episode number> in filename
        # build regex pattern
        patterns = [r"S[0-9]+E[0-9]+", r"[0-9]+E[0-9]+", r"[0-9]+x[0-9]+"]
        for pattern in patterns:
            pattern = re.compile(pattern)
            # find episode number in filename
            match = re.findall(pattern, self.name)
            if len(match) == 1:
                logging.debug("match in %s ---> %s", self.name, match[0])
                season_num, episode_num = match[0].split("E")
                season_num = int(season_num)
                episode_num = int(episode_num)
                logging.debug(
                    "season number: %d, episode number: %d", season_num, episode_num
                )
                return episode_num
        logging.error("Couldn't find episode number in %s", self.name)
        return None

# set up logging level
if "--verbose" in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


# get selected path
selected_path = sys.argv[1]
logging.info("selected path: %s", selected_path)

# check if selected path exists and is a directory
if not os.path.exists(selected_path):
    logging.error("path %s does not exist", selected_path)
    sys.exit(1)
if not os.path.isdir(selected_path):
    logging.error("path %s is not a directory", selected_path)
    sys.exit(1)

# get the list of files in the selected path
all_files_in_selected_path = [
    File(os.path.join(selected_path, file))
    for file in os.listdir(selected_path)
    if os.path.isfile(os.path.join(selected_path, file))
]
# filter out not compatible files
files_in_selected_path = [
    file for file in all_files_in_selected_path if file.is_archive or file.is_video
]
logging.debug("compatible files in selected path:")
for file in files_in_selected_path:
    logging.debug(file)

# check if there is exactly one archive
archives = [file for file in files_in_selected_path if file.extension == ".zip"]
archive = None
if len(archives) == 1:
    archive = archives[0]
    logging.debug("found archive %s\n", archive)
else:
    if len(archives) > 1:
        logging.error(
            "there should be exactly one archive in the selected path, found %d",
            len(archives),
        )
    if len(archives) == 0:
        logging.error("there is no .zip archive in the selected path")
    sys.exit(1)

videos = [file for file in files_in_selected_path if file.is_video]
logging.debug("videos in selected path:")
for video in videos:
    logging.debug(video)
if len(videos) == 0:
    logging.error("there is no video in the selected path")
    sys.exit(1)

# extract the archive to temporary directory
tmpdir = os.path.join(selected_path, "tmp")
if os.path.exists(tmpdir):
    logging.error("temporary directory %s already exists", tmpdir)
    answer = input("do you want to remove it and continue? [y/N] ")
    if answer.lower() == "y":
        shutil.rmtree(tmpdir)
    else:
        logging.info("exiting")
        sys.exit(1)

os.mkdir(tmpdir)
with zipfile.ZipFile(archive.path) as zf:
    zf.extractall(tmpdir)

# get the list of extracted files in the temporary directory
all_extracted_files = [
    File(os.path.join(tmpdir, file))
    for file in os.listdir(tmpdir)
    if os.path.isfile(os.path.join(tmpdir, file))
]
logging.debug("\nextracted files:")
for file in all_extracted_files:
    logging.debug(file)

# filter out not compatible files
subtitles = [
    file for file in all_extracted_files if file.extension in SUBTITLES_FORMATS
]
logging.debug("\nsubtitles:")
for subtitle in subtitles:
    logging.debug(subtitle)

for video in videos:
    # find subtitle of matching episode number
    if video.episode_number is not None:
        logging.debug("video episode number: %d", video.episode_number)
        matched_subtitle = [
            subtitle
            for subtitle in subtitles
            if subtitle.episode_number == video.episode_number
        ]
        if len(matched_subtitle) == 0:
            logging.warning(
                "no subtitle found for episode number %d", video.episode_number
            )
            break
        if len(matched_subtitle) > 1:
            logging.warning(
                "more than one subtitle found for episode number %d",
                video.episode_number,
            )
            break
        matched_subtitle = matched_subtitle[0]
        logging.info(
            "matched subtitle for episode %s is %s",
            video.episode_number,
            matched_subtitle,
        )
        logging.debug("moving %s to %s", matched_subtitle, selected_path)
        matched_subtitle.move_to(selected_path)
        # new name for the subtitle file, matching the name of the video without the video extension
        matched_subtitle.rename(video.name)

# delete the temporary directory
shutil.rmtree(tmpdir)

# exit
sys.exit(0)
