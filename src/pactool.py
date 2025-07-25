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

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from sys import exit as sysExit, argv as sysArgv


# ==> PACTOOL FILES
from core.logger import logSuccess, logError
from core.formatter import Formatter
from core.manager import Manager
from operations.packages import Packages
from operations.services import Services
from operations.mirrors import Mirrors
from operations.kernels import Kernels
from operations.security import Security



##########################################################################
#                                                                        #
#                                VERSION                                 #
#                                                                        #
##########################################################################
class Version:
    description = "A cross-distro package management helper for Linux systems."
    release = "1.0.4"
    releaseDate = "23/7/2025"








##########################################################################
#                                                                        #
#                            ARGUMENT PARSER                             #
#                                                                        #
##########################################################################


class PactoolArgumentParser(ArgumentParser):
    def showLogo(self):
        # ==> DEFINE START AND END COLORS
        startColor = (255, 255, 25)
        endColor = (255, 150, 40)


        # ==> DEFINE LOGO
        logoLines = [
            "            +++++++++++++++++     ",
            "         +++++++++++++++++++++++  ",
            "       +++++++++++++++++++++++++++",
            "      ++++++++++++++++++++++++++  ",
            "     +++++++++++++++++++++++ P    ",
            "    ++++++++++++++++++++++ A      ",
            "    ++++++++++++++++++++ C        ",
           f"    +++++++++++++++++       {Version.release}",
            "    ++++++++++++++++++++ T        ",
            "    ++++++++++++++++++++++ O      ",
            "     +++++++++++++++++++++++ L    ",
            "      ++++++++++++++++++++++++++  ",
            "       +++++++++++++++++++++++++++",
            "         +++++++++++++++++++++++  ",
            "            +++++++++++++++++     "
        ]



        # ==> INTERPOLATE BETWEEN TWO COLORS
        def interpolateColor(start, end, factor):
            return tuple(
                int(start[i] + (end[i] - start[i]) * factor) for i in range(3)
            )



        for i, line in enumerate(logoLines):
            factor = i / (len(logoLines) - 1)
            r, g, b = interpolateColor(startColor, endColor, factor)
            colorCode = f"\033[38;2;{r};{g};{b}m"
            print(f"{colorCode}{line}\033[0m")





    def format_help(self):
        self.showLogo()
        helpText = (
            f"{Formatter.bold}{Formatter.yellow}USAGE:{Formatter.reset}\n"
            "  python3 pactool.py [OPTIONS]\n"
            f"\n{Formatter.bold}{Formatter.yellow}GENERAL COMMANDS:{Formatter.reset}\n"
            "  --version                   Show Pactool version and exit\n"
            "  --about                     Display detailed information about Pactool\n"
            f"\n{Formatter.bold}{Formatter.yellow}PACKAGE COMMANDS:{Formatter.reset}\n"
            "  --list                      List installed packages (paged by default)\n"
            "  -n N                        Number of packages to show (0 = all)\n"
            "  --stats                     Show statistics about packages\n"
            "  --files PACKAGE             List all files installed by a package\n"
            "  --search SEARCH             Search for a package by name\n"
            "  --why PACKAGE               Show reverse dependencies of a package\n"
            "  --uninstall PACKAGE         Uninstall a package by name\n"
            "  --install PACKAGE           Install a package by name\n"
            "  --update                    Update all installed packages\n"
            "  --upgrade                   Upgrade all installed packages\n"
            "  --clean                     Clean cached or unused package files\n"
            "  --sort CRITERIA             name/size/install-date/update-date/type\n"
            "  --rsort CRITERIA            Reverse sort by the same criteria\n"
            "  --user                      Show only user-installed packages\n"
            "  --system                    Show only system packages\n"
            "  --info PACKAGE              Show detailed information about a package\n"
            "  --bloat                     Find unused optional dependencies (bloat)\n"
            "  --unused                    Find unused or orphaned packages\n"
            "  --outdated                  List all outdated packages\n"
            "  --history PACKAGE           Show version history and updates of a package\n"
            "  --versions PACKAGE          Show all available versions of a package with risk levels\n"
            f"\n{Formatter.bold}{Formatter.yellow}SERVICE COMMANDS:{Formatter.reset}\n"
            "  --services                  Show status of services related to packages\n"
            "  --service-info SERVICE      Show detailed info about a service\n"
            "  --service-logs SERVICE      Show logs of a service\n"
            f"\n{Formatter.bold}{Formatter.yellow}MIRROR COMMANDS:{Formatter.reset}\n"
            "  --show-mirrors              Show current mirrors with ping & last update\n"
            "  --update-mirrors            Update to fastest mirrors\n"
            "  --revert-mirrors            Revert mirrors to previous backup\n"
            "  --backup-mirrors            Create a manual backup of the current mirror list\n"
            f"\n{Formatter.bold}{Formatter.yellow}KERNEL COMMANDS:{Formatter.reset}\n"
            "  --cleanup-kernels           Automatically remove old kernels\n"
            "  --backup-kernel             Backup the current running kernel to /boot/pactool/backup\n"
            f"\n{Formatter.bold}{Formatter.yellow}SECURITY COMMANDS:{Formatter.reset}\n"
            "  --upgrade-security          Upgrade only security-related packages (Debian/Ubuntu)\n"
            "  --vuln-check PACKAGE        Check known CVEs (vulnerabilities) for a package\n"
            "  --deep-search               Use with --vuln-check for detailed exploit tree and history\n"
            "  --view-security-packages    View all installed security packages with details\n"
        )

        return helpText

    
    
    
    def error(self, message):
        # ==> CUSTOM ERROR MESSAGE
        self.print_help()
        print(f"\n{Formatter.red}{message.capitalize()}{Formatter.reset}")
        sysExit(2)
        
        
        
        
    def parse_args(self, args=None, namespace=None):
        # ==> SHOW HELP IF NO ARGS ARE PROVIDED
        if len(sysArgv) == 1:
            self.print_help()
            sysExit(0)
        return super().parse_args(args, namespace)



