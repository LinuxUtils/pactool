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

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from sys import exit as sysExit


# ==> PACTOOL FILES
from core.logger import logSuccess, logError
from core.formatter import Formatter
from core.manager import Manager
from operations.packages import Packages
from operations.services import Services
from operations.mirrors import Mirrors



##########################################################################
#                                                                        #
#                                 MAIN                                   #
#                                                                        #
##########################################################################


class Main:
    def __init__(self) -> None:
        # ==> GENERAL INFO
        self.description = "A cross-distro package management helper for Linux systems."
        self.release = "1.0.0"
        self.releaseDate = "18/7/2025"


        # ==> CREATE OBJECTS
        self.manager = Manager()
        self.packages = Packages(Pactool=self)
        self.services = Services(Pactool=self)
        self.mirrors = Mirrors(Pactool=self)




    def ping(self) -> None:
        print(f"Pong (Pactool {self.release})")




    def baseMessage(self) -> None:
        print(f"Pactool {self.release}")





    def info(self) -> None:
        print(f"Pactool {self.release}")
        
        # ==> AUTHOR INFO
        print(f"{Formatter.tab4}Author:")
        print(f"{Formatter.tab8}g7gg <www.github.com/g7gg>")
        print()

        # ==> RELEASE INFO
        print(f"{Formatter.tab4}Version:")
        print(f"{Formatter.tab8}Release {self.release}")
        print(f"{Formatter.tab8}Released on {self.releaseDate}")





    def quit(self, code: int = 0) -> None:
        sysExit(code)





    def createParser(self) -> ArgumentParser:
        parser = ArgumentParser(
            prog="pactool.py",
            description=(
                "Pactool 1.0.0 - A cross-distro package management helper for Linux systems.\n\n"
                "\nExamples:\n"
                "  python3 pactool.py --list\n"
                "  python3 pactool.py --search firefox\n"
                "  python3 pactool.py --install vlc --user\n"
            ),
            formatter_class=RawTextHelpFormatter
        )


        ##########################################################################
        #                                GENERAL                                 #
        ##########################################################################
        general = parser.add_argument_group("General Commands")
        general.add_argument("--version", action="store_true", help="Show Pactool version and exit")
        general.add_argument("--ping", action="store_true", help="Check if Pactool is working (returns Pong)")
        general.add_argument("--about", action="store_true", help="Display detailed information about Pactool")



        ##########################################################################
        #                                 Packages                               #
        ##########################################################################
        pkg = parser.add_argument_group("Package Commands")
        pkg.add_argument("--list", action="store_true", help="List installed packages (paged by default)")
        pkg.add_argument("-n", type=int, metavar="N", help="Number of packages to show (0 = all)")
        pkg.add_argument("--stats", action="store_true", help="Show statistics about packages")
        pkg.add_argument("--files", metavar="PACKAGE", help="List all files installed by a package")
        pkg.add_argument("--search", metavar="SEARCH", help="Search for a package by name")
        pkg.add_argument("--why", metavar="PACKAGE", help="Show which packages depend on this package (reverse dependencies)")
        pkg.add_argument("--uninstall", metavar="PACKAGE", help="Uninstall a package by name")
        pkg.add_argument("--install", metavar="PACKAGE", help="Install a package by name")
        pkg.add_argument("--update", action="store_true", help="Update all installed packages")
        pkg.add_argument("--upgrade", action="store_true", help="Upgrade all installed packages")
        pkg.add_argument("--clean", action="store_true", help="Clean cached or unused package files")
        sortChoices = "name/size/install-date/update-date/type"
        pkg.add_argument("--sort", metavar="CRITERIA", help=f"{sortChoices}")
        pkg.add_argument("--rsort", metavar="CRITERIA", help=f"{sortChoices}")
        pkg.add_argument("--user", action="store_true", help="Show only user-installed packages")
        pkg.add_argument("--system", action="store_true", help="Show only system packages")
        pkg.add_argument("--info", metavar="PACKAGE", help="Show detailed information about a specific package")
        pkg.add_argument("--bloat", action="store_true", help="Find unused optional dependencies (bloat)")
        pkg.add_argument("--unused", action="store_true", help="Find unused or orphaned packages")

                
                
        ##########################################################################
        #                                 Services                               #
        ##########################################################################
        services = parser.add_argument_group("Service Commands")
        services.add_argument("--services", action="store_true", help="Show the status of system services related to installed packages")
        services.add_argument("--service-info", metavar="SERVICE", help="Show detailed information about a service")
        services.add_argument("--service-logs", metavar="SERVICE", help="Show the logs of a service")

        
        ##########################################################################
        #                                  Mirrors                               #
        ##########################################################################
        mirrors = parser.add_argument_group("Mirror Commands")
        mirrors.add_argument("--show-mirrors", action="store_true", help="Show the current mirrors with ping and last update")
        mirrors.add_argument("--update-mirrors", action="store_true", help="Update to the fastest mirrors")
        mirrors.add_argument("--revert-mirrors", action="store_true", help="Revert mirrors to a previous backup")
        mirrors.add_argument("--backup-mirrors", action="store_true", help="Create a manual backup of the current mirror list")
        

        return parser







    def run(self) -> None:
        parser = self.createParser()

        try:
            args: Namespace = parser.parse_args()

            
            # ==> GET SORTING OPTIONS (IF ANY)
            sortOption = args.sort or args.rsort
            reverseSort = bool(args.rsort)


            if args.ping:
                self.ping()
            elif args.about:
                self.info()


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
