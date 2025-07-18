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


from argparse import ArgumentParser
from sys import exit
from paktool.logger import logSuccess, logError




##########################################################################
#                                                                        #
#                               FUNCTIONS                                #
#                                                                        #
##########################################################################


def handleBase():
    """
    Displays a base message for PakTool.
    Currently a placeholder for future features.
    """
    message = "PakTool Base: No features implemented yet."
    print(message)
    logSuccess(message)





def createParser():
    """
    Creates and returns the base argument parser for PakTool.
    """
    parser = ArgumentParser(description="PakTool - Package Management Helper (Base Version)")
    parser.add_argument("--version", action="version", version="PakTool 0.1.0")
    return parser




def main():
    """
    Entry point of PakTool.
    Parses arguments, logs startup, and calls the base handler.
    """
    parser = createParser()

    try:
        logSuccess("PakTool started.")
        args = parser.parse_args()
        handleBase()
        logSuccess("PakTool finished successfully.")

    except BaseException as error:
        logError(f"Unhandled exception when logging to cache ({error})")
        exit(1)




##########################################################################
#                                                                        #
#                                  MAIN                                  #
#                                                                        #
##########################################################################


if __name__ == "__main__":
    main()
