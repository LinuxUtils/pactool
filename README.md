![PACTOOL BANNER](https://github.com/LinuxUtils/paktool/blob/main/graphics/PACTOOL_BANNER.png?raw=true)

[![License: Apache 2](https://img.shields.io/badge/License-APACHE2-blue.svg)](https://github.com/LinuxUtils/pactool/blob/main/LICENSE)
[![Latest Commit](https://img.shields.io/github/last-commit/LinuxUtils/pactool?color=blue&label=Last%20Commit)](https://github.com/LinuxUtils/pactool/commits/main)
[![Release](https://img.shields.io/github/v/release/LinuxUtils/pactool?color=green&label=Latest%20Release)](https://github.com/LinuxUtils/pactool/releases)
[![Issues](https://img.shields.io/github/issues/LinuxUtils/pactool?color=red&label=Open%20Issues)](https://github.com/LinuxUtils/pactool/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/LinuxUtils/pactool?label=Pull%20Requests)](https://github.com/LinuxUtils/pactool/pulls)
[![Repo Size](https://img.shields.io/github/repo-size/LinuxUtils/pactool?label=Repo%20Size)](https://github.com/LinuxUtils/pactool)
[![Code Size](https://img.shields.io/github/languages/code-size/LinuxUtils/pactool?label=Code%20Size)](https://github.com/LinuxUtils/pactool)
[![Top Language](https://img.shields.io/github/languages/top/LinuxUtils/pactool?color=yellow)](https://github.com/LinuxUtils/pactool)
[![Contributors](https://img.shields.io/github/contributors/LinuxUtils/pactool)](https://github.com/LinuxUtils/pactool/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/LinuxUtils/pactool?style=social)](https://github.com/LinuxUtils/pactool/network/members)
[![Stars](https://img.shields.io/github/stars/LinuxUtils/pactool?style=social)](https://github.com/LinuxUtils/pactool/stargazers)
[![Watchers](https://img.shields.io/github/watchers/LinuxUtils/pactool?style=social)](https://github.com/LinuxUtils/pactool/watchers)
[![Downloads](https://img.shields.io/github/downloads/LinuxUtils/pactool/total?color=purple&label=Downloads)](https://github.com/LinuxUtils/pactool/releases)
[![Python Version](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![OS](https://img.shields.io/badge/Supported-Arch%20%7C%20Debian%20%7C%20Ubuntu-orange)](https://github.com/LinuxUtils/pactool)
[![PyPI Version](https://img.shields.io/pypi/v/pactool-linuxutils?color=blue&label=PyPI%20Version)](https://pypi.org/project/pactool-linuxutils/)


# What is Pactool?
#### Pactool is a versatile, simple, and powerful package management helper designed for **Arch Linux** and **Debian-based distributions**. It provides a clear and modern overview of all installed packages, their sizes, and dependencies, and offers various tools to optimize and maintain your system efficiently.

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



## **Security Management**

Pactool offers built-in tools to manage and check for security vulnerabilities.

### **View Security Packages**
Check for installed security-related packages on Debian/Ubuntu or run a security audit on Arch Linux:
```bash
python3 pactool.py --view-security-packages
```
**Debian/Ubuntu Example Output:**
```
Security Packages Installed (Debian/Ubuntu):
libssl1.1
libgnutls30
```
**Arch Linux Example Output:**
```
grub        [High Risk]    Affected by multiple issues.
libxml2     [High Risk]    Affected by denial of service.
```
Packages are **color-coded**:
- **Blue**: System packages.
- **Magenta**: User-installed packages.

### **Upgrade Security Packages**
On Debian/Ubuntu systems, upgrade only security-related packages:
```bash
python3 pactool.py --upgrade-security
```
This ensures only security-related updates are applied.

### **Check Security Vulnerabilities**
You can run a vulnerability check for any package using:
```bash
python3 pactool.py --vuln-check PACKAGE
```
Example:
```
python3 pactool.py --vuln-check openssl
```
This will list all known CVEs, paginate results, and allow keyword searching within CVEs.
\
\
You can also perform a deep search on a package
```
python3 pactool.py --vuln-check feh --deep-search
```


## Deep‑Dive Commands: `--history` & `--versions`
These two commands for very useful for tracking package vulnerabilities on your Linux system.  
They are optional, safe‑to‑run, **read‑only** operations – nothing is modified on disk.

---

### `--history PACKAGE` — Time‑Travel Through Install & Upgrade Events
| What it does | Why it matters |
|--------------|----------------|
| **Parses native logs** (`/var/log/pacman.log` on Arch/Manjaro, `apt` history on Debian/Ubuntu). | No additional services or daemons required.  |
| **Groups each event** → _Installed / Upgraded_  | Instantly see when & why a package changed. |
| **Extracts the exact command** that triggered the change. | Answers *“Which script or user action installed this?”* |
| **Builds a tree** of version transitions  (`3.10.3‑1 → 3.11.0‑2`). | Visual diff of how you arrived at the current release. |
| **Colour‑codes** user vs system packages. | Glance‑level ownership info. |
| **Respects `Ctrl +C`** — quits instantly, no messy tracebacks. | Friendly CLI UX. |

#### Example
```bash
pactool --history bash
```
```
Package Version History for 'bash':

    Installed bash (5.2.037‑1)              on 15 Feb 2025, 06:43 AM UTC
     Upgraded bash (5.2.037‑1 → 5.2.037‑2)  on 14 Mar 2025, 10:49 AM UTC+03:00
     Upgraded bash (5.2.037‑2 → 5.2.037‑3)  on 07 May 2025, 09:53 AM UTC+03:00
     Upgraded bash (5.2.037‑3 → 5.2.037‑5)  on 10 May 2025, 02:33 AM UTC+03:00
     Upgraded bash (5.2.037‑5 → 5.3.0‑1)    on 14 Jul 2025, 12:47 AM UTC+03:00

    Command used:
        pacman -Syu bash

    Version Tree:
        ├─ 5.2.037‑1
        ├─ 5.2.037‑1 → 5.2.037‑2
        ├─ 5.2.037‑2 → 5.2.037‑3
        ├─ 5.2.037‑3 → 5.2.037‑5
        └─ 5.2.037‑5 → 5.3.0‑1 (current)
```
**Tips**
* Pipe to `less -R` to keep colours while scrolling.
* Combine with `grep` to find a specific date:  
  `pactool --history openssl | grep 2025‑04`

---

### `--versions PACKAGE` — Repo‑Wide Version Explorer
<details>
<summary><strong>Quick glance</strong></summary>

| Mode | Purpose |
|------|---------|
| **Plain** (`--versions pkg`) | Fast list – shows every build string available in enabled repositories. |
| **Risk mode** (`--versions pkg --assess-risk`) | Queries the **NVD API** live, counts CVEs per version, colour‑codes severity, shows a spinner while fetching. |

</details>

#### Why you’ll love it
* **Upgrade forecasting** – see what you’ll get _before_ hitting `pacman -Syu`.
* **Rollback clarity** – pick an earlier safe build if the latest has many CVEs.
* **Security snapshot** – Low/Medium/High risk label + exact CVE count.

#### Example – quick scan
```bash
pactool --versions python
```
```
    ├─ 3.12.6‑2
    ├─ 3.12.6‑3
    └─ 3.13.0‑1  (current)
```

#### Example – full risk audit
```bash
pactool --versions python --assess-risk
```
```
Assessing risk for 'python' [\]
Available Versions for 'python':

    ├─ 3.12.6‑2  [LOW RISK]     0 CVEs
    ├─ 3.12.6‑3  [MEDIUM RISK]  4 CVEs
    └─ 3.13.0‑1  [HIGH RISK]    7 CVEs  (current)
```

**How the risk score works**

| CVE Count | Label | Typical action |
|-----------|----------------|----------------|
| 0 | **LOW RISK** | Safe to use / keep. |
| 1 – 5 | **MEDIUM RISK** | Read CVE details; upgrade soon. |
| > 5 | **HIGH RISK** | Patch or pin a safer version ASAP (or get exploited, idc either way). |

> NVD API is rate‑limited (5 req / 30 s). Pactool caches results per session to avoid throttling.


---

### Some really useful combinations
| Goal | Command |
|------|---------|
| Audit all install events **and** fetch CVEs for each version | `pactool --history openssl && pactool --versions openssl --assess-risk` |
| Show only available versions newer than installed | `pactool --versions vim \| awk '$1 > "9.0.0"'` |
| Continuous monitoring (cron) | `pactool --versions kernel --assess-risk >> /var/log/kernel-risk.log` |

---

## **Command Overview**
```
GENERAL COMMANDS:
  --version                   Show Pactool version and exit
  --about                     Display detailed information about Pactool

PACKAGE COMMANDS:
  --list                      List installed packages (paged by default)
  -n N                        Number of packages to show (0 = all)
  --stats                     Show statistics about packages
  --files PACKAGE             List all files installed by a package
  --search SEARCH             Search for a package by name
  --why PACKAGE               Show reverse dependencies of a package
  --uninstall PACKAGE         Uninstall a package by name
  --install PACKAGE           Install a package by name
  --update                    Update all installed packages
  --upgrade                   Upgrade all installed packages
  --clean                     Clean cached or unused package files
  --sort CRITERIA             name/size/install-date/update-date/type
  --rsort CRITERIA            Reverse sort by the same criteria
  --user                      Show only user-installed packages
  --system                    Show only system packages
  --info PACKAGE              Show detailed information about a package
  --bloat                     Find unused optional dependencies (bloat)
  --unused                    Find unused or orphaned packages
  --outdated                  List all outdated packages
  --history PACKAGE           Show version history and updates of a package
  --versions PACKAGE          Show all available versions of a package with risk levels

SERVICE COMMANDS:
  --services                  Show status of services related to packages
  --service-info SERVICE      Show detailed info about a service
  --service-logs SERVICE      Show logs of a service

MIRROR COMMANDS:
  --show-mirrors              Show current mirrors with ping & last update
  --update-mirrors            Update to fastest mirrors
  --revert-mirrors            Revert mirrors to previous backup
  --backup-mirrors            Create a manual backup of the current mirror list

KERNEL COMMANDS:
  --cleanup-kernels           Automatically remove old kernels
  --backup-kernel             Backup the current running kernel to /boot/pactool/backup

SECURITY COMMANDS:
  --upgrade-security          Upgrade only security-related packages (Debian/Ubuntu)
  --vuln-check PACKAGE        Check known CVEs (vulnerabilities) for a package
  --deep-search               Use with --vuln-check for detailed exploit tree and history
  --view-security-packages    View all installed security packages with details
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
Copyright 2025 LinuxUtils

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

[View License](LICENSE)
