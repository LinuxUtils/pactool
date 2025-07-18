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

from datetime import datetime
from pathlib import Path
from logging import basicConfig, info, error, INFO


# ==> CREATE LOG DIRECTORY
logDir = Path.home() / ".cache" / "paktool" / "logs"
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
    Logs a success message to today's PakTool log file.
    """
    info(message)


def logError(message: str):
    """
    Logs an error message to today's PakTool log file.
    """
    error(message)
