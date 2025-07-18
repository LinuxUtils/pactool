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
#                                                                        #
#                                MODULES                                 #
#                                                                        #
##########################################################################

from subprocess import run
from os.path import exists as pathExists


# ==> PACTOOL FILES
from core.logger import logError
from core.formatter import Formatter




##########################################################################
#                                                                        #
#                               Kernels                                  #
#                                                                        #
##########################################################################

class Kernels:
    def __init__(self, Pactool=None) -> None:
        self.pactool = Pactool
        
        
        
        
    # ==> CLEANUP OLD KERNELS
    def cleanupKernels(self, testMode: bool = False) -> None:
        try:
            # ==> PRINT HEADER
            print(Formatter.colorText("\nCleaning up old kernels [...]\n", Formatter.headerColor, Formatter.bold))


            # ==> GET CURRENTLY RUNNING KERNEL
            currentKernel = run(["uname", "-r"], capture_output=True, text=True, check=False).stdout.strip()
            currentKernelPkg = f"linux{currentKernel.split('-')[0]}"


            if self.pactool.manager.defaultPackageManager == "pacman":
                if testMode:
                    # ==> FAKE DATA FOR TESTING
                    kernels = ["linux", "linux-lts", "linux-zen", "linux-hardened"]
                else:
                    # ==> GET INSTALLED KERNEL PACKAGES
                    result = run(["pacman", "-Qq", "linux"], capture_output=True, text=True, check=False)
                    kernels = [k for k in result.stdout.splitlines() if k.startswith("linux")]



                # ==> REMOVE CURRENTLY RUNNING KERNEL FROM DELETION LIST
                oldKernels = [k for k in kernels if currentKernelPkg not in k]



                if not oldKernels:
                    print(Formatter.colorText("No old kernels found.", Formatter.green))
                    return



                # ==> DISPLAY OLD KERNELS TO BE REMOVED
                print(Formatter.colorText("Removing old kernels:\n", Formatter.yellow))
                for k in oldKernels:
                    print(f"  {Formatter.colorText(k, Formatter.red)}")
                    if not testMode:
                        run(["sudo", "pacman", "-Rns", k], check=False)



            elif self.pactool.manager.defaultPackageManager == "apt":
                if testMode:
                    print(Formatter.colorText("APT old kernels found: linux-image-5.15, linux-image-6.1", Formatter.yellow))
                    print(Formatter.colorText("Simulating removal of old kernels [...]", Formatter.yellow))
                else:
                    # ==> USE APT AUTOREMOVE BUT KEEP CURRENT KERNEL
                    print(Formatter.colorText("Removing old kernels using apt autoremove [...]", Formatter.yellow))
                    run(["sudo", "apt-get", "autoremove", "--purge", "-y"], check=False)



            print(Formatter.colorText("Kernel cleanup complete.", Formatter.green))


        except Exception as error:
            logError(f"Failed to clean up kernels ({error})")
            
            
            
            
            
        # ==> BACKUP CURRENT KERNEL
    def backupKernel(self, testMode: bool = False) -> None:
        try:
            # ==> PRINT HEADER
            print(Formatter.colorText("\nBacking up current kernel [...]\n", Formatter.headerColor, Formatter.bold))


            # ==> GET CURRENT KERNEL VERSION
            currentKernel = run(["uname", "-r"], capture_output=True, text=True, check=False).stdout.strip()


            # ==> DETERMINE KERNEL IMAGE
            if "zen" in currentKernel:
                kernelImage = "/boot/vmlinuz-linux-zen"
            elif "lts" in currentKernel:
                kernelImage = "/boot/vmlinuz-linux-lts"
            elif "hardened" in currentKernel:
                kernelImage = "/boot/vmlinuz-linux-hardened"
            else:
                kernelImage = "/boot/vmlinuz-linux"


            # ==> VERIFY KERNEL IMAGE
            result = run(["ls", kernelImage], capture_output=True, text=True, check=False)
            if result.returncode != 0:
                print(Formatter.colorText("Error -> No kernel image found in /boot.", Formatter.red))
                return


            # ==> DEFINE DESTINATION
            backupDir = "/boot/pactool/backup/"
            backupFile = f"{backupDir}{kernelImage.split('/')[-1]}-{currentKernel}"


            # ==> CREATE BACKUP DIRECTORY
            if not testMode:
                run(["sudo", "mkdir", "-p", backupDir], check=False)


            # ==> COPY KERNEL IMAGE
            if testMode:
                print(Formatter.colorText(f"Simulating -> sudo cp {kernelImage} {backupFile}", Formatter.yellow))
            else:
                # ==> ASK USER TO OVERWRITE IF A BACKUP ALREADY EXISTS
                if pathExists(backupFile):
                    print(Formatter.colorText(f"[WARNING] A backup of this kernal already exists!", Formatter.red))
                    choice = input(f"\n{Formatter.yellow}Do you want to overwrite it? [y/N] > {Formatter.white}{Formatter.bold}").strip().lower()
                    print()
                    
                    
                    if choice != "y":
                        print("Backup aborted.")
                        return None
                    
                    
                run(["sudo", "cp", kernelImage, backupFile], check=False)


            print(
                Formatter.colorText(f"Kernel {currentKernel}", Formatter.green)
                + " backed up to "
                + Formatter.colorText(f"{backupFile}", Formatter.green)
            )


        except Exception as error:
            logError(f"Failed to backup kernel ({error})")
