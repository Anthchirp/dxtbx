#!/usr/bin/env python
# TestRegistry.py
#   Copyright (C) 2011 Diamond Light Source, Graeme Winter
#
#   This code is distributed under the BSD license, a copy of which is
#   included in the root directory of this package.
#
# Code to give the registry a bit of a workout.

from __future__ import print_function
import os
import sys

assert "XIA2_ROOT" in os.environ

if not os.environ["XIA2_ROOT"] in sys.path:
    sys.path.append(os.environ["XIA2_ROOT"])

from dxtbx.format.Registry import Registry

import time


def TestRegistry(files):
    """Print the class which claims to work with each file."""

    s = time.time()

    for f in files:

        print(f)

        format = Registry.find(f)

        print(format.__name__)

        if format.understand(f) >= 2:
            i = format(f)
            print(i.get_xbeam())
            print(i.get_xgoniometer())
            print(i.get_xdetector())

    return time.time() - s


def TestRegistry2(files):
    """First find the class, then read every frame with it."""

    s = time.time()

    format = Registry.find(files[0])

    b0 = format(files[0]).get_xbeam()
    g0 = format(files[0]).get_xgoniometer()
    d0 = format(files[0]).get_xdetector()

    for f in files:

        print(f)

        i = format(f)
        print(i.get_xbeam())
        print(i.get_xgoniometer())
        print(i.get_xdetector())
        print(i.get_xscan())

        print(i.get_xbeam() == b0, i.get_xgoniometer() == g0, i.get_xdetector() == d0)

    return time.time() - s


def TestRegistry3(files):
    """First find the class, then read every frame with it, then add the scans
    together to make sure that they all make sense."""

    s = time.time()

    format = Registry.find(files[0])

    scan = format(files[0]).get_xscan()

    for f in files[1:]:

        i = format(f)

        scan += i.get_xscan()

    print(scan)
    print(scan[: len(scan) // 2])
    print(scan[:])
    print(scan[: len(scan)])
    print(scan[1 + len(scan) // 2 :])

    return time.time() - s


if __name__ == "__main__":

    # t = TestRegistry(sys.argv[1:])
    t = TestRegistry2(sys.argv[1:])
    # t = TestRegistry3(sys.argv[1:])

    print(t)
