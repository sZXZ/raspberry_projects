from subprocess import run
from pathlib import Path
from datetime import datetime

def main():
    copy_files(folder_with_photos)
    
def copy_files(folder_with_photos):
    new_name = f"list{datetime.now():%Y%m%d}"
    run(["rclone", "sync", folder_with_photos, f"y:Photos/imports/{new_name}"])
    

if __name__ == "__main__":
    main()
