import time
import os
import subprocess




while True:
    subprocess.call(["python", "scraping_mods.py"])
    time.sleep(60)
    subprocess.call(["python", "uploading.py"])
    time.sleep(60)
    subprocess.call(["python", "building.py"])
    time.sleep(60)
    try:
        os.system("./dropbox_sync.sh")
    except:
        ""
    time.sleep(43200)
