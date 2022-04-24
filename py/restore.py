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
            f"y:pi/{folder}",
            f"/home/ubuntu/notebook/{folder}",
            "--dry-run",
        ]
        if folder in "photo":
            cmd.extend(["--exclude", "thumbnails**"])
        run(cmd)

    run(["rclone", "sync", "y:pi/backup", "/home/ubuntu/backup"])
    run(["mongorestore", "/home/ubuntu/backup/", "--gzip"])
