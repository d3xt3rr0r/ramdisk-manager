#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import shutil

USER_HOME = os.path.expanduser("~")
CONFIG_PATH = os.path.join(USER_HOME, ".config", "ramdisk-manager", "config.json")
RAMDISK_PATH = os.path.join(USER_HOME, "RAMDisk")
RAMDISK_DATA = os.path.join(USER_HOME, "RAMDisk_data")

DEFAULT_CONFIG = {"size_gb": 4, "interval_min": 1}


# ---------------- CONFIG ----------------
def load_config():
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        print("Warning: config.json corrupted, restoring default")
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG


def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)


# ---------------- SYNC ----------------
def sync_to_data():
    if not os.path.exists(RAMDISK_PATH):
        return

    os.makedirs(RAMDISK_DATA, exist_ok=True)

    subprocess.run([
        "rsync",
        "-rl",
        "--delete",
        RAMDISK_PATH + "/",
        RAMDISK_DATA + "/"
    ], check=True)


def restore_to_ramdisk():
    if not os.path.exists(RAMDISK_DATA):
        return
    if not os.path.exists(RAMDISK_PATH):
        return

    subprocess.run([
        "rsync",
        "-rl",
        RAMDISK_DATA + "/",
        RAMDISK_PATH + "/"
    ], check=True)


# ---------------- RAMDISK ----------------
def mount_ramdisk(size_gb):
    os.makedirs(RAMDISK_PATH, exist_ok=True)

    mounts = subprocess.getoutput("mount")
    if RAMDISK_PATH in mounts:
        print("RAMDisk already mounted")
        return

    try:
        subprocess.run(
            [
                "pkexec",
                "mount", "-t", "tmpfs", "-o", f"size={size_gb}G", "tmpfs", RAMDISK_PATH
            ],
            check=True
        )
        print(f"RAMDisk created: {RAMDISK_PATH} ({size_gb}GB)")
    except subprocess.CalledProcessError as e:
        print(f"Error mounting RAMDisk: {e}")
    except FileNotFoundError:
        print("Error: pkexec not available - install `polkit` or use sudo in terminal")


def remove_ramdisk():
    if os.path.exists(RAMDISK_PATH):
        try:
            subprocess.run(
                ["pkexec", "umount", RAMDISK_PATH],
                check=True
            )
        except subprocess.CalledProcessError:
            try:
                subprocess.run(
                    ["pkexec", "umount", "-l", RAMDISK_PATH],
                    check=True
                )
            except subprocess.CalledProcessError:
                print("Unmounting RAMDisk failed - try manually")
                return

        shutil.rmtree(RAMDISK_PATH, ignore_errors=True)
        print("Unmounted and deleted RAMDisk")


# ---------------- COMMANDS ----------------
def start_ramdisk(size_gb=None):
    config = load_config()

    if size_gb is not None:
        config["size_gb"] = size_gb
        save_config(config)
        mount_size = size_gb
    else:
        mount_size = config["size_gb"]

    mount_ramdisk(mount_size)
    restore_to_ramdisk()
    print("Synchronization: RAMDisk_data ==> RAMDisk")


def stop_ramdisk():
    sync_to_data()
    print("Synchronization: RAMDisk ==> RAMDisk_data")
    remove_ramdisk()


def sync_ramdisk():
    os.makedirs(RAMDISK_DATA, exist_ok=True)
    sync_to_data()
    print("Synchronization: RAMDisk ==> RAMDisk_data")


def launch_gui():
    gui_path = os.path.join(os.path.dirname(__file__), "gui.py")

    if not os.path.exists(gui_path):
        print("Error: gui.py not found")
        sys.exit(1)

    try:
        subprocess.Popen(["python3", gui_path])
    except Exception as e:
        print(f"Error launching GUI: {e}")


# ---------------- CLI ----------------
def parse_size_arg():
    if len(sys.argv) < 3:
        return None

    raw = sys.argv[2].strip()
    if raw == "":
        return None

    try:
        return int(raw)
    except ValueError:
        print("Error: size must be an integer")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  ramdisk-manager start [sizeGB]")
        print("  ramdisk-manager stop")
        print("  ramdisk-manager sync")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "start":
        size = parse_size_arg()
        start_ramdisk(size)

    elif cmd == "stop":
        stop_ramdisk()

    elif cmd == "sync":
        sync_ramdisk()

    elif cmd == "gui":
        launch_gui()

    else:
        print("Unknown command")
