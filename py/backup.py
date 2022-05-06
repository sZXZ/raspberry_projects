from subprocess import run

if __name__ == "__main__":
    notebook_folders = [
        "bot",
        "cooking",
        "games",
        "gd",
        "hdd",
        "health",
        "photo",
        "tests",
        "in.ipynb",
    ]

    for folder in notebook_folders:
        cmd = [
            "rclone",
            "sync",
            f"/home/ubuntu/notebook/{folder}",
            f"y:pi/{folder}",
            # "--dry-run",
        ]
        if folder in "photo":
            cmd.extend(["--exclude", "thumbnails**"])
        run(cmd)
    
    run(["rclone","sync", "out=/home/ubuntu/py", "y:pi/py"])
    run(["mongodump", "--out=/home/ubuntu/backup/", "--gzip"])
    run(["rclone", "sync", f"/home/ubuntu/backup", "y:pi/backup"])
