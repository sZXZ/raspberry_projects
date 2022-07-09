from subprocess import run
from pathlib import Path
from datetime import datetime
import shutil

def main():
    mount_drives()
    path = copy_to_ssd()
    upload_files(path)
    analize()
    thumbnails()
    mongo_db
    backup
    
def upload_files(folder_with_photos):
    run(["rclone", "sync", str(folder_with_photos), f"y:Photos/imports/{folder_with_photos.name}"])
    
def mount_drives():
    lsblk = run(["sudo","lsblk"], capture_output=True).stdout.decode().split('\n')
    for line in lsblk:
        if 'part' in line:
            if '118.4G' in line and len(line.split())<7:
                mount = line.split(' ')[0].replace('└─','')
                print((line.split()))
                run(["sudo", "mount", f"/dev/{mount}", "/home/ubuntu/ssd"])
            if '29.8G' in line and len(line.split())<7:
                mount = line.split(' ')[0].replace('└─','')
                run(["sudo", "mount", f"/dev/{mount}", "/home/ubuntu/camera_drive"])
                
def copy_to_ssd():
    camera_folder = Path('/home/ubuntu/camera_drive/DCIM/')
    folder_name = f"upload_{datetime.now():%Y%m%d}"
    new_path = Path(f'/home/ubuntu/ssd/ph/{folder_name}')
    new_path.mkdir(exist_ok=True)
    for file in camera_folder.glob('*/*'):
        name = file.name
        shutil.move(file, new_path.joinpath(name))
    return new_path
    
    
if __name__ == "__main__":
    main()
