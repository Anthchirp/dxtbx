from __future__ import absolute_import, division
from __future__ import print_function
from dxtbx.format.FormatHDF5 import FormatHDF5


class FormatRawData(FormatHDF5):
    def __init__(self, image_file, **kwargs):
        assert self.understand(image_file)
        FormatHDF5.__init__(self, image_file, **kwargs)

    @staticmethod
    def understand(image_file):
        import h5py

        h5_handle = h5py.File(image_file, "r")

        return len(h5_handle) == 1 and "data" in h5_handle

    def _start(self):
        import h5py

        self._h5_handle = h5py.File(self.get_image_file(), "r")

    def get_raw_data(self):
        from scitbx.array_family import flex

        data = self._h5_handle["data"]
        return flex.int(data[:, :])

    def get_num_images(self):
        return 1


if __name__ == "__main__":
    import sys

    for arg in sys.argv[1:]:
        print(FormatRawData.understand(arg))
