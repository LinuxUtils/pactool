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


from shutil import which


# ==> PACTOOL FILES
from core.logger import logError




##########################################################################
#                                                                        #
#                               MANAGER                                  #
#                                                                        #
##########################################################################


class Manager:
    def __init__(self):
        # ==> DETECT PACKAGE MANAGER ON INIT
        self.defaultPackageManager = self.detectManager()
    
    
    
    # ==> DETECT SYSTEM PACKAGE MANAGER
    def detectManager(self) -> str:
        if which("apt"):
            return "apt"
        elif which("pacman"):
            return "pacman"
        
        
        logError("No supported package manager found (apt/pacman).")
        return ""