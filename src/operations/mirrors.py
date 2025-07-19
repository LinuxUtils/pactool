# ==============================================================================
#
#  Pactool - A Cross-Distro Package Management Helper
#  Copyright 2025 The Linux Utils (https://github.com/LinuxUtils/pactool)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  This software is provided for free and open use, but attribution is
#  REQUIRED when redistributing or modifying this code. Any derivative
#  works must include this license header and must clearly indicate all
#  modifications that have been made.
#
#  For third-party code integrations, ensure you comply with both the
#  Pactool license and the license of the third-party code.
#
#  DISCLAIMER:
#  Pactool is provided "as is," without any warranties of any kind,
#  whether express or implied, including but not limited to warranties
#  of merchantability or fitness for a particular purpose.
#
# ==============================================================================


##########################################################################
#                                MODULES                                 #
##########################################################################

from os import makedirs, listdir
from os.path import expanduser, join, isdir, getctime
from datetime import datetime
from subprocess import run, PIPE
from shutil import copy, which
from sys import stdout
from time import sleep, perf_counter
from urllib.request import urlopen
from threading import Event


# ==> PACTOOL FILES
from core.logger import logError
from core.formatter import Formatter
from core.thread import SafeThread


##########################################################################
#                                MIRRORS                                 #
##########################################################################

