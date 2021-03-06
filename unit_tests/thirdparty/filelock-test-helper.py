#
# Copyright (c) 2013-2014, PagerDuty, Inc. <info@pagerduty.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the copyright holder nor the
#     names of its contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

import os
import signal
import sys
import time

from pdagent.thirdparty.filelock import FileLock, LockTimeoutException
from unit_tests.thirdparty.test_filelock import TEST_LOCK_FILE

lock = FileLock(TEST_LOCK_FILE, timeout=1)


def test_spawn_ok():
    return 10

def test_simple_lock():
    lock.acquire()
    time.sleep(1)
    lock.release()
    return 20

def test_lock_wait():
    lock.acquire()
    time.sleep(2)
    lock.release()
    return 25

def test_lock_timeout():
    try:
        lock.acquire()
    except LockTimeoutException:
        return 30
    return 31

def test_lock_timeout_other_way_around():
    lock.acquire()
    time.sleep(3)  # assumes the main test is using a timeout of 1 seconds
    lock.release()
    return 35

def test_exit_without_release():
    lock.acquire()
    return 40

def test_kill_releases_lock():
    lock.acquire()
    os.kill(os.getpid(), signal.SIGKILL)
    return 50


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2: sys.exit(2)  # wrong number of args

    _test_func_name = args[1]
    if not _test_func_name.startswith("test_"): sys.exit(5)  # bad test name

    main_module = sys.modules["__main__"]
    _test_func = getattr(main_module, _test_func_name, None)
    if not _test_func: sys.exit(6)  # no such test

    exit_code = _test_func()
    if exit_code is None: sys.exit(7)  # missing exit code
    if exit_code != 0 and exit_code < 10: sys.exit(8)  # reserved exit code
    sys.exit(exit_code)


