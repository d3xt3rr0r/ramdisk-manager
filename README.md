
---

<h1 align="center">RAMDisk Manager v1.1</h1>
<p align="center">
  <a href="https://www.python.org/downloads/release/python-38/">
    <img alt="Python" src="https://img.shields.io/badge/python-3.8%2B-blue.svg?logo=python&logoColor=white">
  </a>
  <a href="https://www.gnu.org/software/bash/">
    <img alt="Shell" src="https://img.shields.io/badge/shell-bash-brightgreen?logo=gnu-bash">
  </a>
  <a href="https://github.com/d3xt3rr0r/ramdisk-manager/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/d3xt3rr0r/ramdisk-manager?color=green">
  </a>
</p>

<p align="center">
  <strong>Simple & efficient RAMDisk manager for Linux — with CLI and modern GUI</strong><br>
  💾 Creates volatile in-RAM filesystems, enables safe data persistence via sync with persistent storage, and features 
one-click GUI control.
</p>

---

## ✨ Features

- 🧠 **RAM-based storage** — Create high-speed, volatile `tmpfs` disks of configurable size
- 🔄 **Bi-directional sync** — Automatic and manual sync between RAM disk and persistent `RAMDisk_data/` folder
- 🖥 **Dual interfaces** — Full CLI for scripting & terminal workflows + modern GUI (built with PySide6) for daily use
- 🔒 **Secure password handling** — Uses `pkexec` for privileged operations — no terminal password input needed
- ⏱ **Auto-sync scheduling** — Configure periodic sync intervals in GUI (CLI requires manual triggers)
- 📊 **Real-time status** — GUI logs mount state, sync history, and warnings

---

## 📋 Requirements

| Component | Requirement |
|-----------|-------------|
| OS        | Linux (tested on Ubuntu, Fedora, Arch) |
| Python    | ≥ 3.8 (`python3 --version`) |
| Runtime   | `rsync`, `mount`, `umount` (standard on all major distros) |
| GUI       | `polkit` + `pkexec` (for secure sudo-equivalent auth) <br> *Optional: `zenity`/`yad` for fallback auth 
| GUI lib   | `PySide6` (`pip install PySide6`) |

> 💡 **Note**: `pkexec` is required for the GUI's *mount/umount* buttons. If missing, the app will fall back to 
warning the user (CLI still works with `sudo`).

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/d3xt3rr0r/ramdisk-manager.git
cd ramdisk-manager
```

### 2. Make the wrapper executable
```bash
chmod +x run.sh
```

### 3. Install GUI dependency (if using GUI)
```bash
pip install --user PySide6
```

---

## 💻 Usage

### CLI Commands
First run via `./run.sh` and wrapper will be installed to ~/.local/bin.

| Command | Description |
|---------|-------------|
| `ramdisk-manager start [sizeGB]` | Mount RAM disk of given size (default: from `config.json`) |
| `ramdisk-manager stop` | Sync RAM → persistent store, then unmount & delete |
| `ramdisk-manager sync` | One-time RAM → persistent sync (CLI-only) |
| `ramdisk-manager gui` | Launch GUI (requires PySide6) |

> ⚠ **Root permissions** are requested via GUI dialog or terminal (via `pkexec`/`sudo`).  
> 📝 **Config** is stored in `~/.config/ramdisk-manager/config.json`  
> 📁 **Paths**:  
> - RAM disk: `~/RAMDisk/`  
> - Persistent backup: `~/RAMDisk_data/`

---

### 🖥 GUI Interface
Launch with:
```bash
ramdisk-manager gui
```

#### Main controls:
- 🔲 **Mount RAMDisk**: Set size in GB (1-1024) & click *Start*  
- ⏹ **Unmount**: Click *Stop* (triggers sync first)  
- 🔄 **Sync Now**: One-time manual sync  
- ⏱ **Auto-sync interval**: Minutes (1-1440)  
- 📜 **Log Panel**: Real-time terminal output  
- 🛠 **Config editor**: Adjust defaults (size, interval)  
- ℹ **Status**: Shows mount state & sync last run time  

![GUI mockup](https://i.imgur.com/RYFEZlC.png)  

---

## 🗂 Project Structure

```
ramdisk-manager/
├── ramdisk.py         # Core CLI logic (mount/umount/sync)
├── gui.py             # PySide6 GUI (configurable widgets + logs)
├── run.sh             # Bash wrapper (imports/invokes ramdisk.py)
├── config.json        # Sample config (auto-generated on first run)
├── README.md          # This file
└── LICENSE            # MIT License
```

> 🔧 All paths are relative to `$HOME`. No system-wide changes made.

---

## 📌 Notes & Troubleshooting

| Issue | Solution |
|-------|----------|
| `pkexec` not found | Install `polkit` (`sudo apt install polkit`, `sudo pacman -S polkit`, etc.) |
| GUI fails to start | Check: `python3 -m PySide6` → install `PySide6` if missing |
| Sync fails with `rsync` error | Ensure `rsync` installed: `sudo apt install rsync` |
| Already mounted | CLI prints warning; GUI shows current state & disables mount button |

---

## 📄 License

Distributed under the **[MIT License](https://github.com/d3xt3rr0r/ramdisk-manager/blob/main/LICENSE)**.  
© 2024 [d3xt3rr0r](https://github.com/d3xt3rr0r)

---

<p align="center">
  <i>Happy RAM-hacking! 🧠💾🚀</i><br>
  <sub>Feedback, PRs & issues welcome!</sub>
</p>

---

