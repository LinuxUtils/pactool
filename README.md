![PACTOOL BANNER](https://github.com/LinuxUtils/paktool/blob/main/graphics/PACTOOL_BANNER.png?raw=true)

# What is Pactool?
#### PacTool is a simple and powerful package management helper designed for **Arch Linux** and **Debian-based distributions**. It provides a clear overview of all installed packages and offers tools to optimize your system by managing package sizes and kernel versions.


---

## **Features**
- **Cross-distro support** (Arch Linux and Debian/Ubuntu).
- List all installed packages with pagination and sorting.
- **Filter packages** (user-installed or system).
- Search, install, uninstall, update, and upgrade packages.
- **Mirror management**:  
  - Show current mirrors with latency and last-updated info.  
  - Automatically update to the fastest mirrors.  
  - Backup and revert mirrors with timestamps.  
- **Reverse dependency tree**: `--why PACKAGE`.
- **File listing**: `--files PACKAGE` (lists all files installed by a package).
- **Cache cleaning**: `--clean`.
- Manual mirror backups: `--backup-mirrors`.
- Color-coded, formatted output.

---

### Run Directly
```bash
python3 pactool.py --help
```

### Add Pactool to PATH
```bash
sudo cp pactool.py /usr/local/bin/pactool
sudo chmod +x /usr/local/bin/pactool
```

### Requirements
- Python 3.8+
- `reflector` (Arch Linux) or `netselect-apt` (Debian/Ubuntu) for mirror management.
- `dpkg`, `apt`, or `pacman` must be installed based on your distro.

---

## **Basic Usage**
```bash
python3 pactool.py [COMMANDS] [OPTIONS]
```

### **Examples**
```bash
# Show all installed packages
python3 pactool.py --list

# Show only 20 packages
python3 pactool.py --list -n 20

# Search for 'firefox'
python3 pactool.py --search firefox

# Install VLC
python3 pactool.py --install vlc

# Uninstall VLC
python3 pactool.py --uninstall vlc

# Update all packages
python3 pactool.py --update

# Upgrade system
python3 pactool.py --upgrade
```

---

## **Package Management**

### **List Packages**
Display installed packages with pagination and sorting:
```bash
python3 pactool.py --list -n 30
```
Sort by name:
```bash
python3 pactool.py --list --sort name
```
Reverse sort by size:
```bash
python3 pactool.py --list --rsort size
```

### **Search Packages**
```bash
python3 pactool.py --search vlc
```

---

## **Mirror Management**

### **Show Current Mirrors**
Displays active mirrors with **response time** and **last updated**:
```bash
python3 pactool.py --show-mirrors
```
**Sample Output:**
```
[✔]  https://mirror.osbeck.com/archlinux/$repo/os/$arch         124.42 ms    (Last Updated: Fri, 18 Jul 2025 14:38:24 GMT)
[✔]  https://mirror.cyberbits.eu/archlinux/$repo/os/$arch       738.60 ms    (Last Updated: Fri, 18 Jul 2025 13:30:26 GMT)
[✔]  https://mirror.ubrco.de/archlinux/$repo/os/$arch           949.06 ms    (Last Updated: N/A)
```

### **Update to Fastest Mirrors**
```bash
python3 pactool.py --update-mirrors
```

### **Backup Mirrors**
```bash
python3 pactool.py --backup-mirrors
```
Backups stored in:
```
~/.cache/pactool/mirrors/
```

### **Revert Mirrors**
```bash
python3 pactool.py --revert-mirrors
```
**Example:**
```
Available backups:
(1) Friday, 18 July 2025 at 05:42:54
(2) Friday, 18 July 2025 at 05:44:15

Which backup would you like? (ID) > 2
Reverted mirrors to 2025-07-18_05-44-15
```

---

## **Advanced Commands**

### **Reverse Dependency Tree**
```bash
python3 pactool.py --why firefox
```
**Output:**
```
Reverse dependency tree for 'firefox':

firefox
  └─ gnome-browser
    └─ gnome-desktop
```

### **List Files Installed by a Package**
```bash
python3 pactool.py --files vlc
```
**Example:**
```
Files installed by 'vlc':
    /usr/bin/vlc
    /usr/share/applications/vlc.desktop
    /usr/share/icons/hicolor/48x48/apps/vlc.png
```

### **Clean Cache**
```bash
python3 pactool.py --clean
```
Cleans cache safely and prompts before deletion.

---

## **Command Overview**
```
--list              List installed packages
--stats             Show package statistics
--search NAME       Search for a package
--install PACKAGE   Install a package
--uninstall PACKAGE Uninstall a package
--update            Update all packages
--upgrade           Upgrade all packages
--files PACKAGE     List files installed by a package
--why PACKAGE       Show reverse dependencies
--clean             Clean package manager cache
--show-mirrors      Show current mirrors
--update-mirrors    Update to fastest mirrors
--backup-mirrors    Backup current mirror list
--revert-mirrors    Revert mirrors to a backup
```

---

## **Tips and Tricks**
- Use `--user` to only list user-installed packages.
- Combine `--list` with `--sort` for a quick overview.
- Backup mirrors before performing big updates.
- Use `--why` to diagnose why unnecessary packages are installed.

---

## **Roadmap / Planned Features**
- `--owns FILE`: Find which package owns a file.
- `--orphans`: List orphaned packages.
- `--kernel-clean`: Remove old kernels on APT.
- `--size`: Show disk usage.
- Interactive shell: `pactool shell`.

---

## **Troubleshooting**
**Q:** Pactool says `reflector` is missing.  
**A:** Install it with:
```bash
sudo pacman -S reflector
```
(For Debian use `sudo apt install netselect-apt`.)

**Q:** Permission errors on mirror updates?  
**A:** Run with `sudo` or `sudo -E`.

---

## **Contributing**
We welcome contributions! Fork the repo, create a branch, and submit a PR.

---

## **License**
MIT License - see LICENSE file.