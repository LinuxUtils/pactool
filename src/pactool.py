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

from argparse import ArgumentParser, Namespace
from sys import exit as sysExit


# ==> PACTOOL FILES
from core.logger import logSuccess, logError
from core.formatter import Formatter
from operations.packages import Packages



##########################################################################
#                                                                        #
#                                 MAIN                                   #
#                                                                        #
##########################################################################


class Pactool:
    def __init__(self) -> None:
        # ==> GENERAL INFO
        self.description = "A cross-distro package management helper for Linux systems."
        self.release = "1.0.0"
        self.releaseDate = "18/7/2025"


        # ==> CREATE OBJECTS
        self.packages = Packages()




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
        parser = ArgumentParser(description=f"Pactool {self.release} - {self.description}")


        ##########################################################################
        #                                GENERAL                                 #
        ##########################################################################
        generalGroup = parser.add_argument_group("General Commands")
        generalGroup.add_argument("--version", action="version", version=f"Pactool {self.release}")
        generalGroup.add_argument("--ping", action="store_true", help="Checks if Pactool is working (returns Pong)")
        generalGroup.add_argument("--info", action="store_true", help="Displays information about Pactool")



        ##########################################################################
        #                                self.packages.                               #
        ##########################################################################
        packageGroup = parser.add_argument_group("Package Commands")
        packageGroup.add_argument(
            "--list", action="store_true", help="Lists installed packages (paged by default)"
        )
        packageGroup.add_argument(
            "-n", type=int, default=None,
            help="Number of packages to show (use 0 for all)"
        )
        packageGroup.add_argument("--stats", action="store_true", help="Shows package statistics")
        packageGroup.add_argument("--search", type=str, help="Search for a package by name")
        packageGroup.add_argument("--uninstall", type=str, help="Uninstall a package by name")
        packageGroup.add_argument("--install", type=str, help="Install a package by name")
        packageGroup.add_argument("--update", action="store_true", help="Updates all installed packages")
        packageGroup.add_argument("--upgrade", action="store_true", help="Upgrades all installed packages")


        return parser







    def run(self) -> None:
        parser = self.createParser()

        try:
            args: Namespace = parser.parse_args()

            if args.ping:
                self.ping()
            elif args.info:
                self.info()

            # ==> PACKAGE COMMANDS
            elif args.list:
                self.packages.list(args.n)
            elif args.stats:
                self.packages.stats(args.n)
            elif args.search:
                self.packages.search(args.search, args.n)
            elif args.uninstall:
                self.packages.uninstall(args.uninstall)
            elif args.install:
                self.packages.install(args.install)
            elif args.update:
                self.packages.update()
            elif args.upgrade:
                self.packages.upgrade()
            else:
                self.baseMessage()

            self.quit(code=0)


        except BaseException as error:
            errorName = type(error).__name__
            
            # ==> IGNORE CLEAN EXITS
            if errorName == "SystemExit":
                if getattr(error, "code", 1) == 0:
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
    Pactool().run()
