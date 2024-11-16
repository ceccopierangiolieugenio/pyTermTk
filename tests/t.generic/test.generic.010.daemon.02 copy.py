#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os,sys
import time

def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    """
    Double fork-trick. For starting a posix daemon.

    This forks the current process into a daemon. The stdin, stdout, and stderr
    arguments are file names that will be opened and be used to replace the
    standard file descriptors in sys.stdin, sys.stdout, and sys.stderr. These
    arguments are optional and default to /dev/null. Note that stderr is opened
    unbuffered, so if it shares a file with stdout then interleaved output may
    not appear in the order that you expect.

    Thanks to:
    http://code.activestate.com/recipes/66012-fork-a-daemon-process-on-unix/
    """
    # Do first fork.
    try:
        pid = os.fork()
        if pid > 0:
            os.waitpid(pid, 0)
            return 0  # Return 0 from first parent.
    except OSError as e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # Decouple from parent environment.
    os.chdir("/")
    os.umask(0)
    os.setsid()

    # Do second fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit second parent.
    except OSError as e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # Now I am a daemon!

    # Redirect standard file descriptors.

        # NOTE: For debugging, you meight want to take these instead of /dev/null.
    # so = open('/tmp/log2', 'ab+')
    # se = open('/tmp/log2', 'ab+', 0)

    # si = open(stdin, 'rb')
    # so = open(stdout, 'ab+')
    # se = open(stderr, 'ab+', 0)
    # os.dup2(si.fileno(), sys.stdin.fileno())
    # os.dup2(so.fileno(), sys.stdout.fileno())
    # os.dup2(se.fileno(), sys.stderr.fileno())

    # Return 1 from daemon.
    return 1

if daemonize(stdout=sys.stdout):
    for i in range(100):
        print(f"{i=}",flush=True)
        time.sleep(0.1)

time.sleep(3)

print(f"Main Process exit...")



