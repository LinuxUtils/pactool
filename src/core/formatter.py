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
from re import sub as reSub



##########################################################################
#                                                                        #
#                           FORMATTER CLASS                              #
#                                                                        #
##########################################################################
class Formatter:
    # ==> SPACING
    tab4 = " " * 4
    tab8 = " " * 8
    point = "•"


    # ==> ANSI COLOR CODES
    reset = "\033[0m"
    bold = "\033[1m"
    dim = "\033[2m"
    italic = "\033[3m"
    underline = "\033[4m"


    # ==> COLORS
    black = "\033[30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    magenta = "\033[35m"
    cyan = "\033[36m"
    white = "\033[37m"


    # ==> BRIGHT COLORS
    brightBlack = "\033[90m"
    brightRed = "\033[91m"
    brightGreen = "\033[92m"
    brightYellow = "\033[93m"
    brightBlue = "\033[94m"
    brightMagenta = "\033[95m"
    brightCyan = "\033[96m"
    brightWhite = "\033[97m"
    
    
    # ==> CUSTOM COLOR ASSIGNMENTS
    packageColor = f"{bold}{blue}"
    userPackageColor = f"{bold}{magenta}"
    systemPackageColor = f"{bold}{blue}"
    sizeColor = f"{bold}{green}"
    dateColor = f"{bold}{yellow}"
    headerColor = f"{bold}{brightYellow}"






    @classmethod
    def formatSize(cls, bytesSize: int) -> str:
        units = ["B", "KiB", "MiB", "GiB"]
        size = float(bytesSize)
        unitIndex = 0
        
        
        while size >= 1024 and unitIndex < len(units) - 1:
            size /= 1024
            unitIndex += 1
            
            
        return f"{size:.2f} {units[unitIndex]}"






    @classmethod
    def colorText(cls, text: str, color: str = "", style: str = "") -> str:
        """
        Returns text with given ANSI color and style.
        Example:
            Formatter.colorText("Hello", Formatter.red, Formatter.bold)
        """
        return f"{style}{color}{text}{cls.reset}"
    
    
    
    
    
    
    @classmethod
    def displayPackageLegend(cls) -> None:
        # ==> DEFINE COLORED SQUARES
        userSquare = Formatter.colorText("■", Formatter.userPackageColor, Formatter.bold)
        systemSquare = Formatter.colorText("■", Formatter.systemPackageColor, Formatter.bold)


        # ==> DISPLAY LEGEND
        print(f"{userSquare} User package")
        print(f"{systemSquare} System package")





    
    @classmethod
    def formatHistoryTime(cls, timestamp: str) -> str:
        """
        Parse timestamps from pacman and apt logs into a human-readable format.
        Supports multiple common formats.
        """
        timeFormats = [
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S",
            "%a %d %b %Y %H:%M:%S %z",
            "%Y-%m-%d %H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S",
            "%d-%m-%Y %H:%M:%S",
            "%m/%d/%Y %H:%M:%S"
        ]
        
        for fmt in timeFormats:
            try:
                dt = datetime.strptime(timestamp, fmt)
                return dt.strftime("%d %b %Y, %I:%M %p %Z")
            except ValueError:
                continue
            
            
        return timestamp