from __future__ import absolute_import, division


class FormatMultiImage(object):
    def __init__(self, **kwargs):
        pass

    def get_num_images(self):
        raise RuntimeError("Overload!")

    def get_goniometer(self, index=None):
        raise RuntimeError("Overload!")

    def get_detector(self, index=None):
        raise RuntimeError("Overload!")

    def get_beam(self, index=None):
        raise RuntimeError("Overload!")

    def get_scan(self, index=None):
        raise RuntimeError("Overload!")

    def get_raw_data(self, index=None):
        raise RuntimeError("Overload!")

    def get_mask(self, index=None, goniometer=None):
        return None

    def get_detectorbase(self, index=None):
        raise RuntimeError("Overload!")

    def get_image_file(self, index=None):
        raise RuntimeError("Overload!")
