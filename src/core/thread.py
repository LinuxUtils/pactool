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

from threading import Thread, Event
from traceback import print_exc as tracebackPrintExec
from sys import stdout as sysStdout



##########################################################################
#                                                                        #
#                                THREAD                                  #
#                                                                        #
##########################################################################


class SafeThread(Thread):
    """
    A daemon thread that stores any exception and can be stopped
    gracefully with .stop().
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daemon = True
        self.exception = None
        self._stop_evt = Event()
        
        
        
        
    def stop(self) -> None:
        """Request the thread to stop."""
        self._stop_evt.set()
        
        
        
        
        
    def stopped(self) -> bool:
        """True if a stop request has been issued."""
        return self._stop_evt.is_set()
        




    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        
        
        except KeyboardInterrupt:
            sysStdout.write("\n")
            sysStdout.flush
                
                
        except BaseException as error:
            self.exception = error
            tracebackPrintExec()