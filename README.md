# Snapchat Data Memories Tools
When you download your Snapchat data, instead of coming with your memories, you are only provided a list of links to download your memories. I wrote these python scripts to make this easier. 

### download_memories.py
To use this script, move the memories_history.html file from your Snapchat data to the same directory as this script. The Selenium, Watchdog, and PyExifTool (which needs ExifTool) are required to run this script. It uses Selenium to grab the links from the HTML file and click them to download the files as well as to get the dates of each file. Watchdog waits for the file to download and returns the filename to make renaming the file possible. Finally, ExifTool is used to change the metadata of the files to use the correct dates.

### create_thumbnails.py
This creates thumbnails of the images and videos to be used in a new HTML file (made by the next script). Requires FFmpeg.

### create_html.py
Generates a new memories_history.html file with thumbnails of the images / videos, as well as functionality for hiding the different file types, sorting, and copying the filepath of a file to your clipboard.
