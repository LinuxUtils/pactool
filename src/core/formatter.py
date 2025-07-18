# MIT License
#
# Copyright (c) 2025 CLEN - By www.github.com/g7gg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.




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
    headerColor = f"{bold}{cyan}"






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
