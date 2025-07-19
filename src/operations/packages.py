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

from shutil import get_terminal_size
from subprocess import run, CalledProcessError, DEVNULL, PIPE
from datetime import datetime
from os import stat
from re import search
from urllib.request import urlopen, Request
from urllib.parse import quote
from json import loads as jsonLoads
from time import sleep as timeSleep
from sys import stdout as sysStdout


# ==> PACTOOL FILES
from core.logger import logError
from core.formatter import Formatter
from core.thread import SafeThread




##########################################################################
#                                                                        #
#                               PACKAGES                                 #
#                                                                        #
##########################################################################

class Packages:
    def __init__(self, Pactool=None) -> None:
        self.pactool = Pactool





    def _paginate(self, items, renderFunc, limit: int = None):
        # ==> APPLY LIMIT IF PROVIDED
        if limit is not None:
            if limit > 0:
                items = items[:limit]
            elif limit == 0:
                Formatter.displayPackageLegend()
                print()
                renderFunc(items, startIndex=0)
                return


        # ==> DETERMINE TERMINAL HEIGHT
        terminalHeight = get_terminal_size().lines - 10
        index = 0


        while index < len(items):
            # ==> RENDER CURRENT CHUNK
            endIndex = index
            lineCount = 0
            
            
            while endIndex < len(items):
                # ==> ESTIMATE LINES FOR CURRENT ITEM (NAME + DESCRIPTION)
                pkg = items[endIndex]
                pkgLines = 1
                
                
                # ==> NAME & DESCRIPTION
                if isinstance(pkg, tuple) and pkg[1]:
                    pkgLines += 2
                if lineCount + pkgLines > terminalHeight:
                    break
                
                
                lineCount += pkgLines
                endIndex += 1



            Formatter.displayPackageLegend()
            print()
            renderFunc(items[index:endIndex], startIndex=index)
            index = endIndex



            if index < len(items):
                print(f"{Formatter.headerColor}\nPress enter to continue | 'Q' to quit\n")
                userInput = input(
                    Formatter.colorText(
                        "--> ",
                        Formatter.headerColor
                    )
                ).strip()
                if userInput == "q":
                    break
                print()
                
                
                
                
                
                
    
    
    
    def _paginateSearch(self, packages, keyword, renderFunc, limit: int = None):
        # ==> APPLY LIMIT IF PROVIDED
        if limit is not None:
            if limit > 0:
                packages = packages[:limit]
                
                
            elif limit == 0:
                # ==> SHOW HEADER AND DISPLAY ALL RESULTS WITHOUT PAGINATION
                print(f'{Formatter.headerColor}Showing results for "{keyword}"{Formatter.reset}\n')
                Formatter.displayPackageLegend()
                print()
                renderFunc(packages, keyword, startIndex=0)
                
                
                # ==> ASK USER FOR A NEW KEYWORD EVEN IF RESULTS FIT ON ONE PAGE
                print(f"{Formatter.headerColor}\nPress enter to continue | 'Q' to quit | or type a new keyword\n")
                userInput = input(
                    Formatter.colorText(
                        "--> ",
                        Formatter.headerColor
                    )
                ).strip().lower()
                
                
                return userInput if userInput and userInput != "q" else None


        # ==> CALCULATE TERMINAL HEIGHT (NUMBER OF LINES THAT FIT)
        terminalHeight = get_terminal_size().lines - 10


        # ==> TOTAL PACKAGES AND PAGE CALCULATION
        totalPackages = len(packages)
        pageSize = 0
        index = 0
        pageNumber = 1


        # ==> CALCULATE TOTAL PAGES (APPROX) BY SIMULATING A SINGLE PAGE
        tempIndex = 0
        tempLines = 0
        
        
        while tempIndex < totalPackages:
            pkg = packages[tempIndex]
            pkgLines = 1
            if isinstance(pkg, tuple) and pkg[1]:
                pkgLines += 2
            if tempLines + pkgLines > terminalHeight:
                break
            
            
            tempLines += pkgLines
            tempIndex += 1
            
        
        pageSize = max(1, tempIndex)
        totalPages = (totalPackages + pageSize - 1) // pageSize



        # ==> PAGINATION LOOP
        while index < totalPackages:
            endIndex = index
            lineCount = 0


            # ==> DETERMINE HOW MANY PACKAGES FIT IN THIS PAGE
            while endIndex < totalPackages:
                pkg = packages[endIndex]
                pkgLines = 1
                
                
                if isinstance(pkg, tuple) and pkg[1]:
                    pkgLines += 2
                if lineCount + pkgLines > terminalHeight:
                    break
                
                
                lineCount += pkgLines
                endIndex += 1



            # ==> DISPLAY PAGE HEADER
            print(f'\n{Formatter.headerColor}Showing results for "{keyword}" - Page {pageNumber} of {totalPages}{Formatter.reset}\n')
            Formatter.displayPackageLegend()
            print()



            # ==> RENDER CURRENT PAGE
            renderFunc(packages[index:endIndex], keyword, startIndex=index)



            # ==> UPDATE INDEX AND PAGE NUMBER
            index = endIndex
            pageNumber += 1



            # ==> ASK USER FOR INPUT IF THERE ARE MORE PAGES
            if index < totalPackages:
                print(f"{Formatter.headerColor}\nPress enter to continue | 'Q' to quit | or type a new keyword\n")
                userInput = input(
                    Formatter.colorText(
                        "--> ",
                        Formatter.headerColor
                    )
                ).strip()



                # ==> HANDLE USER INPUT
                if userInput.lower() == "q":
                    return None
                elif userInput:
                    return userInput
                print()



        # ==> ASK USER FOR A NEW KEYWORD EVEN IF RESULTS FIT ON ONE PAGE
        print(f"{Formatter.headerColor}\nPress enter to continue | 'Q' to quit | or type a new keyword\n")
        userInput = input(
            Formatter.colorText(
                "--> ",
                Formatter.headerColor
            )
        ).strip().lower()
        
        
        return userInput if userInput and userInput != "q" else None








    def list(self, limit: int = None, sortBy: str = None, showUser: bool = False, showSystem: bool = False, reverseSort: bool = False) -> None:
        try:
            packageList = self.collectAptPackages() if self.pactool.manager.defaultPackageManager == "apt" else self.collectPacmanPackages()
            if not packageList:
                print(Formatter.colorText("No packages found.", Formatter.red, Formatter.bold))
                return


            # ==> GET ALL USER PACKAGES ONCE
            userPkgs = self._getUserPackages()


            # ==> TAG EACH PACKAGE AS USER OR SYSTEM
            for pkg in packageList:
                pkg["isUser"] = pkg["name"] in userPkgs


            # ==> FILTER IF USER OR SYSTEM FLAGS ARE SET
            packageList = self._filterPackages(packageList, showUser, showSystem)


            # ==> SORT
            packageList = self._sortPackages(packageList, sortBy, reverseSort)


            # ==> WIDTH CALCULATION
            nameWidth = max(len(pkg["name"]) for pkg in packageList)
            sizeValWidth = max(len(pkg["sizeValue"]) for pkg in packageList) + 2
            sizeUnitWidth = max(len(pkg["sizeUnit"]) for pkg in packageList)
            dateWidth = max(
                max(len(pkg["installed"]) for pkg in packageList),
                max(len(pkg["updated"]) for pkg in packageList)
            )


            def renderChunk(chunk, startIndex=0):
                self._printPackages(chunk, nameWidth, sizeValWidth, sizeUnitWidth, dateWidth, startIndex=startIndex)


            self._paginate(packageList, renderChunk, limit)



        except CalledProcessError as error:
            logError(f"Failed to list packages ({error})")


        
        
        
    
    
    
    
    def _sortPackages(self, pkgs, sortBy: str, reverseSort=False):
        reverse = not reverseSort
        key = None


        if sortBy == "name":
            key = lambda p: p["name"].lower()
        elif sortBy == "size":
            key = lambda p: float(p["sizeValue"])
        elif sortBy == "install-date":
            key = lambda p: p.get("installedTs", 0)
        elif sortBy == "update-date":
            key = lambda p: p.get("updatedTs", 0)
        elif sortBy == "type":
            key = lambda p: (0 if p.get("isUser", False) else 1, p["name"].lower())


        return sorted(pkgs, key=key, reverse=reverse) if key else pkgs









    def _filterPackages(self, packageList, showUser: bool, showSystem: bool):
        if not (showUser or showSystem):
            return packageList


        userPkgs = self._getUserPackages()
        if showUser:
            return [pkg for pkg in packageList if pkg["name"] in userPkgs]
        elif showSystem:
            return [pkg for pkg in packageList if pkg["name"] not in userPkgs]
        return packageList







    def _getUserPackages(self):
        if self.pactool.manager.defaultPackageManager == "pacman":
            result = run(["pacman", "-Qe"], capture_output=True, text=True)
            return {line.split()[0] for line in result.stdout.strip().splitlines() if line}
        
        
        elif self.pactool.manager.defaultPackageManager == "apt":
            result = run(["apt-mark", "showmanual"], capture_output=True, text=True)
            return {line.strip() for line in result.stdout.strip().splitlines() if line}
        
        
        return set()








    
    def _parseDate(self, dateStr: str) -> datetime:
        """
        Parse package date strings from both APT and pacman.
        Normalize bare-hour timezones (e.g. "+03") to "+0300" so %z will accept them.
        Falls back to datetime.min if parsing fails.
        """
        dateStr = dateStr.strip()


        m = search(r' ([+-]\d{2})$', dateStr)
        if m:
            tz = m.group(1)
            dateStr = dateStr[:-len(tz)] + tz + "00"


        formats = [
            "%a %d %b %Y %I:%M:%S %p %z",
            "%a %d %b %Y %H:%M:%S %z",
            "%a %d %b %Y %I:%M:%S %p",
            "%Y-%m-%d %H:%M:%S",
        ]


        for fmt in formats:
            try:
                return datetime.strptime(dateStr, fmt)
            except ValueError:
                continue


        logError(f"Failed to parse date ({dateStr})")
        return datetime.min












    def _printPackages(self, pkgList, nameWidth, sizeValWidth, sizeUnitWidth, dateWidth, startIndex=0):
        for i, pkg in enumerate(pkgList, start=startIndex + 1):
            nameText = f"{pkg['name']:<{nameWidth}}"
            sizeText = f"{pkg['sizeValue']:<{sizeValWidth}} {pkg['sizeUnit']:<{sizeUnitWidth}}"
            installedText = f"{pkg['installed']:<{dateWidth}}"
            updatedText = f"{pkg['updated']:<{dateWidth}}"


            # ==> DETERMINE COLOR BASED ON USER VS SYSTEM
            packageColor = Formatter.userPackageColor if pkg.get("isUser", False) else Formatter.systemPackageColor


            print(
                f"{Formatter.bold}{i:<4}{Formatter.reset} "
                f"{Formatter.colorText(nameText, packageColor)}  "
                f"{Formatter.colorText(sizeText, Formatter.sizeColor)}  "
                f"Installed {Formatter.colorText(installedText, Formatter.dateColor)}  "
                f"Updated {Formatter.colorText(updatedText, Formatter.dateColor)}"
            )











    def search(self, name: str, limit: int = None) -> None:
        try:
            while True:
                result = ""
                if self.pactool.manager.defaultPackageManager == "apt":
                    result = run(["apt", "search", name], capture_output=True, text=True, check=True).stdout
                elif self.pactool.manager.defaultPackageManager == "pacman":
                    result = run(["pacman", "-Ss", name], capture_output=True, text=True, check=True).stdout
                else:
                    print(Formatter.colorText("No package manager found.", Formatter.red))
                    return



                # ==> PARSE RESULTS INTO (NAME, DESCRIPTION) PAIRS
                lines = [line.rstrip() for line in result.splitlines() if line.strip()]
                packages = []
                i = 0
                
                
                while i < len(lines):
                    nameLine = lines[i]
                    descLine = ""
                    if i + 1 < len(lines) and lines[i + 1].startswith(" "):
                        descLine = lines[i + 1].strip()
                        i += 1
                    packages.append((nameLine, descLine))
                    i += 1



                # ==> APPLY LIMIT AFTER PAIRING
                if limit is not None and limit > 0:
                    packages = packages[:limit]
                elif limit == 0:
                    self._printSearchResults(packages, name, startIndex=0)
                    return


                # ==> APPLY PAGINATION
                newKeyword = self._paginateSearch(
                    packages,
                    name,
                    lambda chunk, keyword, startIndex=0: self._printSearchResults(chunk, keyword, startIndex),
                    None
                )

                if newKeyword:
                    name = newKeyword
                    continue
                else:
                    break


        except CalledProcessError as error:
            logError(f"Failed to search for package '{name}' ({error})")









    def _printSearchResults(self, packages, keyword, startIndex=0):
        # ==> DETERMINE TERMINAL WIDTH AND DESCRIPTION MAX WIDTH
        terminalWidth = get_terminal_size().columns - 10
        maxDescWidth = terminalWidth - 8


        # ==> START PACKAGE INDEXING FROM startIndex + 1
        index = startIndex + 1


        # ==> LOOP THROUGH EACH PACKAGE AND ITS DESCRIPTION
        for pkgName, pkgDesc in packages:
            # ==> HIGHLIGHT MATCHING KEYWORDS IN PACKAGE NAME
            highlightedName = self._highlightKeyword(pkgName, keyword)


            # ==> DETERMINE PACKAGE COLOR BASED ON USER OR SYSTEM TYPE
            pkgColor = Formatter.userPackageColor if self._isUserPackage(pkgName) else Formatter.systemPackageColor


            # ==> PRINT PACKAGE NAME WITH COLOR AND INDEX
            print(f"({index}) {Formatter.colorText(highlightedName, pkgColor, Formatter.bold)}")
            index += 1


            # ==> PRINT DESCRIPTION IF AVAILABLE
            if pkgDesc:
                # ==> TRUNCATE DESCRIPTION IF IT EXCEEDS TERMINAL WIDTH
                if len(pkgDesc) > maxDescWidth:
                    pkgDesc = pkgDesc[:maxDescWidth - 3] + "..."


                # ==> HIGHLIGHT MATCHING KEYWORDS IN DESCRIPTION
                highlightedDesc = self._highlightKeyword(pkgDesc, keyword)


                # ==> PRINT DESCRIPTION WITH INDENTATION AND COLOR
                print(f"{Formatter.tab8}Description:")
                print(f"{Formatter.tab8}{Formatter.tab4}{Formatter.colorText(highlightedDesc, Formatter.white)}")










    def _highlightKeyword(self, text: str, keyword: str) -> str:
        lowerText = text.lower()
        lowerKey = keyword.lower()
        start = 0
        result = ""
        
        
        while True:
            idx = lowerText.find(lowerKey, start)
            if idx == -1:
                result += text[start:]
                break
            result += text[start:idx] + Formatter.colorText(
                text[idx:idx + len(keyword)], Formatter.green, Formatter.bold
            )
            start = idx + len(keyword)
            
            
        return result
    
    
    
    
    
    
    
    
    
    
    
    def why(self, packageName: str) -> None:
        try:
            if not self._packageExists(packageName):
                print(Formatter.colorText(f"Package '{packageName}' not found.", Formatter.red))
                return

            # ==> PRELOAD ALL REVERSE DEPENDENCIES ONCE
            reverseMap = self._buildReverseDepMap()


            self._drawTree(packageName, reverseMap)
            
            
        except Exception as error:
            logError(f"Failed to check reverse dependencies ({error})")







    def _buildReverseDepMap(self) -> dict:
        reverseMap = {}
        
        
        
        # ==> HANDLE PACMAN PACKAGE MANAGER
        if self.pactool.manager.defaultPackageManager == "pacman":
            result = run(["pacman", "-Qi"], capture_output=True, text=True, check=False).stdout
            currentPkg = None
            
            
            # ==> ITERATE OVER EACH LINE OF OUTPUT
            for line in result.splitlines():
                if line.startswith("Name            :"):
                    currentPkg = line.split(":", 1)[1].strip()
                
                
                # ==> DETECT "Required By" LINE FOR THE CURRENT PACKAGE
                elif line.startswith("Required By     :") and currentPkg:
                    deps = line.split(":", 1)[1].strip()
                    reverseMap[currentPkg] = [] if deps == "None" else deps.split()
                    
                    
                    
                    
        elif self.pactool.manager.defaultPackageManager == "apt":
            # ==> GET A LIST OF INSTALLED PACKAGES
            pkgListResult = run(
                ["dpkg-query", "-W", "-f=${Package}\n"],
                capture_output=True, text=True, check=False
            ).stdout.splitlines()



            # ==> BUILD REVERSE DEPENDENCY MAP FOR EACH PACKAGE
            for pkg in pkgListResult:
                rdependsResult = run(
                    ["apt-cache", "rdepends", pkg],
                    capture_output=True, text=True, check=False
                ).stdout.splitlines()



                deps = []
                for line in rdependsResult:
                    line = line.strip()
                    
                    
                    # ==> SKIP HEADERS
                    if not line or line.startswith("Reverse Depends:") or line == pkg:
                        continue
                    
                    
                    # ==> ADD VALID DEPENDENCIES
                    deps.append(line)
                
                
                reverseMap[pkg] = deps
            
        
        return reverseMap




    
    
    
    
    
    def _drawTree(self, pkg: str, reverseMap: dict, depth: int = 0, visited=None) -> None:
        if visited is None:
            visited = set()
            
            
        if pkg in visited:
            return
        visited.add(pkg)


        prefix = "  " * depth + ("└─ " if depth > 0 else "")
        print(f"{prefix}{Formatter.colorText(pkg, Formatter.green)}")


        for dep in reverseMap.get(pkg, []):
            self._drawTree(dep, reverseMap, depth + 1, visited)
                







    def _packageExists(self, pkg: str) -> bool:
        if self.pactool.manager.defaultPackageManager == "pacman":
            return run(["pacman", "-Qi", pkg], capture_output=True, text=True, check=False).returncode == 0
        
        
        elif self.pactool.manager.defaultPackageManager == "apt":
            return run(["dpkg", "-s", pkg], capture_output=True, text=True, check=False).returncode == 0
        
        
        return False







    def stats(self, limit: int = None, headerText: str = "Package Statistics") -> None:
        try:
            # ==> COLLECT PACKAGE LIST FROM APT OR PACMAN
            packageList = self.collectAptPackages() if self.pactool.manager.defaultPackageManager == "apt" else self.collectPacmanPackages()
            if not packageList:
                print(Formatter.colorText("No packages found.", Formatter.red, Formatter.bold))
                return



            # ==> APPLY LIMIT IF PROVIDED (ONLY TAKE FIRST 'limit' PACKAGES)
            if limit is not None and limit > 0:
                packageList = packageList[:limit]



            # ==> FIND LARGEST AND SMALLEST PACKAGE BY SIZE
            largest = max(packageList, key=lambda p: float(p["sizeValue"]))
            smallest = min(packageList, key=lambda p: float(p["sizeValue"]))



            # ==> HELPER FUNCTION TO CONVERT DATE STRING TO DATETIME OBJECT
            def parseDate(dateStr):
                try:
                    return datetime.strptime(dateStr, "%a %d %b %Y %I:%M:%S %p %z")
                except ValueError:
                    return datetime.min



            # ==> FIND OLDEST AND LATEST INSTALL DATES
            oldestInstalled = min(packageList, key=lambda p: parseDate(p["installed"]))
            latestInstalled = max(packageList, key=lambda p: parseDate(p["installed"]))



            # ==> FIND OLDEST AND LATEST UPDATE DATES
            oldestUpdated = min(packageList, key=lambda p: parseDate(p["updated"]))
            latestUpdated = max(packageList, key=lambda p: parseDate(p["updated"]))



            # ==> CALCULATE WIDTHS FOR CLEAN COLUMN ALIGNMENT
            nameWidth = max(len(pkg["name"]) for pkg in [largest, smallest, oldestInstalled, latestInstalled, oldestUpdated, latestUpdated])
            sizeValueWidth = max(len(pkg["sizeValue"]) for pkg in [largest, smallest])
            sizeUnitWidth = max(len(pkg["sizeUnit"]) for pkg in [largest, smallest])
            
            
            
            # ==> PRINT HEADER AND COUNTS
            totalCount = len(packageList)


            # ==> SYSTEM/USER CLASSIFICATION
            userCount = 0
            systemCount = 0


            if self.pactool.manager.defaultPackageManager == "pacman":
                result = run(["pacman", "-Qe"], capture_output=True, text=True)
                userPkgs = {line.split()[0] for line in result.stdout.strip().splitlines() if line}
                for pkg in packageList:
                    if pkg["name"] in userPkgs:
                        userCount += 1
                    else:
                        systemCount += 1


            elif self.pactool.manager.defaultPackageManager == "apt":
                result = run(["apt-mark", "showmanual"], capture_output=True, text=True)
                userPkgs = {line.strip() for line in result.stdout.strip().splitlines() if line}
                for pkg in packageList:
                    if pkg["name"] in userPkgs:
                        userCount += 1
                    else:
                        systemCount += 1
                        
                        
                        
                        
            # ==> CALCULATE TOTAL, USER, AND SYSTEM SIZES
            def parseSize(pkg):
                try:
                    return float(pkg["sizeValue"])
                except ValueError:
                    return 0.0



            totalSize = sum(parseSize(pkg) for pkg in packageList)
            userSize = sum(parseSize(pkg) for pkg in packageList if pkg["name"] in userPkgs)
            systemSize = totalSize - userSize



            # ==> SPLIT FORMATTED SIZES INTO VALUE + UNIT
            def splitFormattedSize(sizeBytes):
                formatted = Formatter.formatSize(int(sizeBytes * 1024))
                parts = formatted.split()
                if len(parts) == 2:
                    return parts[0], parts[1]
                return formatted, ""



            totalValue, totalUnit = splitFormattedSize(totalSize)
            userValue, userUnit = splitFormattedSize(userSize)
            systemValue, systemUnit = splitFormattedSize(systemSize)



            # ==> CALCULATE WIDTHS FOR ALIGNMENT
            valueWidth = max(len(totalValue), len(userValue), len(systemValue))
            unitWidth = max(len(totalUnit), len(userUnit), len(systemUnit))



            ############################################################################
            # ==> DISPLAY RESULTS                                                      #
            ############################################################################



            # ==> FUNCTION TO GET PACKAGE COLOR BASED ON TYPE
            def getPackageColor(pkg):
                return Formatter.userPackageColor if pkg.get("isUser", False) else Formatter.systemPackageColor




            # ==> PRINT HEADER
            print(Formatter.colorText(headerText, Formatter.headerColor, Formatter.bold))
            print()





            # ==> PRINT PACKAGE INFO
            print(f"{Formatter.tab4}Total packages       ->  {Formatter.colorText(str(totalCount), Formatter.white, Formatter.bold)}")
            print(f"{Formatter.tab4}User-installed       ->  {Formatter.colorText(str(userCount), Formatter.userPackageColor)}")
            print(f"{Formatter.tab4}System dependencies  ->  {Formatter.colorText(str(systemCount), Formatter.systemPackageColor)}")
            print()

            # ==> PAD VALUES AND THEN APPLY COLOR
            print(f"{Formatter.tab4}Total size           ->  "
                f"{Formatter.colorText(totalValue.ljust(valueWidth), Formatter.sizeColor)} "
                f"{Formatter.colorText(totalUnit.ljust(unitWidth), Formatter.sizeColor)}")

            print(f"{Formatter.tab4}User-installed size  ->  "
                f"{Formatter.colorText(userValue.ljust(valueWidth), Formatter.sizeColor)} "
                f"{Formatter.colorText(userUnit.ljust(unitWidth), Formatter.sizeColor)}")

            print(f"{Formatter.tab4}System size          ->  "
                f"{Formatter.colorText(systemValue.ljust(valueWidth), Formatter.sizeColor)} "
                f"{Formatter.colorText(systemUnit.ljust(unitWidth), Formatter.sizeColor)}")
            print()




            # ==> PRINT SIZE STATISTICS
            print(f"{Formatter.tab4}{Formatter.bold}Size:{Formatter.reset}")
            
            largestName = f"{largest['name']:<{nameWidth}}"
            smallestName = f"{smallest['name']:<{nameWidth}}"

            largestSize = f"{largest['sizeValue']:<{sizeValueWidth}} {largest['sizeUnit']:<{sizeUnitWidth}}"
            smallestSize = f"{smallest['sizeValue']:<{sizeValueWidth}} {smallest['sizeUnit']:<{sizeUnitWidth}}"

            print(f"{Formatter.tab8}Largest package  ->  "
                f"{Formatter.colorText(largestName, getPackageColor(largest), Formatter.bold)}  "
                f"{Formatter.colorText(largestSize, Formatter.sizeColor)}")

            print(f"{Formatter.tab8}Smallest package ->  "
                f"{Formatter.colorText(smallestName, getPackageColor(smallest), Formatter.bold)}  "
                f"{Formatter.colorText(smallestSize, Formatter.sizeColor)}")
            print()





            # ==> PRINT INSTALLATION DATES
            print(f"{Formatter.tab4}{Formatter.bold}Installation Dates:{Formatter.reset}")
            
            oldestName = f"{oldestInstalled['name']:<{nameWidth}}"
            latestName = f"{latestInstalled['name']:<{nameWidth}}"

            print(f"{Formatter.tab8}Oldest installed ->  "
                f"{Formatter.colorText(oldestName, getPackageColor(oldestInstalled), Formatter.bold)}  "
                f"({Formatter.colorText(oldestInstalled['installed'], Formatter.dateColor)})")

            print(f"{Formatter.tab8}Latest installed ->  "
                f"{Formatter.colorText(latestName, getPackageColor(latestInstalled), Formatter.bold)}  "
                f"({Formatter.colorText(latestInstalled['installed'], Formatter.dateColor)})")
            print()





            # ==> PRINT UPDATE DATES
            print(f"{Formatter.tab4}{Formatter.bold}Update Dates:{Formatter.reset}")
            
            oldestUpdName = f"{oldestUpdated['name']:<{nameWidth}}"
            latestUpdName = f"{latestUpdated['name']:<{nameWidth}}"

            print(f"{Formatter.tab8}Oldest updated   ->  "
                f"{Formatter.colorText(oldestUpdName, getPackageColor(oldestUpdated), Formatter.bold)}  "
                f"({Formatter.colorText(oldestUpdated['updated'], Formatter.dateColor)})")

            print(f"{Formatter.tab8}Latest updated   ->  "
                f"{Formatter.colorText(latestUpdName, getPackageColor(latestUpdated), Formatter.bold)}  "
                f"({Formatter.colorText(latestUpdated['updated'], Formatter.dateColor)})")
            print()



        except Exception as error:
            logError(f"Failed to fetch package statistics ({error})")

    
    
    
    
    
    
    
    def listFiles(self, packageName: str) -> None:
        try:
            # ==> CHECK IF PACKAGE EXISTS
            if not self._packageExists(packageName):
                print(Formatter.colorText(f"Package '{packageName}' not found.", Formatter.red))
                return



            print(Formatter.colorText(f"\nFiles installed by '{packageName}':", Formatter.headerColor, Formatter.bold))
            print()



            if self.pactool.manager.defaultPackageManager == "pacman":
                result = run(["pacman", "-Ql", packageName], capture_output=True, text=True, check=False)
                files = [line.split(maxsplit=1)[1] for line in result.stdout.splitlines()]
            elif self.pactool.manager.defaultPackageManager == "apt":
                result = run(["dpkg", "-L", packageName], capture_output=True, text=True, check=False)
                files = result.stdout.splitlines()
            else:
                print(Formatter.colorText("No supported package manager found.", Formatter.red))
                return



            if not files or all(f.strip() == "" for f in files):
                print(Formatter.colorText(f"No files found for package '{packageName}'.", Formatter.yellow))
                return



            for f in files:
                print(f"{Formatter.tab4}{f}")


        except Exception as error:
            logError(f"Failed to list files for '{packageName}' ({error})")










    def uninstall(self, name: str) -> None:
        try:
            # ==> DETERMINE WHICH PACKAGE MANAGER TO USE
            if self.pactool.manager.defaultPackageManager == "apt":
                command = ["sudo", "apt", "remove", name, "-y"]
                print(Formatter.colorText(f"Using apt to uninstall '{name}'", Formatter.yellow, Formatter.bold))
            elif self.pactool.manager.defaultPackageManager == "pacman":
                command = ["sudo", "pacman", "-R", name]
                print(Formatter.colorText(f"Using pacman to uninstall '{name}'", Formatter.yellow, Formatter.bold))
            else:
                print(Formatter.colorText("No package manager found.", Formatter.red))
                return


            # ==> EXECUTE THE COMMAND
            print()
            run(command, check=True)
            print()


            # ==> SUCCESS MESSAGE
            print(Formatter.colorText(f"Successfully uninstalled '{name}'", Formatter.green, Formatter.bold))
            print()
            
            
            # ==> DISPLAY UPDATED STATS
            self.stats(headerText="Updated Package Statistics")


        except BaseException as error:
            logError(f"\nFailed to uninstall package '{name}' ({error})")


    
    
    
    
    
    
    
    def install(self, name: str) -> None:
        try:
            # ==> DETERMINE WHICH PACKAGE MANAGER TO USE
            if self.pactool.manager.defaultPackageManager == "apt":
                command = ["sudo", "apt", "install", name, "-y"]
                print(Formatter.colorText(f"Using apt to install '{name}'", Formatter.yellow, Formatter.bold))
            elif self.pactool.manager.defaultPackageManager == "pacman":
                command = ["sudo", "pacman", "-S", name]
                print(Formatter.colorText(f"Using pacman to install '{name}'", Formatter.yellow, Formatter.bold))
            else:
                print(Formatter.colorText("No package manager found.", Formatter.red))
                return


            # ==> EXECUTE THE COMMAND
            print()
            run(command, check=True)
            print()


            # ==> SUCCESS MESSAGE
            print(Formatter.colorText(f"Successfully installed '{name}'", Formatter.green, Formatter.bold))
            print()


            # ==> DISPLAY UPDATED STATS
            self.stats(headerText="Updated Package Statistics")


        except BaseException as error:
            logError(f"\nFailed to install package '{name}' ({error})")


    
    
    
    
    
    
    
    
    def update(self) -> None:
        try:
            # ==> DETERMINE WHICH PACKAGE MANAGER TO USE
            if self.pactool.manager.defaultPackageManager == "apt":
                command = ["sudo", "apt", "update"]
                print(Formatter.colorText("Using apt to update package lists", Formatter.yellow, Formatter.bold))
            elif self.pactool.manager.defaultPackageManager == "pacman":
                command = ["sudo", "pacman", "-Sy"]
                print(Formatter.colorText("Using pacman to update package lists", Formatter.yellow, Formatter.bold))
            else:
                print(Formatter.colorText("No package manager found.", Formatter.red))
                return


            # ==> EXECUTE THE COMMAND
            print()
            run(command, check=True)
            print()


            # ==> SUCCESS MESSAGE
            print(Formatter.colorText("Package lists updated successfully", Formatter.green, Formatter.bold))
            print()


            # ==> DISPLAY UPDATED STATS
            self.stats(headerText="Updated Package Statistics")


        except BaseException as error:
            logError(f"\nFailed to update packages ({error})")



    
    
    
    
    
    
    
    def upgrade(self) -> None:
        try:
            # ==> DETERMINE WHICH PACKAGE MANAGER TO USE
            if self.pactool.manager.defaultPackageManager == "apt":
                command = ["sudo", "apt", "upgrade", "-y"]
                print(Formatter.colorText("Using apt to upgrade packages", Formatter.yellow, Formatter.bold))
            elif self.pactool.manager.defaultPackageManager == "pacman":
                command = ["sudo", "pacman", "-Syu"]
                print(Formatter.colorText("Using pacman to upgrade packages", Formatter.yellow, Formatter.bold))
            else:
                print(Formatter.colorText("No package manager found.", Formatter.red))
                return


            # ==> EXECUTE THE COMMAND
            print()
            run(command, check=True)
            print()


            # ==> SUCCESS MESSAGE
            print(Formatter.colorText("Packages upgraded successfully", Formatter.green, Formatter.bold))
            print()


            # ==> DISPLAY UPDATED STATS
            self.stats(headerText="Updated Package Statistics")


        except BaseException as error:
            logError(f"\nFailed to upgrade packages ({error})")










    def collectAptPackages(self) -> list:
        result = run(
            ["dpkg-query", "-W", "-f=${Package} ${Installed-Size}\n"],
            capture_output=True, text=True, check=True
        )


        packages = []
        for line in result.stdout.strip().split("\n"):
            parts = line.split()
            if len(parts) < 2:
                continue


            packageName = parts[0]
            sizeKb = int(parts[1])


            # ==> SPLIT SIZE INTO VALUE AND UNIT
            sizeVal, sizeUnit = self.splitSize(Formatter.formatSize(sizeKb * 1024))


            # ==> GET INSTALL AND UPDATE DATES
            infoFile = f"/var/lib/dpkg/info/{packageName}.list"
            installedTime, installedTs = self.getFileDate(infoFile, returnTimestamp=True)
            updatedTime, updatedTs = self.getFileDate(infoFile, updated=True, returnTimestamp=True)


            # ==> APPEND PACKAGE DATA
            packages.append({
                "name": packageName,
                "sizeValue": sizeVal,
                "sizeUnit": sizeUnit,
                "installed": installedTime,
                "updated": updatedTime,
                "installedTs": installedTs,
                "updatedTs": updatedTs
            })


        return packages
    
    
    
    
    
    
    
    
    

    def collectPacmanPackages(self) -> list:
        result = run(["pacman", "-Qi"], capture_output=True, text=True, check=True)
        blocks = result.stdout.strip().split("\n\n")


        packages = []
        for block in blocks:
            packageData = self.parsePacmanBlock(block)
            if packageData:
                packages.append(packageData)


        return packages








    def parsePacmanBlock(self, block: str) -> dict:
        lines = block.split("\n")
        info = {}


        for line in lines:
            if line.startswith("Name"):
                info["name"] = line.split(":", 1)[1].strip()
                
                
            elif line.startswith("Installed Size"):
                sizeStr = line.split(":", 1)[1].strip()
                sizeVal, sizeUnit = self.splitSize(sizeStr)
                info["sizeValue"] = sizeVal
                info["sizeUnit"] = sizeUnit
                
                
            elif line.startswith("Install Date"):
                dateStr = line.split(":", 1)[1].strip()
                info["installed"] = info["updated"] = dateStr


                # ==> CONVERT PARSED DATE TO TIMESTAMP (FALL BACK TO 0)
                dt = self._parseDate(dateStr)
                try:
                    ts = dt.timestamp()
                except (OverflowError, ValueError, OSError):
                    ts = 0

                info["installedTs"] = info["updatedTs"] = ts


        return info if "name" in info else None









    def splitSize(self, sizeStr: str):
        parts = sizeStr.split()
        return (parts[0], parts[1]) if len(parts) == 2 else (sizeStr, "")









    def getFileDate(self, path: str, *, updated=False, returnTimestamp=False):
        try:
            st = stat(path)
            ts = st.st_mtime if updated else st.st_ctime
            nice = datetime.fromtimestamp(ts).strftime("%a %d %b %Y %I:%M:%S %p %z")
            return (nice, ts) if returnTimestamp else nice
        except FileNotFoundError:
            return ("N/A", 0) if returnTimestamp else "N/A"



        
        
        
        
        
        
        
        
    def _isUserPackage(self, packageName: str) -> bool:
        if not hasattr(self, "_cachedUserPkgs"):
            self._cachedUserPkgs = set()
            
            
            if self.pactool.manager.defaultPackageManager == "pacman":
                result = run(["pacman", "-Qe"], capture_output=True, text=True)
                self._cachedUserPkgs = {line.split()[0] for line in result.stdout.strip().splitlines() if line}
                
                
            elif self.pactool.manager.defaultPackageManager == "apt":
                result = run(["apt-mark", "showmanual"], capture_output=True, text=True)
                self._cachedUserPkgs = {line.strip() for line in result.stdout.strip().splitlines() if line}
                
                
        return packageName.split()[0] in self._cachedUserPkgs
    
    
    
    
    
    
    
    
    def clean(self) -> None:
        try:
            # ==> CLEAN APT PACKAGE CACHE
            if self.pactool.manager.defaultPackageManager == "apt":
                print(Formatter.colorText("Cleaning APT package cache [...]", Formatter.yellow, Formatter.bold))
                run(["sudo", "apt-get", "clean"], stdout=DEVNULL, stderr=DEVNULL, check=False)
                run(["sudo", "apt-get", "autoremove", "-y"], stdout=DEVNULL, stderr=DEVNULL, check=False)
                print(Formatter.colorText("\nAPT package cache cleaned.", Formatter.green, Formatter.bold))


            # ==> CLEAN PACMAN PACKAGE CACHE
            elif self.pactool.manager.defaultPackageManager == "pacman":
                print(Formatter.colorText("Cleaning Pacman package cache [...]", Formatter.yellow, Formatter.bold))
                run(["sudo", "pacman", "-Scc", "--noconfirm"], stdout=DEVNULL, stderr=DEVNULL, check=False)
                print(Formatter.colorText("\nPacman package cache cleaned.", Formatter.green, Formatter.bold))

            else:
                print(Formatter.colorText("\nNo supported package manager found for cleaning.", Formatter.red))


        except Exception as error:
            logError(f"\nFailed to clean package cache ({error})")
            
            
        # ==> SHOW THE NEW STATS
        print()
        self.stats()







    def info(self, packageName: str) -> None:
        try:
            # ==> CHECK IF PACKAGE EXISTS
            if not self._packageExists(packageName):
                print(Formatter.colorText(f"Package '{packageName}' not found.", Formatter.red))
                return


            # ==> GET PACKAGE INFO BASED ON PACKAGE MANAGER
            if self.pactool.manager.defaultPackageManager == "pacman":
                result = run(["pacman", "-Qi", packageName], capture_output=True, text=True, check=False).stdout
                self._displayPackageInfoPacman(result)
            elif self.pactool.manager.defaultPackageManager == "apt":
                result = run(["apt-cache", "show", packageName], capture_output=True, text=True, check=False).stdout
                self._displayPackageInfoApt(result)
            else:
                print(Formatter.colorText("No supported package manager found.", Formatter.red))


        except Exception as error:
            logError(f"Failed to get package info ({error})")





    def _displayPackageInfoPacman(self, info: str) -> None:
        print(Formatter.colorText("\nPackage Information:\n", Formatter.headerColor, Formatter.bold))
        
        for line in info.splitlines():
            # ==> SPLIT LINE INTO KEY AND VALUE
            if line.startswith("Name") or line.startswith("Version") or line.startswith("Installed Size") or line.startswith("Install Date"):
                key, value = line.split(":", 1)
                print(f"{Formatter.colorText(key.strip() + ':', Formatter.cyan)} {Formatter.colorText(value.strip(), Formatter.white)}")

            
            # ==> SPECIAL HANDLING FOR DEPENDENCIES
            elif line.startswith("Depends On"):
                key, value = line.split(":", 1)
                dependencies = value.strip().split()
                print(f"{Formatter.colorText('Depends On:', Formatter.cyan)}")
                
                
                # ==> PRINT EACH DEPENDENCY ON A NEW LINE IN TREE FORMAT
                for dep in dependencies:
                    print(f"  └─ {Formatter.colorText(dep, Formatter.green)}")







    def _displayPackageInfoApt(self, info: str) -> None:
        print(Formatter.colorText("\nPackage Information:\n", Formatter.headerColor, Formatter.bold))
        
        for line in info.splitlines():
            # ==> SPLIT LINE INTO KEY AND VALUE
            if line.startswith("Package") or line.startswith("Version") or line.startswith("Installed-Size") or line.startswith("Description"):
                key, value = line.split(":", 1)
                print(f"{Formatter.colorText(key.strip() + ':', Formatter.cyan)} {Formatter.colorText(value.strip(), Formatter.white)}")


            # ==> SPECIAL HANDLING FOR DEPENDENCIES
            elif line.startswith("Depends"):
                key, value = line.split(":", 1)
                dependencies = [dep.strip() for dep in value.split(',')]
                print(f"{Formatter.colorText('Depends On:', Formatter.cyan)}")
                
                
                # ==> PRINT EACH DEPENDENCY ON A NEW LINE IN TREE FORMAT
                for dep in dependencies:
                    print(f"  └─ {Formatter.colorText(dep, Formatter.green)}")







    # ==> FIND UNUSED OPTIONAL DEPENDENCIES (BLOAT)
    def bloat(self, limit: int = None) -> None:
        try:
            # ==> PRINT HEADER
            print(Formatter.colorText("\nAnalyzing for bloat (unused optional dependencies) [...]\n", Formatter.headerColor, Formatter.bold))



            bloatList = []
            userPkgs = set(self._getUserPackages())



            # ==> PACMAN IMPLEMENTATION
            if self.pactool.manager.defaultPackageManager == "pacman":
                result = run(["pacman", "-Qi"], capture_output=True, text=True, check=False)
                currentPkg = None

                for line in result.stdout.splitlines():
                    if line.startswith("Name"):
                        currentPkg = line.split(":", 1)[1].strip()
                    elif line.startswith("Optional Deps") and currentPkg:
                        if "None" not in line:
                            bloatList.append(currentPkg)



            # ==> APT IMPLEMENTATION
            elif self.pactool.manager.defaultPackageManager == "apt":
                installedPkgs = run(
                    ["dpkg-query", "-f", "${binary:Package}\n", "-W"],
                    capture_output=True,
                    text=True
                ).stdout.splitlines()



                for pkg in installedPkgs:
                    info = run(["apt-cache", "show", pkg], capture_output=True, text=True).stdout
                    for line in info.splitlines():
                        if line.startswith("Recommends:") or line.startswith("Suggests:"):
                            bloatList.append(pkg)
                            break



            # ==> DISPLAY RESULTS
            if bloatList:
                print(Formatter.colorText("Packages with unused optional dependencies:\n", Formatter.yellow))
                
                
                # ==> WIDTH OF THE INDEX COLUMN
                indexWidth = len(str(len(bloatList)))
                
                
                # ==> WIDTH OF PACKAGE NAME COLUMN
                nameWidth = max(len(pkg) for pkg in bloatList) + 2


                def renderChunk(chunk, startIndex=0):
                    for i, pkg in enumerate(chunk, start=startIndex + 1):
                        color = Formatter.magenta if pkg in userPkgs else Formatter.blue
                        print(f"  {Formatter.bold}{Formatter.white}{str(i).rjust(indexWidth)}{Formatter.reset}. {Formatter.colorText(pkg.ljust(nameWidth), color)}")


                self._paginate(bloatList, renderChunk, limit)
            else:
                print(Formatter.colorText("No bloat detected.", Formatter.green))


        except Exception as error:
            logError(f"Failed to check bloat ({error})")









    # ==> FIND UNUSED ORPHANED PACKAGES
    def unused(self, limit: int = None) -> None:
        try:
            # ==> PRINT HEADER
            print(Formatter.colorText("\nFinding unused (Orphan) packages [...]\n", Formatter.headerColor, Formatter.bold))


            # ==> CHECK FOR PACMAN PACKAGE MANAGER
            if self.pactool.manager.defaultPackageManager == "pacman":
                result = run(["pacman", "-Qdtq"], capture_output=True, text=True, check=False)
                orphaned = result.stdout.splitlines()


            # ==> CHECK FOR APT PACKAGE MANAGER
            elif self.pactool.manager.defaultPackageManager == "apt":
                result = run(["apt-mark", "showauto"], capture_output=True, text=True, check=False)
                orphaned = [line.strip() for line in result.stdout.splitlines() if line.strip()]


            else:
                orphaned = []


            # ==> HANDLE NO UNUSED PACKAGES FOUND
            if not orphaned:
                print(Formatter.colorText("No unused packages found.", Formatter.green))
                return


            # ==> DISPLAY HEADER
            print(Formatter.colorText("Unused packages:\n", Formatter.yellow))


            # ==> CALCULATE WIDTHS
            indexWidth = len(str(len(orphaned)))
            nameWidth = max(len(pkg) for pkg in orphaned) + 2


            # ==> RENDER FUNCTION
            def renderChunk(chunk, startIndex=0):
                for i, pkg in enumerate(chunk, start=startIndex + 1):
                    print(f"  {Formatter.bold}{Formatter.white}{str(i).rjust(indexWidth)}{Formatter.reset}. {Formatter.colorText(pkg.ljust(nameWidth), Formatter.magenta)}")


            # ==> PAGINATE RESULTS
            self._paginate(orphaned, renderChunk, limit)


        except Exception as error:
            logError(f"Failed to check unused packages ({error})")
            
            
            
            
            
            
            
            
            
    # ==> LIST ALL OUTDATED PACKAGES
    def outdated(self, limit: int = None) -> None:
        try:
            # ==> PRINT HEADER
            print(Formatter.colorText("\nChecking for outdated packages [...]\n", Formatter.headerColor, Formatter.bold))


            outdatedPkgs = []
            userPkgs = set(self._getUserPackages())


            # ==> PACMAN IMPLEMENTATION
            if self.pactool.manager.defaultPackageManager == "pacman":
                # ==> RUN PACMAN SYNC TO LIST OUTDATED PACKAGES
                result = run(["pacman", "-Qu"], capture_output=True, text=True, check=False)


                for line in result.stdout.splitlines():
                    # ==> FORMAT (packageName currentVersion -> newVersion)
                    parts = line.split()
                    if len(parts) >= 4:
                        outdatedPkgs.append((parts[0], parts[1], parts[3]))


            # ==> APT IMPLEMENTATION
            elif self.pactool.manager.defaultPackageManager == "apt":
                # ==> UPDATE PACKAGE INFO
                run(["sudo", "apt", "update"], stdout=PIPE, stderr=PIPE, text=True)


                # ==> CHECK OUTDATED PACKAGES USING APT LIST
                result = run(["apt", "list", "--upgradable"], capture_output=True, text=True, check=False)


                for line in result.stdout.splitlines():
                    # ==> SKIP HEADERS
                    if "Listing [...]" in line:
                        continue
                    
                    
                    parts = line.split()
                    if len(parts) >= 3:
                        pkg = parts[0].split("/")[0]
                        current = parts[1]
                        newVersion = parts[2] if len(parts) > 2 else "?"
                        outdatedPkgs.append((pkg, current, newVersion))


            # ==> HANDLE EMPTY RESULT
            if not outdatedPkgs:
                print(Formatter.colorText("All packages are up-to-date.", Formatter.green))
                return


            # ==> WIDTH CALCULATIONS FOR CLEAN OUTPUT
            indexWidth = len(str(len(outdatedPkgs)))
            nameWidth = max(len(pkg[0]) for pkg in outdatedPkgs) + 2
            currentWidth = max(len(pkg[1]) for pkg in outdatedPkgs) + 2
            newWidth = max(len(pkg[2]) for pkg in outdatedPkgs) + 2


            # ==> GET USER PACKAGES TO DETERMINE COLOR
            userPkgs = self._getUserPackages()


            # ==> DISPLAY OUTDATED PACKAGES HEADER
            print(Formatter.colorText("Outdated Packages:\n", Formatter.headerColor, Formatter.bold))


            # ==> RENDER FUNCTION FOR PAGINATION
            def renderChunk(chunk, startIndex=0):
                for i, (pkg, current, new) in enumerate(chunk, start=startIndex + 1):
                    # ==> DETERMINE COLOR BASED ON USER OR SYSTEM PACKAGE
                    color = Formatter.magenta if pkg in userPkgs else Formatter.blue


                    print(
                        f"  {Formatter.bold}{Formatter.white}{str(i).rjust(indexWidth)}{Formatter.reset}. "
                        f"{Formatter.colorText(pkg.ljust(nameWidth), color)} "
                        f"{Formatter.colorText(current.ljust(currentWidth), Formatter.cyan)} -> "
                        f"{Formatter.colorText(new.ljust(newWidth), Formatter.yellow)}"
                    )


            # ==> PAGINATE OUTPUT
            self._paginate(outdatedPkgs, renderChunk, limit)


        except Exception as error:
            logError(f"Failed to list outdated packages ({error})")







    def history(self, packageName: str) -> None:
        try:
            # ==> CHECK IF PACKAGE EXISTS
            if not self._packageExists(packageName):
                print(Formatter.colorText(f"Package '{packageName}' not found.", Formatter.red))
                return


            # ==> DETERMINE PACKAGE COLOR
            pkgColor = Formatter.packageColor if self._isUserPackage(packageName) else Formatter.systemPackageColor


            # ==> PRINT HEADER
            print(Formatter.colorText(f"\nPackage Version History for '{packageName}':\n", Formatter.headerColor, Formatter.bold))


            # ==> LIST TO STORE EVENTS
            events = []
            commandUsed = None


            ################################################################################
            # ==> PACMAN                                                                   #
            ################################################################################
            if self.pactool.manager.defaultPackageManager == "pacman":
                logData = run(["grep", packageName, "/var/log/pacman.log"], capture_output=True, text=True).stdout.splitlines()
                if not logData:
                    print(Formatter.colorText("No version history found.", Formatter.yellow))
                    return


                for line in logData:
                    if "[PACMAN]" in line and packageName in line:
                        commandUsed = line.split("]")[-1].strip().replace("Running '", "").replace("'", "")
                    
                    
                    elif "[ALPM]" in line and ("installed" in line or "upgraded" in line):
                        timestamp = line.split()[0].strip("[]")

                        # ==> DETERMINE ACTION AND VERSION INFO
                        if "upgraded" in line:
                            oldVer = line.split("from")[-1].split()[0].strip("()")
                            newVer = line.split("to")[-1].split()[0].strip("()")
                            version = f"{oldVer} -> {newVer}"
                            action = " Upgraded"
                        else:
                            version = line.split(packageName)[-1].strip().strip("()")
                            action = "Installed"

                        timeStr = Formatter.formatHistoryTime(timestamp)
                        events.append((action, version, timeStr))



            ################################################################################
            # ==> APT                                                                      #
            ################################################################################
            elif self.pactool.manager.defaultPackageManager == "apt":
                logData = run(["grep", "-i", packageName, "/var/log/apt/history.log"], capture_output=True, text=True).stdout.splitlines()
                if not logData:
                    print(Formatter.colorText("No version history found.", Formatter.yellow))
                    return


                for line in logData:
                    if "Commandline:" in line:
                        commandUsed = line.split("Commandline:")[-1].strip()
                    
                    
                    elif "Install" in line or "Upgrade" in line:
                        action = "Installed" if "Install" in line else " Upgraded"
                        version = line.split()[-1]
                        dateStr = self._extractAptDate()
                        timeStr = Formatter.formatHistoryTime(dateStr)
                        events.append((action, version, timeStr))



            ################################################################################
            # ==> PRINT COLLECTED EVENTS WITH ALIGNMENT                                    #
            ################################################################################
            if not events:
                print(Formatter.colorText("No install or upgrade events found.", Formatter.yellow))
                return


            # ==> CALCULATE MAX WIDTH FOR ALIGNMENT
            maxWidth = max(len(f"{a} {packageName} ({v})") for a, v, _ in events)


            # ==> PRINT EVENTS WITH EVEN SPACING
            for action, version, timeStr in events:
                baseStr = f"{action} {packageName} ({version})"
                padding = " " * (maxWidth - len(baseStr))
                
                print(f"{Formatter.tab4}{Formatter.colorText(action, Formatter.white, Formatter.bold)} "
                    f"{Formatter.colorText(packageName, pkgColor)} "
                    f"({Formatter.colorText(version, Formatter.cyan)}){padding} "
                    f"on {Formatter.colorText(timeStr, Formatter.dateColor)}")



            ################################################################################
            # ==> PRINT COMMAND USED                                                       #
            ################################################################################
            if commandUsed:
                print(f"\n{Formatter.tab4}{Formatter.colorText('Command used:', Formatter.brightWhite, Formatter.bold)}")
                highlightedCommand = self._highlightCommandPackage(commandUsed, packageName, pkgColor)
                print(f"{Formatter.tab8}{highlightedCommand}")



            ################################################################################
            # ==> SHOW VERSION TREE                                                        #
            ################################################################################
            print()
            self._showVersionTree(packageName)



        except Exception as error:
            logError(f"Failed to get package history for '{packageName}' ({error})")








    def _showVersionTree(self, packageName: str) -> None:
        # ==> PRINT HEADER
        print(Formatter.colorText("\n    Version Tree:", Formatter.headerColor, Formatter.bold))
        versions = []



        ################################################################################
        # ==> PACMAN IMPLEMENTATION                                                    #
        ################################################################################
        if self.pactool.manager.defaultPackageManager == "pacman":
            currentVer = run(["pacman", "-Q", packageName], capture_output=True, text=True).stdout.split()[1]
            logData = run(["grep", packageName, "/var/log/pacman.log"], capture_output=True, text=True).stdout.splitlines()



            # ==> COLLECT VERSIONS
            for line in logData:
                if "[ALPM]" in line:
                    if "upgraded" in line:
                        parts = line.split()
                        oldVer = parts[-3].strip("()")
                        newVer = parts[-1].strip("()")
                        versions.append((oldVer, newVer))
                        
                        
                    elif "installed" in line:
                        ver = line.split(packageName)[-1].strip().strip("()")
                        versions.append((ver, None))



            versions = list(dict.fromkeys(versions))


            # ==> FIND MAX LENGTHS FOR LEFT AND RIGHT VERSIONS
            leftMax = max(len(v[0]) for v in versions)
            rightMax = max(len(v[1]) if v[1] else 0 for v in versions)



            # ==> PRINT TREE WITH ALIGNMENT
            for i, (oldVer, newVer) in enumerate(versions):
                prefix = "└─ " if i == len(versions) - 1 else "├─ "
                
                if newVer:
                    left = oldVer.ljust(leftMax)
                    right = newVer.ljust(rightMax)
                    combined = f"{left} -> {right}"
                    isCurrent = (newVer == currentVer)
                else:
                    combined = oldVer.ljust(leftMax)
                    isCurrent = (oldVer == currentVer)



                suffix = " " + Formatter.colorText("(Current)", Formatter.brightWhite, Formatter.bold) if isCurrent else ""
                color = Formatter.green if isCurrent else Formatter.cyan


                print(f"{Formatter.tab8}{prefix}{Formatter.colorText(combined, color)}{suffix}")






        ################################################################################
        # ==> APT IMPLEMENTATION                                                       #
        ################################################################################
        elif self.pactool.manager.defaultPackageManager == "apt":
            currentVer = run(
                ["dpkg-query", "-W", "-f=${Version}", packageName],
                capture_output=True, text=True
            ).stdout.strip()
            result = run(["apt-cache", "madison", packageName], capture_output=True, text=True).stdout.splitlines()



            for line in result:
                parts = line.split("|")
                if len(parts) >= 2:
                    versions.append((parts[1].strip(), None))



            leftMax = max(len(v[0]) for v in versions)



            for i, (ver, _) in enumerate(versions):
                prefix = "└─ " if i == len(versions) - 1 else "├─ "
                isCurrent = (ver == currentVer)
                suffix = " " + Formatter.colorText("(Current)", Formatter.brightWhite, Formatter.bold) if isCurrent else ""
                color = Formatter.green if isCurrent else Formatter.cyan
                print(f"{Formatter.tab8}{prefix}{Formatter.colorText(ver.ljust(leftMax), color)}{suffix}")










    def _highlightCommandPackage(self, command: str, packageName: str, pkgColor: str) -> str:
        # ==> HIGHLIGHTS ONLY THE PACKAGE NAME WITHIN THE COMMAND STRING
        parts = command.split()
        highlightedParts = [
            Formatter.colorText(p, pkgColor) if p == packageName else p
            for p in parts
        ]
        return " ".join(highlightedParts)










    def versions(self, packageName: str, assessRisk: bool = False) -> None:
        try:
            # ==> CHECK IF PACKAGE EXISTS
            if not self._packageExists(packageName):
                print(Formatter.colorText(f"Package '{packageName}' not found.", Formatter.red))
                return


            # ==> DETERMINE PACKAGE COLOR
            pkgColor = Formatter.packageColor if self._isUserPackage(packageName) else Formatter.systemPackageColor


            # ==> COLLECT VERSIONS
            versions = []
            currentVer = None


            ################################################################################
            # ==> PACMAN IMPLEMENTATION
            ################################################################################
            if self.pactool.manager.defaultPackageManager == "pacman":
                currentVer = run(["pacman", "-Q", packageName], capture_output=True, text=True).stdout.split()[1].strip()
                repoData = run(["pacman", "-Ss", packageName], capture_output=True, text=True).stdout.splitlines()


                for line in repoData:
                    if "/" in line and packageName in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            versions.append(parts[1].strip())



            ################################################################################
            # ==> APT IMPLEMENTATION
            ################################################################################
            elif self.pactool.manager.defaultPackageManager == "apt":
                currentVer = run(["dpkg-query", "-W", "-f=${Version}", packageName], capture_output=True, text=True).stdout.strip()
                repoData = run(["apt-cache", "madison", packageName], capture_output=True, text=True).stdout.splitlines()


                for line in repoData:
                    parts = line.split("|")
                    if len(parts) >= 2:
                        versions.append(parts[1].strip())



            # ==> REMOVE DUPLICATES
            versions = list(dict.fromkeys(versions))


            if not versions:
                print(f"{Formatter.colorText('No version data available.', Formatter.yellow)}")
                return



            ################################################################################
            # ==> ASSESS RISK IF ENABLED
            ################################################################################
            riskInfo = []
            
            
            if assessRisk:
                assessingText = f"Assessing risk for '{packageName}'"
                print(Formatter.colorText(assessingText, Formatter.brightYellow, Formatter.bold), end="", flush=True)


                spinnerActive = True
                spinnerChars = ['[|]', '[/]', '[-]', '[\\]']
                spinnerIndex = 0


                def spinner():
                    nonlocal spinnerIndex
                    while spinnerActive:
                        sysStdout.write(f"\r{Formatter.colorText(assessingText + ' ' + spinnerChars[spinnerIndex % 4], Formatter.brightYellow, Formatter.bold)}")
                        sysStdout.flush()
                        spinnerIndex += 1
                        timeSleep(0.1)



                spinnerThread = SafeThread(target=spinner)
                spinnerThread.start()



                # ==> PERFORM RISK CALCULATIONS
                for v in versions:
                    riskLevel, vulnCount = self._getVulnerabilityInfo(packageName, v)
                    riskInfo.append((v, riskLevel, vulnCount))



                spinnerActive = False
                spinnerThread.join()
                print("\r" + " " * 60 + "\r", end="")

            else:
                riskInfo = [(v, "", 0) for v in versions]

                    
                    

            ################################################################################
            # ==> CALCULATE PADDING WIDTHS
            ################################################################################
            
            maxVerLen = max(len(v[0]) for v in riskInfo)
            maxRiskLen = max(len(v[1]) for v in riskInfo) if assessRisk else 0



            ################################################################################
            # ==> PRINT VERSION LIST
            ################################################################################
            
            
            # ==> PRINT HEADER
            print(Formatter.colorText(f"\nAvailable Versions for '{packageName}':\n", Formatter.headerColor, Formatter.bold))
            
            
            
            for i, (ver, riskLevel, vulnCount) in enumerate(riskInfo):
                prefix = "└─ " if i == len(riskInfo) - 1 else "├─ "
                verColor = Formatter.green if ver == currentVer else Formatter.cyan
                suffix = " " + Formatter.colorText("(Current)", Formatter.brightWhite, Formatter.bold) if ver == currentVer else ""


                verPadding = " " * (maxVerLen - len(ver))
                riskText = f" [{riskLevel}] {vulnCount} CVEs" if assessRisk else ""
                riskPadding = " " * (maxRiskLen - len(riskLevel)) if assessRisk else ""


                print(
                    f"{Formatter.tab4}{prefix}"
                    f"{Formatter.colorText(ver, verColor)}{verPadding}"
                    f"{riskText}{riskPadding:2}"
                    f"{suffix}"
                )




        except Exception as error:
            logError(f"Failed to get versions for '{packageName}' ({error})")










    def _getVulnerabilityInfo(self, packageName: str, version: str) -> tuple:
        """
        Returns (riskLevel, vulnCount) for a package version.
        Uses the NVD API (no third-party libraries).
        """
        
        
        try:
            # ==> BUILD QUERY URL
            baseUrl = "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch="
            query = quote(f"{packageName} {version}")
            url = f"{baseUrl}{query}"


            # ==> SEND HTTP REQUEST
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=10) as response:
                data = jsonLoads(response.read().decode("utf-8"))


            # ==> PARSE CVE COUNT
            vulnCount = len(data.get("vulnerabilities", []))


            # ==> DETERMINE RISK LEVEL
            if vulnCount == 0:
                riskLevel = Formatter.colorText("Low risk", Formatter.green, Formatter.bold)
            elif vulnCount <= 5:
                riskLevel = Formatter.colorText("Medium risk", Formatter.yellow, Formatter.bold)
            else:
                riskLevel = Formatter.colorText("High risk", Formatter.red, Formatter.bold)


            return (riskLevel, vulnCount)



        except Exception as error:
            # ==> IF API FAILS, RETURN SAFE DEFAULT
            return (Formatter.colorText("Unknown", Formatter.brightBlack, Formatter.bold), 0)

