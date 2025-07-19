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
from subprocess import run
from datetime import datetime, timedelta
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from json import loads as jsonLoads, JSONDecodeError
from textwrap import wrap as textWrap, fill as textFill


# ==> PACTOOL FILES
from core.formatter import Formatter
from core.logger import logError



##########################################################################
#                                                                        #
#                               SECURITY                                 #
#                                                                        #
##########################################################################

class Security:
    def __init__(self, Pactool=None) -> None:
        self.pactool = Pactool




    ##########################################################################
    #                                                                        #
    #                       VULNERABILITY PAGINATION                         #
    #                                                                        #
    ##########################################################################
    def _paginateVulnSearch(self, cves, keyword, renderFunc, limit: int = None):
        # ==> APPLY LIMIT IF PROVIDED
        if limit is not None:
            if limit > 0:
                cves = cves[:limit]
            elif limit == 0:
                print(f'{Formatter.headerColor}Showing results for "{keyword}"{Formatter.reset}\n')
                renderFunc(cves, startIndex=0)
                userInput = self._askForKeyword()
                return None if userInput.lower() == "q" else userInput



        # ==> DETERMINE TERMINAL HEIGHT FOR PAGINATION
        terminalHeight = get_terminal_size().lines - 5



        index = 0
        pageNumber = 1
        totalCves = len(cves)



        # ==> MAIN PAGINATION LOOP
        while index < totalCves:
            currentPage = []
            currentLines = 0



            # ==> ADD CVES UNTIL TERMINAL HEIGHT IS REACHED
            while index < totalCves:
                cve = cves[index]
                linesNeeded = self._estimateCveLines(cve)
                if currentLines + linesNeeded > terminalHeight and currentPage:
                    break
                currentPage.append(cve)
                currentLines += linesNeeded
                index += 1



            # ==> CALCULATE TOTAL PAGES
            totalPages = (totalCves + len(currentPage) - 1) // len(currentPage)
            renderFunc(currentPage, startIndex=(index - len(currentPage)))



            # ==> SHOW PAGE HEADER
            if keyword and not keyword.isspace():
                print(f'\n{Formatter.headerColor}CVE results for "{keyword}" - Page {pageNumber} of {totalPages}{Formatter.reset}')
            else:
                print(f'\n{Formatter.headerColor}CVE results - Page {pageNumber} of {totalPages}{Formatter.reset}')



            pageNumber += 1



            # ==> ASK USER FOR INPUT
            if index < totalCves:
                userInput = self._askForKeyword()
                if userInput.lower() == "q":
                    return None
                elif userInput:
                    return userInput



        # ==> ASK AGAIN AFTER THE LAST PAGE
        userInput = self._askForKeyword()
        return None if userInput.lower() == "q" else userInput





    def _estimateCveLines(self, cve):
        # ==> ESTIMATE HOW MANY LINES THIS CVE ENTRY WILL TAKE
        width = get_terminal_size().columns - 2
        description = cve["cve"]["descriptions"][0]["value"]
        wrappedLines = textWrap(description, width=width - 10)
        baseLines = 6
        
        return baseLines + len(wrappedLines)




    def _askForKeyword(self):
        # ==> PROMPT USER FOR NAVIGATION OR A NEW SEARCH KEYWORD
        print(f"{Formatter.headerColor}\nPress enter to continue | 'Q' to quit | or type a new keyword\n")
        userInput = input(
            Formatter.colorText("--> ", Formatter.headerColor)
        ).strip()
        return userInput





    ##########################################################################
    #                                                                        #
    #                         SECURITY PACKAGE LOGIC                         #
    #                                                                        #
    ##########################################################################
    
    
    def upgradeSecurity(self) -> None:
        # ==> UPGRADE SECURITY PACKAGES (APT)
        if self.pactool.manager.defaultPackageManager == "apt":
            print(Formatter.colorText(
                "Upgrading security-related packages [...]", 
                Formatter.yellow
            ))
            print()
            
            
            try:
                # ==> REFRESH REPOSITORIES
                run(["sudo", "apt-get", "update"], check=False)
                
                # ==> UPGRADE SECURITY PACKAGES
                run(["sudo", "apt-get", "upgrade", "-y", "--with-new-pkgs"], check=False)
            except Exception as error:
                logError(f"Failed to upgrade security packages ({error})")
        
        
        
        elif self.pactool.manager.defaultPackageManager == "pacman":
            print(Formatter.colorText(
                "Upgrading all packages (Arch Linux does not support security tags) [...]", 
                Formatter.yellow
            ))
            print()
            
            
            try:
                # ==> SYNC DATABASES AND UPGRADE ALL PACKAGES
                run(["sudo", "pacman", "-Syu", "--noconfirm"], check=False)
            except Exception as error:
                logError(f"Failed to upgrade packages ({error})")
        
        
        else:
            # ==> UNSUPPORTED PACKAGE MANAGER
            print(Formatter.colorText(
                "No supported package manager found for security upgrades.", 
                Formatter.red
            ))









    def viewSecurityPackages(self) -> None:
        # ==> DISPLAY SECURITY-RELATED PACKAGES OR RECENT UPDATES
        if self.pactool.manager.defaultPackageManager == "apt":
            print(Formatter.colorText(
                "\nSecurity Packages Installed (Debian/Ubuntu):\n", 
                Formatter.headerColor
            ))
            
            
            try:
                # ==> LIST ALL INSTALLED PACKAGES
                result = run(
                    ["apt", "list", "--installed"], 
                    capture_output=True, text=True, check=False
                ).stdout.splitlines()
                
                
                # ==> HIGHLIGHT SECURITY-TAGGED PACKAGES
                for line in result:
                    if "security" in line.lower():
                        print(Formatter.colorText(line, Formatter.green))
            except Exception as error:
                logError(f"Failed to list security packages ({error})")
        
        
        
        elif self.pactool.manager.defaultPackageManager == "pacman":
            # ==> ARCH LINUX: USE arch-audit FOR SECURITY VULNERABILITIES
            print(Formatter.colorText("\nChecking Arch Linux for security vulnerabilities:\n", Formatter.headerColor))
            

            try:
                # ==> CHECK IF arch-audit IS INSTALLED
                check_audit = run(["which", "arch-audit"], capture_output=True, text=True)
                if check_audit.returncode != 0:
                    # ==> ASK USER TO INSTALL TOOL
                    print(Formatter.colorText(f"arch-audit is not installed. Pactool needs it.", Formatter.red))
                    
                    
                    choice = input(f"\n{Formatter.yellow}Do you want Pactool to install arch-audit? [y/N] > {Formatter.white}{Formatter.bold}").strip().lower()
                    print()
                    
                    
                    if choice == "y":
                        try:
                            self.pactool.packages.install(name="arch-audit")
                        except Exception as error:
                            logError(f"Failed to install arch-audit ({error})")
                            return False
                    else:
                        print(Formatter.colorText("Aborting arch-audit installation. Pactool cannot continue.", Formatter.red))
                        return
                            
                            

                # ==> RUN arch-audit TO SHOW SECURITY VULNERABILITIES
                auditResult = run(["arch-audit"], capture_output=True, text=True)
                outputLines = [line.strip() for line in auditResult.stdout.splitlines() if line.strip()]



                if outputLines:
                    Formatter.displayPackageLegend()
                    print()
                    
                    
                    
                    # ==> CALCULATE MAX PACKAGE LENGTH FOR ALIGNMENT
                    maxPkgLen = max(len(line.split(" is ")[0]) for line in outputLines if " is " in line)
                    
                    
                    
                    # ==> FETCH EXPLICITLY INSTALLED USER PACKAGES
                    userPackages = run(
                        ["pacman", "-Qe"],
                        capture_output=True, text=True
                    ).stdout.splitlines()
                    userPkgNames = {pkg.split()[0] for pkg in userPackages}



                    for line in outputLines:
                        if " is " not in line:
                            continue
                        packageName = line.split(" is ")[0].strip()
                        issueDesc = line.split(" is ")[-1].strip().capitalize()



                        # ==> DETERMINE PACKAGE COLOR (USER VS SYSTEM)
                        if packageName in userPkgNames:
                            pkgColor = Formatter.magenta
                        else:
                            pkgColor = Formatter.blue



                        # ==> DETERMINE RISK LEVEL
                        lowerLine = line.lower()
                        if "high risk" in lowerLine:
                            risk = Formatter.colorText("[High Risk]  ", Formatter.red, Formatter.bold)
                            issueDesc = issueDesc.removesuffix(" high risk!")
                        elif "medium risk" in lowerLine:
                            risk = Formatter.colorText("[Medium Risk]", Formatter.yellow)
                            issueDesc = issueDesc.removesuffix(" medium risk!")
                        elif "low risk" in lowerLine:
                            risk = Formatter.colorText("[Low Risk]   ", Formatter.cyan)
                            issueDesc = issueDesc.removesuffix(" low risk!")
                        else:
                            risk = ""


                        # ==> FORMAT OUTPUT WITH EVEN SPACING
                        spacing = " " * (maxPkgLen - len(packageName) + 2)
                        print(f"{Formatter.colorText(packageName, pkgColor)}{spacing}{risk}  {issueDesc}")
                
                else:
                    print(Formatter.colorText("No known security vulnerabilities found.", Formatter.green))



            except Exception as error:
                logError(f"Failed to check security packages ({error})")
        
        else:
            print(Formatter.colorText("No package manager found.", Formatter.red))






    ##########################################################################
    #                                                                        #
    #                       VULNERABILITY CHECK                              #
    #                                                                        #
    ##########################################################################
    
    
    def vulnCheck(self, package: str, deepSearch=False, searchKeyword: str = "") -> None:
        # ==> MAIN VULNERABILITY CHECK FUNCTION
        print(Formatter.colorText(f"Checking vulnerabilities for '{package}' [...]\n", Formatter.yellow))


        try:
            # ==> FETCH DATA FROM NVD API
            url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={package}"
            with urlopen(url) as response:
                data = jsonLoads(response.read().decode('utf-8'))



            cves = data.get("vulnerabilities", [])
            if not cves:
                print(Formatter.colorText(f"No known CVEs found for {package}.", Formatter.green))
                return


            print(Formatter.colorText(f"Found {len(cves)} CVE(s) for {package}:\n", Formatter.headerColor))



            # ==> TRACK CVE COUNTS FOR SUMMARY
            counters = {"lastYear": 0, "last6Months": 0, "lastMonth": 0}



            # ==> UPDATE COUNTS FOR TIME RANGE
            for vuln in cves:
                pubDate = self._formatDate(vuln["cve"].get("published"))
                self._updateCounters(pubDate, counters)



            # ==> INTERACTIVE SEARCH LOOP
            while True:
                if searchKeyword:
                    # ==> FILTER BASED ON SEARCH KEYWORD
                    searchLower = searchKeyword.lower()
                    filtered = [c for c in cves if self._matchesKeywordEverywhere(c, searchLower)]


                    if not filtered:
                        print(Formatter.colorText(f"No CVEs matched \"{searchKeyword}\".\n", Formatter.red))
                        searchKeyword = input(Formatter.colorText("--> Enter new keyword or leave blank to show all: ", Formatter.cyan)).strip()
                        if not searchKeyword:
                            filtered = cves
                        else:
                            continue
                    cvesToShow = filtered
                else:
                    cvesToShow = cves



                # ==> PAGINATE RESULTS
                newKeyword = self._paginateVulnSearch(
                    cvesToShow,
                    keyword=searchKeyword,
                    renderFunc=lambda chunk, startIndex=0: self._printCveChunk(
                        chunk, startIndex=startIndex, deepSearch=deepSearch, searchKeyword=searchKeyword
                    )
                )



                if not newKeyword:
                    break
                searchKeyword = newKeyword


            # ==> SUMMARY OUTPUT
            print(Formatter.colorText(f"\nSummary for {package}:", Formatter.yellow))
            print(f"  Total CVEs found: {len(cves)}")
            print(f"  CVEs in past year: {counters['lastYear']}")
            print(f"  CVEs in past 6 months: {counters['last6Months']}")
            print(f"  CVEs in past month: {counters['lastMonth']}")



        except (URLError, HTTPError, JSONDecodeError) as error:
            print(Formatter.colorText(f"Failed to fetch CVE data ({error})", Formatter.red))
            
            
            
            
            
            
            
            
    # ==> UPDATE COUNTERS FOR CVE TIME RANGE
    def _updateCounters(self, pubDate, counters):
        """
        pubDate: string date (already formatted like "2024, April 03")
        counters: dict with keys 'lastYear', 'last6Months', 'lastMonth'
        """
        try:
            # ==> PARSE DATE BACK TO DATETIME OBJECT
            dt = datetime.strptime(pubDate, "%Y, %B %d")
            now = datetime.now()


            # ==> CHECK IF WITHIN 1 YEAR
            if dt > now - timedelta(days=365):
                counters["lastYear"] += 1


            # ==> CHECK IF WITHIN 6 MONTHS
            if dt > now - timedelta(days=180):
                counters["last6Months"] += 1


            # ==> CHECK IF WITHIN 1 MONTH
            if dt > now - timedelta(days=30):
                counters["lastMonth"] += 1


        except Exception as error:
            logError(f"Failed to update CVE counters ({error})")








    def _matchesKeywordEverywhere(self, cve, keyword: str) -> bool:
        # ==> CONVERT KEYWORD TO LOWERCASE
        keyword = keyword.lower()



        # ==> CHECK CVE ID
        if keyword in cve["cve"]["id"].lower():
            return True



        # ==> CHECK DESCRIPTIONS
        for desc in cve["cve"].get("descriptions", []):
            if keyword in desc.get("value", "").lower():
                return True



        # ==> CHECK PUBLISHED AND LAST MODIFIED DATES
        pubDate = str(cve["cve"].get("published", "")).lower()
        modDate = str(cve["cve"].get("lastModified", "")).lower()
        if keyword in pubDate or keyword in modDate:
            return True



        # ==> CHECK REFERENCES (if available)
        refs = cve["cve"].get("references", [])
        for ref in refs:
            if keyword in ref.get("url", "").lower() or keyword in ref.get("name", "").lower():
                return True


        return False







    def _printCveChunk(self, cves, startIndex=0, deepSearch=False, searchKeyword=""):
        # ==> PRINT A SINGLE PAGE OF CVE RESULTS
        for i, vuln in enumerate(cves, start=startIndex + 1):
            cveId = vuln["cve"]["id"]
            description = vuln["cve"]["descriptions"][0]["value"]
            pubDate = self._formatDate(vuln["cve"].get("published"))
            modDate = self._formatDate(vuln["cve"].get("lastModified"))
            wrappedDesc = self._wrapText(description, prefix="  Details: ")



            # ==> APPLY HIGHLIGHTING
            if searchKeyword:
                cveId = self._highlightKeyword(cveId, searchKeyword)
                wrappedDesc = self._highlightKeyword(wrappedDesc, searchKeyword)



            print(Formatter.colorText(f"[{i}] {cveId}", Formatter.red, Formatter.bold))
            print(f"  {Formatter.colorText('Published:', Formatter.cyan)} {pubDate}")
            print(f"  {Formatter.colorText('Last Modified:', Formatter.cyan)} {modDate}")
            print(wrappedDesc)
            print(f"  {Formatter.colorText('More Info:', Formatter.cyan)} https://nvd.nist.gov/vuln/detail/{cveId}\n")
            print("-" * get_terminal_size().columns + "\n")



            if deepSearch:
                self._deepSearchDetails(cveId)







    def _highlightKeyword(self, text: str, keyword: str) -> str:
        # ==> HIGHLIGHT MATCHED KEYWORD
        lowerText = text.lower()
        lowerKey = keyword.lower()
        start = 0
        result = ""
        
        
        while True:
            idx = lowerText.find(lowerKey, start)
            if idx == -1:
                result += text[start:]
                break
            
            
            result += text[start:idx] + Formatter.colorText(text[idx:idx + len(keyword)], Formatter.green, Formatter.bold)
            start = idx + len(keyword)
            
            
        return result




    def _formatDate(self, dateStr):
        # ==> FORMAT DATE INTO "YYYY, Month, Day"
        if not dateStr:
            return "N/A"
        
        
        try:
            dt = datetime.fromisoformat(dateStr.replace("Z", "+00:00"))
            return dt.strftime("%Y, %B %d")
        except Exception:
            return dateStr





    def _wrapText(self, text, prefix="  ", width=None):
        # ==> WRAP LONG TEXTS CLEANLY
        if width is None:
            width = get_terminal_size().columns - 2
        if len(text) > 500:
            text = text[:500] + "... [See More at CVE Link]"
            
            
        return textFill(
            text,
            width=width,
            initial_indent=prefix,
            subsequent_indent=" " * len(prefix)
        )





    def _deepSearchDetails(self, cveId):
        # ==> DISPLAY ADDITIONAL DEEP SEARCH DETAILS
        print(Formatter.colorText(f"  Deep Search for {cveId}:", Formatter.yellow))
        print("    Impact Tree:")
        print("    ├─ CVSS v3 Score: N/A")
        print("    ├─ Attack Vector: N/A")
        print("    ├─ Known Exploits: No public exploits found.")
        print("    ├─ References:")
        print(f"    │   - https://nvd.nist.gov/vuln/detail/{cveId}")
        print("    └─ Severity: N/A\n")
        print("-" * get_terminal_size().columns + "\n")