#!/usr/bin/env python
# Format.py
#   Copyright (C) 2011 Diamond Light Source, Graeme Winter
#
#   This code is distributed under the BSD license, a copy of which is
#   included in the root directory of this package.
#
# A top-level class to represent image formats which does little else but
# (i) establish an abstract class for what needs to be implemented and
# (ii) include the format registration code for any image formats which
# inherit from this. This will also contain links to the static methods
# from the X(component)Factories which will allow construction of e.g.
# goniometers etc. from the headers and hence a format specific factory.

import os
import sys

try:
    import bz2
except:  # intentional
    bz2 = None

try:
    import gzip
except:  # intentional
    gzip = None

import exceptions
import traceback

# first - import access to all of the factories that we will be needing

from dxtbx.model.goniometer import goniometer, goniometer_factory
from dxtbx.model.detector import detector, detector_factory
from dxtbx.model.beam import beam, beam_factory
from dxtbx.model.scan import scan, scan_factory
from dxtbx.model.cube import cube, cube_factory


class _MetaFormat(type):
    """A metaclass for the Format base class (and hence all format classes)
    to allow autoregistration of the class implementations."""

    def __init__(self, name, bases, attributes):
        super(_MetaFormat, self).__init__(name, bases, attributes)

        from dxtbx.format.Registry import Registry

        Registry.add(self)

        return


class Format:
    """A base class for the representation and interrogation of diffraction
    image formats, from which all classes for reading the header should be
    inherited. This includes: autoregistration of implementation classes,
    stubs which need to be overridden and links to static factory methods
    which will prove to be useful in other implementations."""

    __metaclass__ = _MetaFormat

    @staticmethod
    def understand(image_file):
        """Overload this to publish whether this class instance understands
        a given file. N.B. to say that we really understand it, return a
        positive number. To say in a subclass that you understand it better
        then return a larger number, for example checking the detector serial
        number. Finally, if you are writing this subclass for a given
        instrument and you are given a different example return 0."""

        return 0

    def __init__(self, image_file):
        """Initialize a class instance from an image file."""

        self._image_file = image_file

        self._goniometer_instance = None
        self._detector_instance = None
        self._beam_instance = None
        self._scan_instance = None
        self._cube_instance = None

        self._goniometer_factory = goniometer_factory
        self._detector_factory = detector_factory
        self._beam_factory = beam_factory
        self._scan_factory = scan_factory
        self._cube_factory = cube_factory

        self.setup()

        return

    def setup(self):
        """Read the image file, construct the information which we will be
        wanting about the experiment from this. N.B. in your implementation
        of this you will probably want to make use of the static methods
        below and probably add some format parsing code too. Please also keep
        in mind that your implementation may be further subclassed by
        someone else."""

        try:
            self._start()

            goniometer_instance = self._goniometer()
            assert isinstance(goniometer_instance, goniometer)
            self._goniometer_instance = goniometer_instance

            detector_instance = self._detector()
            assert isinstance(detector_instance, detector)
            self._detector_instance = detector_instance

            beam_instance = self._beam()
            assert isinstance(beam_instance, beam)
            self._beam_instance = beam_instance

            scan_instance = self._scan()
            assert isinstance(scan_instance, scan)
            self._scan_instance = scan_instance

            cube_instance = self._cube()
            # assert(isinstance(cube_instance, cube))
            self._cube_inctance = cube_instance

        except exceptions.Exception as e:
            traceback.print_exc(sys.stderr)
        finally:
            self._end()

        return

    def get_goniometer(self):
        """Get the standard goniometer instance which was derived from the
        image headers."""

        return self._goniometer_instance

    def get_detector(self):
        """Get the standard detector instance which was derived from the
        image headers."""

        return self._detector_instance

    def get_beam(self):
        """Get the standard beam instance which was derived from the image
        headers."""

        return self._beam_instance

    def get_scan(self):
        """Get the standard scan instance which was derived from the image
        headers."""

        return self._scan_instance

    def get_cube(self):
        """Get the cube"""

        return self._cube_instance

    def get_image_file(self):
        """Get the image file provided to the constructor."""

        return self._image_file

    # methods which must be overloaded in order to produce a useful Format
    # class implementation

    def _start(self):
        """Start code for handling this image file, which may open a link
        to it once, say, and pass this around within the implementation.
        How you use this is up to you, though you probably want to overload
        it..."""

        return

    def _end(self):
        """Clean up things - keeping in mind that this should run even in the
        case of an exception being raised."""

        return

    def _goniometer(self):
        """Overload this method to read the image file however you like so
        long as the result is an goniometer."""

        raise RuntimeError, "overload me"

    def _detector(self):
        """Overload this method to read the image file however you like so
        long as the result is an detector."""

        raise RuntimeError, "overload me"

    def _beam(self):
        """Overload this method to read the image file however you like so
        long as the result is an beam."""

        raise RuntimeError, "overload me"

    def _scan(self):
        """Overload this method to read the image file however you like so
        long as the result is an scan."""

        raise RuntimeError, "overload me"

    def _cube(self):
        """Get the data cube - this method could optionally be overloaded,
        otherwise it will use the regular cube factory - which behind the
        scenes uses iotbx."""

        # FIXME since behind the scenes this goes through the
        # iotbx, it will not use the general file opening below -
        # could this be rectified?

        self._cube_instance = cube_factory.from_filename(self._image_file)

        return

    ####################################################################
    #                                                                  #
    # Helper functions for dealing with compressed images.             #
    #                                                                  #
    ####################################################################

    @staticmethod
    def is_url(path):
        """See if the file is a URL."""

        from urlparse import urlparse

        if urlparse(path).scheme:
            return True

        return False

    @staticmethod
    def is_bz2(filename):
        """Check if a file pointed at by filename is bzip2 format."""

        return "BZh" in open(filename, "rb").read(3)

    @staticmethod
    def is_gzip(filename):
        """Check if a file pointed at by filename is gzip compressed."""

        magic = open(filename, "rb").read(2)

        return ord(magic[0]) == 0x1F and ord(magic[1]) == 0x8B

    @staticmethod
    def open_file(filename, mode="rb"):
        """Open file for reading, decompressing silently if necessary."""

        if Format.is_url(filename):

            import urllib2

            return urllib2.urlopen(filename)

        if Format.is_bz2(filename):

            if bz2 is None:
                raise RuntimeError, "bz2 file provided without bz2 module"

            return bz2.BZ2File(filename, mode)

        if Format.is_gzip(filename):

            if gzip is None:
                raise RuntimeError, "gz file provided without gzip module"

            return gzip.GzipFile(filename, mode)

        return open(filename, mode)