##########################################################################
#                                                                        #
#                                 MAIN                                   #
#                                                                        #
##########################################################################


class Main:
    def __init__(self) -> None:
        # ==> GENERAL INFO
        self.description = Version.description
        self.release = Version.release
        self.releaseDate = Version.releaseDate


        # ==> CREATE OBJECTS
        self.manager = Manager()
        self.packages = Packages(Pactool=self)
        self.services = Services(Pactool=self)
        self.mirrors = Mirrors(Pactool=self)
        self.kernels = Kernels(Pactool=self)
        self.security = Security(Pactool=self)
        
        


    def baseMessage(self) -> None:
        print(f"{Formatter.headerColor}{self.release}{Formatter.reset}")





    def about(self) -> None:
        # ==> HEADER
        print(f"{Formatter.headerColor}Pactool {self.release} {Formatter.reset}")
        
        # ==> SHORT DESCRIPTION
        print(f"{Formatter.tab4}{Formatter.bold}{Formatter.brightWhite}What is Pactool?{Formatter.reset}")
        print(f"{Formatter.tab8}Pactool is a powerful, cross-distro package management helper for")
        print(f"{Formatter.tab8}Arch Linux, Manjaro, Debian, Ubuntu, and derivatives. It simplifies")
        print(f"{Formatter.tab8}package management by providing clear, color-coded, and modern output.")
        print()

        # ==> KEY FEATURES
        print(f"{Formatter.tab4}{Formatter.bold}{Formatter.brightWhite}Key Features:{Formatter.reset}")
        print(f"{Formatter.tab8}- Advanced package listing with pagination and sorting.")
        print(f"{Formatter.tab8}- Search, install, uninstall, update, and upgrade packages.")
        print(f"{Formatter.tab8}- Mirror management: show, update, backup, and revert mirrors.")
        print(f"{Formatter.tab8}- Kernel utilities: cleanup old kernels and backup current kernel.")
        print(f"{Formatter.tab8}- Vulnerability checks (CVEs) and security package overview.")
        print()

        # ==> BASIC USAGE
        print(f"{Formatter.tab4}{Formatter.bold}{Formatter.brightWhite}Basic Usage:{Formatter.reset}")
        print(f"{Formatter.tab8}python3 pactool.py --list")
        print(f"{Formatter.tab8}python3 pactool.py --search firefox")
        print(f"{Formatter.tab8}python3 pactool.py --upgrade")
        print()

        # ==> AUTHOR INFO
        print(f"{Formatter.tab4}{Formatter.bold}{Formatter.brightWhite}Author:{Formatter.reset}")
        print(f"{Formatter.tab8}g7gg <www.github.com/g7gg>")
        print()

        # ==> RELEASE INFO
        print(f"{Formatter.tab4}{Formatter.bold}{Formatter.brightWhite}Version:{Formatter.reset}")
        print(f"{Formatter.tab8}Release {self.release}")
        print(f"{Formatter.tab8}Released on {self.releaseDate}{Formatter.reset}")





    def quit(self, code: int = 0) -> None:
        sysExit(code)






    def createParser(self) -> ArgumentParser:
        parser = PactoolArgumentParser(formatter_class=RawTextHelpFormatter)


        ##########################################################################
        #                                GENERAL                                 #
        ##########################################################################
        parser.add_argument("--version", action="store_true", help="Show Pactool version and exit")
        parser.add_argument("--about", action="store_true", help="Display detailed information about Pactool")


        ##########################################################################
        #                                 PACKAGES                               #
        ##########################################################################
        parser.add_argument("--list", action="store_true", help="List installed packages (paged by default)")
        parser.add_argument("-n", type=int, metavar="N", help="Number of packages to show (0 = all)")
        parser.add_argument("--stats", action="store_true", help="Show statistics about packages")
        parser.add_argument("--files", metavar="PACKAGE", help="List all files installed by a package")
        parser.add_argument("--search", metavar="SEARCH", help="Search for a package by name")
        parser.add_argument("--why", metavar="PACKAGE", help="Show reverse dependencies of a package")
        parser.add_argument("--uninstall", metavar="PACKAGE", help="Uninstall a package by name")
        parser.add_argument("--install", metavar="PACKAGE", help="Install a package by name")
        parser.add_argument("--update", action="store_true", help="Update all installed packages")
        parser.add_argument("--upgrade", action="store_true", help="Upgrade all installed packages")
        parser.add_argument("--clean", action="store_true", help="Clean cached or unused package files")
        parser.add_argument("--sort", metavar="CRITERIA", help="name/size/install-date/update-date/type")
        parser.add_argument("--rsort", metavar="CRITERIA", help="Reverse sort by criteria")
        parser.add_argument("--user", action="store_true", help="Show only user-installed packages")
        parser.add_argument("--system", action="store_true", help="Show only system packages")
        parser.add_argument("--info", metavar="PACKAGE", help="Show detailed information about a package")
        parser.add_argument("--bloat", action="store_true", help="Find unused optional dependencies (bloat)")
        parser.add_argument("--unused", action="store_true", help="Find unused or orphaned packages")
        parser.add_argument("--outdated", action="store_true", help="List all outdated packages")
        parser.add_argument("--history", metavar="PACKAGE", help="Show version history and updates of a package")
        parser.add_argument("--versions", metavar="PACKAGE", help="Show all available versions of a package with risk levels")
        parser.add_argument("--assess-risk", action="store_true", help="Assess risk level for package versions (Only used with --versions)")
        

        ##########################################################################
        #                                 SERVICES                               #
        ##########################################################################
        parser.add_argument("--services", action="store_true", help="Show status of services related to packages")
        parser.add_argument("--service-info", metavar="SERVICE", help="Show detailed info about a service")
        parser.add_argument("--service-logs", metavar="SERVICE", help="Show logs of a service")


        ##########################################################################
        #                                  MIRRORS                               #
        ##########################################################################
        parser.add_argument("--show-mirrors", action="store_true", help="Show current mirrors with ping & last update")
        parser.add_argument("--update-mirrors", action="store_true", help="Update to fastest mirrors")
        parser.add_argument("--revert-mirrors", action="store_true", help="Revert mirrors to previous backup")
        parser.add_argument("--backup-mirrors", action="store_true", help="Create a manual backup of the current mirror list")


        ##########################################################################
        #                              KERNEL COMMANDS                           #
        ##########################################################################
        parser.add_argument("--cleanup-kernels", action="store_true", help="Automatically remove old kernels")
        parser.add_argument("--backup-kernel", action="store_true", help="Backup the current running kernel to /boot/pactool/backup")


        ##########################################################################
        #                              SECURITY COMMANDS                         #
        ##########################################################################
        security = parser.add_argument_group("Security Commands")
        security.add_argument(
            "--upgrade-security",
            action="store_true",
            help="Upgrade only security-related packages (Debian/Ubuntu only)"
        )
        security.add_argument(
            "--view-security-packages",
            action="store_true",
            help="View all installed security packages with install/update dates and size"
        )
        security.add_argument(
            "--vuln-check",
            metavar="PACKAGE",
            help="Check known CVEs (vulnerabilities) for a package"
        )
        security.add_argument(
            "--deep-search",
            action="store_true",
            help="Perform a deeper vulnerability analysis when used with --vuln-check"
        )

        return parser







    def run(self) -> None:
        parser = self.createParser()

        try:
            args: Namespace = parser.parse_args()

            
            # ==> GET SORTING OPTIONS (IF ANY)
            sortOption = args.sort or args.rsort
            reverseSort = bool(args.rsort)


            if args.about:
                self.about()


            # ==> PACKAGE COMMANDS
            elif args.list:
                self.packages.list(args.n, sortOption, args.user, args.system, reverseSort)
            elif args.stats:
                self.packages.stats(args.n)
            elif args.files:
                self.packages.listFiles(args.files)
            elif args.search:
                self.packages.search(args.search, args.n)
            elif args.why:
                self.packages.why(args.why)
            elif args.uninstall:
                self.packages.uninstall(args.uninstall)
            elif args.install:
                self.packages.install(args.install)
            elif args.update:
                self.packages.update()
            elif args.upgrade:
                self.packages.upgrade()
            elif args.clean:
                self.packages.clean()
            elif args.info:
                self.packages.info(args.info)   
            elif args.bloat:
                self.packages.bloat(args.n)
            elif args.unused:
                self.packages.unused(args.n)
            elif args.outdated:
                self.packages.outdated(args.n)
            elif args.history:
                self.packages.history(args.history)
            elif args.versions:
                self.packages.versions(args.versions, assessRisk=args.assess_risk)


 
                
            # ==> SERVICE COMMANDS
            elif args.services:
                self.services.showServices()
            elif args.service_info:
                self.services.info(args.service_info)
            elif args.service_logs:
                self.services.logs(args.service_logs)

            
            
            # ==> MIRROR COMMANDS
            elif args.show_mirrors:
                self.mirrors.showMirrors()
            elif args.update_mirrors:
                self.mirrors.updateFastestMirrors()
            elif args.revert_mirrors:
                self.mirrors.revertMirrors()
            elif args.backup_mirrors:
                self.mirrors.createManualBackup()
                
                
            # ==> KERNEL COMMANDS
            elif args.cleanup_kernels:
                self.kernels.cleanupKernels()
            elif args.backup_kernel:
                self.kernels.backupKernel()
                
                
            # ==> SECURITY COMMANDS
            elif args.upgrade_security:
                self.security.upgradeSecurity()
            elif args.vuln_check:
                self.security.vulnCheck(args.vuln_check, deepSearch=args.deep_search)
            elif args.view_security_packages:
                self.security.viewSecurityPackages()
                
                
            else:
                self.baseMessage()


            self.quit(code=0)




        except BaseException as error:
            errorName = type(error).__name__
            
            # ==> IGNORE CLEAN EXITS
            if errorName == "SystemExit":
                if getattr(error, "code", 1) in (0, 2):
                    self.quit(0)
                else:
                    logError(f"\nUnhandled SystemExit in main execution ({error})")
                    self.quit(error.code if isinstance(error.code, int) else 1)


            # ==> IGNORE CTRL+C
            elif errorName == "KeyboardInterrupt":
                self.quit(0)


            # ==> HANDLE ALL OTHER ERRORS
            else:
                logError(f"\nUnhandled exception in main execution ({error})")
                self.quit(1)





##########################################################################
#                                                                        #
#                                  MAIN                                  #
#                                                                        #
##########################################################################



if __name__ == "__main__":
    Main().run()
