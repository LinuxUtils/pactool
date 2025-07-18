![PACTOOL BANNER](https://github.com/LinuxUtils/paktool/blob/main/graphics/PACTOOL_BANNER.png?raw=true)

# What is Pactool?
#### PacTool is a versatile, simple, and powerful package management helper designed for **Arch Linux** and **Debian-based distributions**. It provides a clear and modern overview of all installed packages, their sizes, and dependencies, and offers various tools to optimize and maintain your system efficiently.

---

## **Features**
- **Cross-distro support** for Arch Linux, Manjaro, Debian, Ubuntu, and other derivatives.
- **Advanced package listing** with pagination, sorting (name, size, type), and filtering (user/system packages).
- Full **search, install, uninstall, update, and upgrade** commands.
- **Mirror management** with support for automatic backups and restores:
  - Show current mirrors with latency checks and timestamps.
  - Auto-update mirrors to the fastest available servers.
  - Backup and revert mirrors using timestamped snapshots.
- **Dependency & reverse dependency tree** analysis via `--why PACKAGE`.
- **File ownership**: list all files installed by a package with `--files PACKAGE`.
- **Cache cleaning** with safe prompts.
- **Kernel utilities**:
  - `--cleanup-kernels` for removing outdated kernels safely.
  - `--backup-kernel` to backup the current kernel and initramfs.
- **Color-coded, human-friendly output** for better readability.
- Detailed **statistics** with `--stats` to understand package count, disk usage, and outdated software.
- **Interactive confirmations** for critical actions like upgrades, removals, or mirror changes.

---

## **Installation & Setup**

### Run Directly
```bash
python3 pactool.py --help
```

### Add Pactool to PATH (Global Install)
```bash
sudo cp pactool.py /usr/local/bin/pactool
sudo chmod +x /usr/local/bin/pactool
```

### Requirements
- **Python 3.8+**
- `reflector` (Arch Linux) or `netselect-apt` (Debian/Ubuntu) for mirror management.
- Core package manager tools (`dpkg`, `apt`, or `pacman`) depending on your distro.
- `sudo` permissions for kernel or mirror-related operations.

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

### **Show Package Info**
```bash
python3 pactool.py --info vlc
```

### **Check for Outdated Packages**
```bash
python3 pactool.py --outdated
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

## **Kernel Management**
Pactool simplifies kernel management on Arch and Debian systems.

### **Cleanup Old Kernels**
```bash
python3 pactool.py --cleanup-kernels
```
This removes outdated kernels while keeping the current version intact.

### **Backup Current Kernel**
```bash
python3 pactool.py --backup-kernel
```
Backs up `vmlinuz`, `initramfs`, and optionally `System.map` to:
```
/boot/pactool/backup/
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
Cleans package cache and prompts before deleting.

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
--cleanup-kernels   Remove old kernels safely
--backup-kernel     Backup the current kernel
```

---

## **Tips and Tricks**
- Use `--user` to list only user-installed packages.
- Combine `--list` with `--sort` for quick overviews of package size and type.
- Backup mirrors before performing major upgrades.
- Use `--why` to track down unnecessary package dependencies.
- Create a shell alias:
```bash
alias pt='python3 /path/to/pactool.py'
```

---

## **Troubleshooting**
**Q:** Pactool says `reflector` is missing.  
**A:** Install it with:
```bash
sudo pacman -S reflector
```
For Debian-based systems, use:
```bash
sudo apt install netselect-apt
```

**Q:** Permission errors on mirror updates?  
**A:** Run with `sudo` or `sudo -E`.

**Q:** Kernel backup fails with missing `vmlinuz`?  
**A:** Ensure the kernel image path matches `/boot/vmlinuz-*`. Adjust `kernals.py` if needed.

---

## **Contributing**
We welcome contributions from developers, testers, and Linux enthusiasts. Steps:
1. Fork this repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a Pull Request.

**Ideas for contributions:**
- Add support for other package managers (e.g., zypper, dnf).
- Improve mirror ranking algorithms.
- Write tests for advanced features.

---

## **License**
MIT License - see LICENSE file.
