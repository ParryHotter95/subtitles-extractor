# sub-extractor.py
This is simple Python 3 script for extracting subtitles from .zip archive for the entire TV show season, renaming extracted subtitle files to match video filenames.
## Usage example
Imagine that `test` folder is your `Season 2` folder containg video files of your TV show episode.

`test` was populated by empty files named as video files of *Orphan Black* shows season 2 for a demonstration.

You download subtitles pack in .zip archive to the same folder. There might be additional files of different filetypes in this folder - in this example: ` not_a_movie.jpg` and ` not_a_movie_without_extension`.

`ls test/
 not_a_movie.jpg
 not_a_movie_without_extension
'Orphan Black (2013) - S02E01 - Nature Under Constraint and Vexed (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E02 - Governed By Sound Reason and True Religion (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E03 - Mingling Its Own Nature with It (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E04 - Governed As It Were By Chance (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E05 - Ipsa Scientia Potestas Est (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E06 - To Hound Nature in Her Wanderings (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E07 - Knowledge of Causes, and Secret Motion of Things (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E08 - Variable and Full of Perturbation (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E09 - Things Which Have Never Yet Been Done (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E10 - By Means Which Have Never Yet Been Tried (1080p BluRay x265 Ghost).mkv'
 orphan-black-second-season_english-1590736.zip

Archive content is:  
`$ zipinfo -1 test/orphan-black-second-season_english-1590736.zip
Orphan.Black.S02E01.HDTV.x264-LOL.srt
Orphan.Black.S02E02.HDTV.x264-KILLERS.srt
Orphan.Black.S02E03.HDTV.x264-LOL.srt
Orphan.Black.S02E04.HDTV.x264-2HD.srt
Orphan.Black.S02E05.HDTV.x264.KILLERS.srt
Orphan.Black.S02E06.HDTV.x264.KILLERS.srt
Orphan.Black.S02E07.HDTV.x264-LOL.srt
Orphan.Black.S02E08.HDTV.x264-KILLERS.srt
Orphan.Black.S02E09.HDTV.x264-2HD.HI.srt
Orphan.Black.S02E10.HDTV.x264-LOL.srt`

 You need to extract them, but also rename it, so the filename of subtitle is the same as video name. This allows various video players to automatically open the subtitles if there's a subtitle file of a name matching video filename in the same folder.

 You just run a script, passing a path:
 `$ python3 sub-extractor.py ./test
INFO:root:selected path: ./test
INFO:root:matched subtitle for episode 1 is ./test/tmp/Orphan.Black.S02E01.HDTV.x264-LOL.srt
INFO:root:matched subtitle for episode 2 is ./test/tmp/Orphan.Black.S02E02.HDTV.x264-KILLERS.srt
INFO:root:matched subtitle for episode 3 is ./test/tmp/Orphan.Black.S02E03.HDTV.x264-LOL.srt
INFO:root:matched subtitle for episode 4 is ./test/tmp/Orphan.Black.S02E04.HDTV.x264-2HD.srt
INFO:root:matched subtitle for episode 5 is ./test/tmp/Orphan.Black.S02E05.HDTV.x264.KILLERS.srt
INFO:root:matched subtitle for episode 6 is ./test/tmp/Orphan.Black.S02E06.HDTV.x264.KILLERS.srt
INFO:root:matched subtitle for episode 7 is ./test/tmp/Orphan.Black.S02E07.HDTV.x264-LOL.srt
INFO:root:matched subtitle for episode 8 is ./test/tmp/Orphan.Black.S02E08.HDTV.x264-KILLERS.srt
INFO:root:matched subtitle for episode 9 is ./test/tmp/Orphan.Black.S02E09.HDTV.x264-2HD.HI.srt
INFO:root:matched subtitle for episode 10 is ./test/tmp/Orphan.Black.S02E10.HDTV.x264-LOL.srt`

It extracts .zip file into temporary `/temp` folder, and extract episode name from filenames containing string like `S02E01`.

As a result for each episode, i.e. `Orphan Black (2013) - S02E01 - Nature Under Constraint and Vexed (1080p BluRay x265 Ghost).mkv` there is corresponding subtitle file `Orphan Black (2013) - S02E01 - Nature Under Constraint and Vexed (1080p BluRay x265 Ghost).srt` having the same name, but keeping it's original extensions.

Full content of a folder after running the script:

`$ ls ./test/
 not_a_movie.jpg
 not_a_movie_without_extension
'Orphan Black (2013) - S02E01 - Nature Under Constraint and Vexed (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E01 - Nature Under Constraint and Vexed (1080p BluRay x265 Ghost).srt'
'Orphan Black (2013) - S02E02 - Governed By Sound Reason and True Religion (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E02 - Governed By Sound Reason and True Religion (1080p BluRay x265 Ghost).srt'
'Orphan Black (2013) - S02E03 - Mingling Its Own Nature with It (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E03 - Mingling Its Own Nature with It (1080p BluRay x265 Ghost).srt'
'Orphan Black (2013) - S02E04 - Governed As It Were By Chance (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E04 - Governed As It Were By Chance (1080p BluRay x265 Ghost).srt'
'Orphan Black (2013) - S02E05 - Ipsa Scientia Potestas Est (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E05 - Ipsa Scientia Potestas Est (1080p BluRay x265 Ghost).srt'
'Orphan Black (2013) - S02E06 - To Hound Nature in Her Wanderings (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E06 - To Hound Nature in Her Wanderings (1080p BluRay x265 Ghost).srt'
'Orphan Black (2013) - S02E07 - Knowledge of Causes, and Secret Motion of Things (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E07 - Knowledge of Causes, and Secret Motion of Things (1080p BluRay x265 Ghost).srt'
'Orphan Black (2013) - S02E08 - Variable and Full of Perturbation (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E08 - Variable and Full of Perturbation (1080p BluRay x265 Ghost).srt'
'Orphan Black (2013) - S02E09 - Things Which Have Never Yet Been Done (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E09 - Things Which Have Never Yet Been Done (1080p BluRay x265 Ghost).srt'
'Orphan Black (2013) - S02E10 - By Means Which Have Never Yet Been Tried (1080p BluRay x265 Ghost).mkv'
'Orphan Black (2013) - S02E10 - By Means Which Have Never Yet Been Tried (1080p BluRay x265 Ghost).srt'
 orphan-black-second-season_english-1590736.zip`

## Syntax
`python3 sub-extractor.py /target/directory [--verbose]`

`/target/directory` should contain video files of one of the types: `VIDEO_FORMATS = [".mp4", ".mkv", ".avi", ".mov"]` and exactly one `*.zip` containing subtitles files with extensions `SUBTITLES_FORMATS = [".srt", ".sub", ".txt"]`

Adding `--verbose` flag will show you detailed output if you want to inspect script's behavior.


## Limitations and TO-DO
- Currently only one season can be processed at the time - script only extracts episode number from filenames, but ignores season number. For example if our `test/orphan-black-second-season_english-1590736.zip` file would contain `*S03E01*.srt` file instead of `*S02E01*.srt`, it would still match its name to `Orphan Black (2013) - S02E01 -*.mkv`
- there are hardcoded file formats which are being recognized as subtitles and videos