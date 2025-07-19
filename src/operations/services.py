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

from subprocess import run, PIPE


# ==> PACTOOL FILES
from core.logger import logError
from core.formatter import Formatter




##########################################################################
#                                                                        #
#                               SERVICES                                 #
#                                                                        #
##########################################################################

class Services:
    def __init__(self, Pactool=None) -> None:
        self.pactool = Pactool
        
        
        
        
    def showServices(self) -> None:
        try:
            # ==> DETECT SERVICE MANAGER
            hasSystemd = run(["which", "systemctl"], capture_output=True, text=True).returncode == 0
            hasService = run(["which", "service"], capture_output=True, text=True).returncode == 0


            if not hasSystemd and not hasService:
                print(Formatter.colorText("No supported service manager found (systemctl/service).", Formatter.red))
                return


            print(Formatter.colorText("\nSystem Services Status:\n", Formatter.headerColor, Formatter.bold))


            services = []
            if hasSystemd:
                # ==> GET ALL SYSTEMD SERVICES
                result = run(["systemctl", "list-unit-files", "--type=service", "--no-pager"],
                            capture_output=True, text=True)
                lines = [line for line in result.stdout.splitlines() if ".service" in line and not line.startswith("UNIT FILE")]


                for line in lines:
                    parts = line.split()
                    if len(parts) >= 2:
                        services.append((parts[0], parts[1].capitalize()))
                        
                        
                        
            elif hasService:
                # ==> GET ALL SYSVINIT SERVICES
                from os import listdir
                for script in listdir("/etc/init.d/"):
                    services.append((script, "UNKNOWN"))



            # ==> CALCULATE FIXED WIDTH FOR COLUMNS
            maxNameWidth = max(len(s[0]) for s in services)
            maxStatusWidth = max(len(s[1]) for s in services)



            # ==> DISPLAY ALL SERVICES WITH COLOR-CODED STATUS
            for name, status in services:
                color = self._getServiceStatusColor(status.lower())
                print(f"  {Formatter.colorText(name.ljust(maxNameWidth), Formatter.cyan)}  {Formatter.colorText(status.ljust(maxStatusWidth), color)}")


        except Exception as error:
            logError(f"Failed to list services ({error})")





    def _getServiceStatusColor(self, status: str) -> str:
        # ==> COLOR CODE BASED ON STATUS
        if status == "enabled":
            return Formatter.green
        elif status == "disabled":
            return Formatter.red
        elif status in ("static", "alias"):
            return Formatter.cyan
        elif status in ("generated", "enabled-runtime"):
            return Formatter.magenta
        elif status == "indirect":
            return Formatter.yellow
        return Formatter.white







    # ==> SHOW DETAILED SERVICE INFO
    def info(self, serviceName: str) -> None:
        try:
            print(
                f"\n{Formatter.colorText('Service Information -> ', Formatter.headerColor, Formatter.bold)}"
                f"{Formatter.colorText(serviceName, Formatter.white, Formatter.bold)}\n"
            )


            result = run(["systemctl", "status", serviceName], stdout=PIPE, stderr=PIPE, text=True)
            if result.returncode != 0:
                print(Formatter.colorText(f"Service '{serviceName}' not found.", Formatter.red))
                return



            for line in result.stdout.splitlines():
                # ==> HIGHLIGHT KEY PARTS
                if "Active:" in line:
                    print(Formatter.colorText(line, Formatter.green))
                elif "Loaded:" in line:
                    print(Formatter.colorText(line, Formatter.cyan))
                elif "Main PID:" in line:
                    print(Formatter.colorText(line, Formatter.magenta))
                else:
                    print(line)
                    
            print()



        except Exception as error:
            logError(f"Failed to show service info ({error})")








    def logs(self, serviceName: str, lines: int = 20) -> None:
        try:
            print(
                f"\n{Formatter.colorText(f'Last {lines} log entries for -> ', Formatter.headerColor, Formatter.bold)}"
                f"{Formatter.colorText(serviceName, Formatter.white, Formatter.bold)}\n"
            )



            result = run(["journalctl", "-u", serviceName, "-n", str(lines), "--no-pager"], stdout=PIPE, stderr=PIPE, text=True)
            if result.returncode != 0 or not result.stdout.strip():
                print(Formatter.colorText(f"No logs found for '{serviceName}'.", Formatter.red))
                return



            for line in result.stdout.splitlines():
                if "error" in line.lower():
                    print(Formatter.colorText(line, Formatter.red))
                elif "warning" in line.lower():
                    print(Formatter.colorText(line, Formatter.yellow))
                else:
                    print(line)
                    
                    
            print()



        except Exception as error:
            logError(f"Failed to fetch service logs ({error})")