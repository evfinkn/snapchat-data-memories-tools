# To-do list

### Top priority
- [ ] Finish README.md
  - [ ] Installation instructions
    - [ ] Link to Selenium and geckodriver
	- [ ] Link to Watchdog
	- [ ] Link to ExifTool
  - [ ] Usage instructions
    - [ ] How to run in console
  - [ ] Add note that images and videos made at exact same time will change to have a difference of 1 second each
  - [ ] Note that 
- [ ] Add comments to code
- [ ] Finish create_html.py
- [ ] Remove PyExifTool dependency and use subprocess module instead

### Medium priority
- [ ] Create sample memories_history.html file for example usage and result
- [ ] Add options to program allowing to skip certain steps
  - [ ] download_memories.py
    - [ ] Option to not rename files
    - [ ] Option to not change file dates
  - [ ] create_thumbnails.py
    - [ ] Options for thumbnail size
  - [ ] create_html.py
    - [ ] Option to not use thumbnails
	- [ ] Option to use local timezone (or input timezone)
    - [ ] Option to make HTML with clicking on an image thumbnail expand into the full image
	- [ ] Option to embed images and videos anyway (using expansion technique on point above this one)
  - [ ] Add new arguments to README.md as implemented
- [ ] Add note to README.md that the original plan was to have the actual images and videos on the webpage, but Firefox doesn't support videos encoded with HEVC
- [ ] Possibly make FFmpeg script that transcodes videos, even though not recommended (very time consuming to transcode)
