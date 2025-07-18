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
#                                MODULES                                 #
#                                                                        #
##########################################################################

from shutil import get_terminal_size
from subprocess import run, CalledProcessError, DEVNULL
from datetime import datetime
from os import stat
from re import search


# ==> PACTOOL FILES
from core.logger import logError
from core.formatter import Formatter




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
                userInput = input(
                    Formatter.colorText("\nPress Enter to view more (or 'q' to quit): ", Formatter.cyan)
                ).strip().lower()
                if userInput == "q":
                    break
                print()








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
            self._paginate(packages, lambda chunk, startIndex=0: self._printSearchResults(chunk, name, startIndex), None)


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


            print(Formatter.colorText(f"\nReverse dependency tree for '{packageName}':", Formatter.headerColor, Formatter.bold))
            print()


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
                print(Formatter.colorText("Cleaning APT package cache...", Formatter.yellow, Formatter.bold))
                run(["sudo", "apt-get", "clean"], stdout=DEVNULL, stderr=DEVNULL, check=False)
                run(["sudo", "apt-get", "autoremove", "-y"], stdout=DEVNULL, stderr=DEVNULL, check=False)
                print(Formatter.colorText("\nAPT package cache cleaned.", Formatter.green, Formatter.bold))


            # ==> CLEAN PACMAN PACKAGE CACHE
            elif self.pactool.manager.defaultPackageManager == "pacman":
                print(Formatter.colorText("Cleaning Pacman package cache...", Formatter.yellow, Formatter.bold))
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