class Mirrors:
    def __init__(self, Pactool):
        # ==> USE THE DEFAULT PACKAGE MANAGER FROM PACTOOL
        self.pactool = Pactool
        self.mirrorsUp = 0
        self.mirrorsDown = 0






    ######################################################################
    #                            SHOW MIRRORS                            #
    ######################################################################
    def showMirrors(self) -> None:
        try:
            mirrors = []
            
            
            if self.pactool.manager.defaultPackageManager == "apt":
                print(Formatter.colorText("  -> Current APT Mirrors", Formatter.headerColor, Formatter.bold))
                with open("/etc/apt/sources.list", "r") as f:
                    mirrors = [line.split()[1] for line in f if line.strip().startswith("deb")]
            elif self.pactool.manager.defaultPackageManager == "pacman":
                print(Formatter.colorText("  -> Current Pacman Mirrors", Formatter.headerColor, Formatter.bold))
                with open("/etc/pacman.d/mirrorlist", "r") as f:
                    mirrors = [line.split("=")[1].strip() for line in f if line.strip().startswith("Server")]
            else:
                print(Formatter.colorText("No supported package manager found.", Formatter.red))
                return


            if not mirrors:
                print(Formatter.colorText("No mirrors found.", Formatter.red))
                return


            maxWidth = max(len(url) for url in mirrors) + 1
            self.mirrorsUp = 0
            self.mirrorsDown = 0


            for url in mirrors:
                self._printMirrorStats(url, maxWidth)


            # ==> SUMMARY
            if self.mirrorsUp == len(mirrors):
                print(Formatter.colorText("\nAll mirrors tested are up.", Formatter.green, Formatter.bold))
            elif self.mirrorsDown == len(mirrors):
                print(Formatter.colorText("\nAll mirrors tested are down.", Formatter.red, Formatter.bold))
            else:
                print(Formatter.colorText(
                    f"\nThere are {self.mirrorsUp} mirror(s) up and {self.mirrorsDown} mirror(s) down.",
                    Formatter.yellow, Formatter.bold
                ))


        except Exception as error:
            logError(f"Failed to show mirrors ({error})")








    def _printMirrorStats(self, url: str, maxWidth: int):
        loadingSymbols = ["-", "\\", "|", "/"]
        stopEvent = Event()



        # ==> ANIMATION (WHILE TESTING CONNECTION)
        def animate():
            i = 0
            while not stopEvent.is_set():
                stdout.write(f"\r{Formatter.tab4} [{loadingSymbols[i % 4]}] Testing {url.ljust(maxWidth)}")
                stdout.flush()
                sleep(0.1)
                i += 1



        animationThread = SafeThread(target=animate)
        animationThread.start()



        # ==> TEST MIRROR SPEED
        try:
            start = perf_counter()
            testUrl = url.replace("$repo", "core").replace("$arch", "x86_64")
            conn = urlopen(testUrl, timeout=5)
            elapsed = (perf_counter() - start) * 1000
            lastModified = conn.headers.get("Last-Modified", "N/A")
            stopEvent.set()
            animationThread.join()


            # ==> FORMAT TIME TO HAVE FIXED WIDTH
            timeStr = f"{elapsed:.2f} ms".rjust(16)


            stdout.write(
                f"\r{Formatter.colorText('[✔]', Formatter.green, Formatter.bold)}  "
                f"{url.ljust(maxWidth)}  "
                f"{Formatter.colorText(timeStr, Formatter.green)}    "
                f"(Last Updated: {lastModified})\n"
            )
            self.mirrorsUp += 1




        except Exception:
            stopEvent.set()
            animationThread.join()
            unreachableStr = "Unreachable".rjust(16)
            stdout.write(
                f"\r{Formatter.colorText('[X]', Formatter.red, Formatter.bold)}  "
                f"{url.ljust(maxWidth)}  "
                f"{Formatter.colorText(unreachableStr, Formatter.red)}\n"
            )
            self.mirrorsDown += 1








    def updateFastestMirrors(self) -> None:
        try:
            # ==> CHECK IF REQUIRED TOOL IS INSTALLED
            if not self._checkMirrorTool():
                return


            # ==> BACKUP CURRENT MIRRORS
            backupFile = self._backupMirrors()
            if backupFile:
                print(Formatter.colorText(f"Backup created at {backupFile}", Formatter.green))
                print()


            # ==> DETERMINE PACKAGE MANAGER AND RUN UPDATE
            if self.pactool.manager.defaultPackageManager == "apt":
                print(Formatter.colorText("Updating APT mirrors to fastest ones [...]", Formatter.yellow, Formatter.bold))
                run(["netselect-apt", "-n", "stable"], stdout=PIPE, stderr=PIPE, text=True)
                print(Formatter.colorText("\nAPT mirrors updated. Check /etc/apt/sources.list for changes.", Formatter.green))


            elif self.pactool.manager.defaultPackageManager == "pacman":
                print(Formatter.colorText("Updating Pacman mirrors to fastest ones [...]", Formatter.yellow, Formatter.bold))
                run([
                    "reflector",
                    "--latest", "10",
                    "--sort", "rate",
                    "--save", "/etc/pacman.d/mirrorlist"
                ], stdout=PIPE, stderr=PIPE, text=True)
                print(Formatter.colorText("\nPacman mirrors updated successfully.", Formatter.green))

            else:
                print(Formatter.colorText("\nNo supported package manager found.", Formatter.red))


        except Exception as error:
            logError(f"\nFailed to update mirrors ({error})")








    def _backupMirrors(self):
        try:
            # ==> CREATE CACHE DIRECTORY IF NEEDED
            backupDir = expanduser("~/.cache/pactool/mirrors")
            makedirs(backupDir, exist_ok=True)


            # ==> BACKUP FILE NAME (TIMESTAMPED)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backupFile = join(backupDir, f"{timestamp}.list")


            # ==> COPY MIRROR LIST BASED ON PACKAGE MANAGER
            if self.pactool.manager.defaultPackageManager == "apt":
                copy("/etc/apt/sources.list", backupFile)
            elif self.pactool.manager.defaultPackageManager == "pacman":
                copy("/etc/pacman.d/mirrorlist", backupFile)
            else:
                return None


            return backupFile
        
        
        except Exception as error:
            logError(f"Failed to backup mirrors ({error})")
            return None







    def revertMirrors(self) -> None:
        try:
            backupDir = expanduser("~/.cache/pactool/mirrors")


            # ==> CHECK IF BACKUP DIRECTORY EXISTS
            if not isdir(backupDir):
                print(Formatter.colorText("No mirror backups found.", Formatter.red))
                return


            # ==> LIST AVAILABLE BACKUPS
            backups = sorted(listdir(backupDir))
            if not backups:
                print(Formatter.colorText("No mirror backups available.", Formatter.red))
                return



            print(Formatter.colorText("Available backups\n", Formatter.headerColor, Formatter.bold))
            for i, backup in enumerate(backups, start=1):
                formattedName = self._formatBackupName(backupDir, backup)
                print(f"{Formatter.magenta}({i}){Formatter.white} {formattedName}")



            # ==> ASK USER TO CHOOSE A BACKUP
            try:
                choice = int(input(f"\n{Formatter.bold}{Formatter.white}Which backup would you like? (ID) > {Formatter.magenta}").strip())
                print()
                if choice < 1 or choice > len(backups):
                    print(Formatter.colorText("Invalid choice.", Formatter.red))
                    return

            except ValueError:
                print(Formatter.colorText("Invalid input.", Formatter.red))
                return


            # ==> APPLY SELECTED BACKUP
            selectedBackup = join(backupDir, backups[choice - 1])
            if self.pactool.manager.defaultPackageManager == "apt":
                copy(selectedBackup, "/etc/apt/sources.list")
            elif self.pactool.manager.defaultPackageManager == "pacman":
                copy(selectedBackup, "/etc/pacman.d/mirrorlist")
            else:
                print(Formatter.colorText("No supported package manager found.", Formatter.red))
                return


            print(Formatter.colorText(f"Reverted mirrors to {backups[choice - 1]}", Formatter.green))
            print()
            
            
            # ==> ASK USER IF THEY WANT TO TEST MIRRORS
            testChoice = input(
                f"{Formatter.bold}{Formatter.white}Would you like to test the mirrors now? [y/N] > {Formatter.cyan}"
            ).strip().lower()
            print()
            
            
            if testChoice == "y":
                self.showMirrors()


        except Exception as error:
            errorName = type(error).__name__.lower()
            
            if errorName == "permissionerror":
                logError("Pactool doesn't have sudo privileges! Try running with 'sudo -E'")
            else:
                logError(f"Failed to revert mirrors ({error})")









    def _formatBackupName(self, backupDir: str, backup: str) -> str:
        try:
            # ==> REMOVE EXTENSION AND PARSE TIMESTAMP
            name = backup.rsplit('.', 1)[0]
            formatted = datetime.strptime(name, "%Y-%m-%d_%H-%M-%S")


            # ==> FORMAT DATE AND TIME
            datePart = formatted.strftime("%A, %d %B %Y")
            timePart = formatted.strftime("%I:%M:%S %p")


            return f"{Formatter.bold}{datePart}{Formatter.reset} at {Formatter.colorText(timePart, Formatter.headerColor, Formatter.bold)}"


        except Exception:
            # ==> TRY FILE CREATION DATE
            try:
                ctime = getctime(join(backupDir, backup))
                formatted = datetime.fromtimestamp(ctime)


                datePart = formatted.strftime("%A, %d %B %Y")
                timePart = formatted.strftime("%I:%M:%S %p")


                return f"{Formatter.bold}{datePart}{Formatter.reset} at {Formatter.colorText(timePart, Formatter.headerColor, Formatter.bold)}"


            except Exception:
                return Formatter.colorText("(Unrecognised Backup)", Formatter.red, Formatter.bold)


    
    
    
    
    
    
    
    
    
    
    
    ######################################################################
    #                        HELPER FUNCTIONS                            #
    ######################################################################
    def _checkMirrorTool(self) -> bool:
        toolName = "reflector" if self.pactool.manager.defaultPackageManager == "pacman" else "netselect-apt"
        if which(toolName):
            return True


        # ==> ASK USER TO INSTALL TOOL
        print(Formatter.colorText(f"'{toolName}' is not installed. Pactool needs it.", Formatter.red))
        
        
        choice = input(f"\n{Formatter.yellow}Do you want Pactool to install '{toolName}'? [y/N] > {Formatter.white}{Formatter.bold}").strip().lower()
        print()
        
        
        if choice == "y":
            try:
                self.pactool.packages.install(name=toolName)
                return True
            except Exception as error:
                logError(f"Failed to install '{toolName}' ({error})")
                return False
            
            
        return False
    
    
    
    
    
    
    
    
    def createManualBackup(self) -> None:
        try:
            backupFile = self._backupMirrors()
            
            
            if backupFile:
                print(Formatter.colorText(f"Manual backup created -> {backupFile}", Formatter.green))
            else:
                print(Formatter.colorText("Failed to create backup. No supported package manager found.", Formatter.red))
        
        
        except Exception as error:
            logError(f"Failed to create manual backup of mirrors ({error})")
