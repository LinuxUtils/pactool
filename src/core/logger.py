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

from datetime import datetime
from pathlib import Path
from logging import basicConfig, info, error, INFO


# ==> PACTOOL FILES
from core.formatter import Formatter


# ==> CREATE LOG DIRECTORY
logDir = Path.home() / ".cache" / "pactool" / "logs"
logDir.mkdir(parents=True, exist_ok=True)



# ==> LOG FILE NAME BASED ON TODAY'S DATE
logFile = logDir / f"{datetime.now().strftime('%Y-%m-%d')}.log"





# ==> CONFIGURE LOGGER
basicConfig(
    filename=logFile,
    level=INFO,
    format="[PACTOOL LOG] [%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%I:%M:%S %p"
)






def logSuccess(message: str):
    """
    Logs a success message to today's Pactool log file.
    """
    cleanString = message.replace("\n", "").replace("\r", "")
    print(Formatter.colorText(message, Formatter.green, Formatter.bold))
    info(cleanString)





def logError(message: str):
    """
    Logs an error message to today's Pactool log file.
    """
    cleanString = message.replace("\n", "").replace("\r", "")
    print(Formatter.colorText(message, Formatter.red, Formatter.bold))
    error(cleanString)
