#!/usr/bin/env python3
import sys
import subprocess
import os
import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QSpinBox, QTextEdit
)
from PySide6.QtCore import QTimer, QThread, Signal

USER_HOME = os.path.expanduser("~")
RAMDISK_CLI = os.path.join(USER_HOME, ".config", "ramdisk-manager", "ramdisk.py")
CONFIG_PATH = os.path.join(USER_HOME, ".config", "ramdisk-manager", "config.json")
RAMDISK_PATH = os.path.join(USER_HOME, "RAMDisk")

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
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

# ---------------- SUBPROCESS ----------------
def run_cmd(cmd, extra_args=None):
    args = [sys.executable, RAMDISK_CLI, cmd]
    if extra_args:
        args += extra_args
    try:
        output = subprocess.check_output(args, stderr=subprocess.STDOUT)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        return f"Error:\n{e.output.decode()}"

# ---------------- THREAD ----------------
class CmdWorker(QThread):
    finished_signal = Signal(str)

    def __init__(self, cmd, args=None):
        super().__init__()
        self.cmd = cmd
        self.args = args

    def run(self):
        res = run_cmd(self.cmd, self.args)
        self.finished_signal.emit(res)

# ---------------- GUI ----------------
class RamdiskGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RAMDisk Manager v1.1 by d3xt3rr0r")
        self.setFixedSize(340, 300)
        self.workers = []
        self.last_cmd = None

        config = load_config()

        self.status_label = QLabel("Status: Unknown")

        self.size_spin = QSpinBox()
        self.size_spin.setRange(1, 1024)
        self.size_spin.setValue(config.get("size_gb", 4))

        self.sync_spin = QSpinBox()
        self.sync_spin.setRange(1, 1440)
        self.sync_spin.setValue(config.get("interval_min", 1))

        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.sync_btn = QPushButton("Sync")

        self.start_btn.clicked.connect(self.start_ramdisk)
        self.stop_btn.clicked.connect(self.stop_ramdisk)
        self.sync_btn.clicked.connect(self.sync_ramdisk)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)

        h1 = QHBoxLayout()
        h1.addWidget(QLabel("RAMDisk Size (GB):"))
        h1.addWidget(self.size_spin)
        layout.addLayout(h1)

        h2 = QHBoxLayout()
        h2.addWidget(QLabel("Auto-Sync Interval (min):"))
        h2.addWidget(self.sync_spin)
        layout.addLayout(h2)

        h3 = QHBoxLayout()
        h3.addWidget(self.start_btn)
        h3.addWidget(self.stop_btn)
        h3.addWidget(self.sync_btn)
        layout.addLayout(h3)

        layout.addWidget(QLabel("Log:"))
        layout.addWidget(self.log_text)

        self.setLayout(layout)

        # STATUS TIMER
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(3000)
        self.update_status()

        # AUTOSYNC TIMER (GUI ONLY)
        self.autosync_timer = QTimer()
        self.autosync_timer.timeout.connect(self.autosync)

    # ---------------- STATUS ----------------
    def update_status(self):
        output = subprocess.getoutput(f"mount | grep {RAMDISK_PATH}")
        if RAMDISK_PATH in output:
            self.status_label.setText("Status: Mounted")
        else:
            self.status_label.setText("Status: Not Mounted")

    # ---------------- AUTOSYNC ----------------
    def autosync(self):
        if "Mounted" not in self.status_label.text():
            return

        self.last_cmd = "autosync"

        worker = CmdWorker("sync")
        worker.finished_signal.connect(self.on_result)
        worker.start()
        self.workers.append(worker)

    # ---------------- ACTIONS ----------------
    def start_ramdisk(self):
        config = {
            "size_gb": self.size_spin.value(),
            "interval_min": self.sync_spin.value()
        }
        save_config(config)

        self.last_cmd = "start"

        worker = CmdWorker("start", [str(config["size_gb"])])
        worker.finished_signal.connect(self.on_result)
        worker.start()
        self.workers.append(worker)

        self.autosync_timer.start(config["interval_min"] * 60 * 1000)

    def stop_ramdisk(self):
        self.autosync_timer.stop()
        self.last_cmd = "stop"

        worker = CmdWorker("stop")
        worker.finished_signal.connect(self.on_result)
        worker.start()
        self.workers.append(worker)

    def sync_ramdisk(self):
        config = {
            "size_gb": self.size_spin.value(),
            "interval_min": self.sync_spin.value()
        }
        save_config(config)

        self.last_cmd = "sync"

        worker = CmdWorker("sync")
        worker.finished_signal.connect(self.on_result)
        worker.start()
        self.workers.append(worker)

        self.autosync_timer.start(config["interval_min"] * 60 * 1000)

    # ---------------- RESULT ----------------
    def on_result(self, res):
        self.log_text.append(res)

        interval = self.sync_spin.value()

        if self.last_cmd in ["start", "sync"]:
            self.log_text.append(f"Auto-Sync enabled ({interval}min)")

        self.update_status()

        for w in self.workers[:]:
            if w.isFinished():
                self.workers.remove(w)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = RamdiskGUI()
    gui.show()
    sys.exit(app.exec())
