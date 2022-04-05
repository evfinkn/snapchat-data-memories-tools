import exiftool
import os
import re
import time
from datetime import datetime, timedelta, timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

downloads_folder = os.path.dirname(os.path.abspath(__file__)) + "\\Memories"
file_created = False
file_location = None
last_modified = 0

regex = re.compile(r"\.\S{3,4}$")
dash = re.compile(r"-")


class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        global file_created, file_location
        if regex.search(event.src_path).group(0).casefold() == ".PART".casefold():
            return
        file_created = True
        file_location = event.src_path

    def on_modified(self, event):
        global last_modified
        if dash.search(event.src_path) is not None and regex.search(event.src_path).group(0).casefold() != ".PART".casefold():
            last_modified = time.time()


def rename_file(original_file_path, new_file_path):
    try:
        os.rename(src=original_file_path, dst=new_file_path)
        return True
    except FileExistsError:
        return False


options = Options()
options.headless = True
options.set_preference(name="browser.download.folderList", value=2)
options.set_preference(name="browser.download.useDownloadDir", value=True)
options.set_preference(name="browser.download.lastDir", value=downloads_folder)
options.set_preference(name="browser.download.dir", value=downloads_folder)
options.set_preference(name="media.play-stand-alone", value=False)

driver = webdriver.Firefox(options=options)
driver.get("file:///" + os.path.dirname(os.path.abspath(__file__)) + "/memories_history.html")

rows = driver.find_elements(by=By.TAG_NAME, value="tr")
rows.pop(0)
columns = [row.find_elements(by=By.TAG_NAME, value="td") for row in rows]
dates = [column[0] for column in columns]
types = [column[1] for column in columns]
links = [column[2].find_element(by=By.TAG_NAME, value="a") for column in columns]

event_handler = EventHandler()
observer = Observer()
observer.schedule(event_handler=event_handler, path=downloads_folder, recursive=False)
observer.start()

for x in range(len(links)):

    links[x].click()
    while not file_created:
        time.sleep(0.25)
    time.sleep(1.5)

    if types[x].text == "Video":
        while last_modified == 0 or time.time() - last_modified < 3.5:
            time.sleep(3.5)

    dt = [int(group) for group in re.split("[- :]", dates[x].text[:-4])]
    dt = datetime(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], 0, timezone.utc)
    dt = dt.astimezone()

    second_increment = 1
    while not rename_file(file_location, downloads_folder + "\\" + dt.strftime("%Y%m%d%H%M%S") + regex.search(file_location).group(0)):
        dt = dt + timedelta(seconds=-second_increment)
        second_increment += 1

    file_created = False
    last_modified = 0
    time.sleep(1)

observer.stop()
observer.join()
driver.close()

try:
    with exiftool.ExifToolHelper(common_args=None) as et:
        print(et.execute("-overwrite_original_in_place", "-EXIF:AllDates<basename", "-FileCreateDate<basename", "-FileModifyDate<basename", downloads_folder))
except exiftool.exceptions.ExifToolExecuteError as err:
    print("cmd:")
    print(err.cmd)

    print("\nstdout:")
    print(err.stdout)

    print("\nstderr:")
    print(err.stderr)

    raise
