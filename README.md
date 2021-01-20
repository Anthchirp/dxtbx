## DX2 project

### Discussion

Features of dxtbx we want to preserve in a re-write:
- Most of the models (beam, detector, crystal, gonio, scan)
- The registry
- In-memory representation of data (like what we get from MemImageSet). Supports streaming.

Things that should go away
- Imageset/imagesweep
- Lazy will be unnecessary because models are random access and read on demand
- Datablocks
- Detectorbase
- `check_format` (implicit in random access/read on demand)

New features that are desired
- Retain more details of the goniometer stack
- Proper definition of scan
- ImageSetData, Reader
- numpy back end as option?
    - would likely enable pybind11
- Match the crystal B matrix convention to IUCr convention.
- `get_image_size` is fast/slow but get raw data is slow/fast
- Count everything from zero
- Array dimensions are in C order
- Remove magic from option parser
- Assume filenames are "sensible" i.e. `.nxs` are nexus files, etc.
- Assume `.expt` is experiments, `.refl` is reflections
- Formats have list of supported filename extensions :thinking_face:
- Define 'half object' conventions (pixel coordinates, U matrix rotations)
- Fast deserialization

Conclusion of discussion: consensus was to take this forward to a project proposal to active collaborators, with an explicit rename such that dxtbx continues along it's existing path for non-DIALS users.


## Diffraction Experiment Toolbox

![Python 3.6 | 3.7 | 3.8](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue.svg)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/dials/dxtbx.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/dials/dxtbx/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/dials/dxtbx.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/dials/dxtbx/alerts/)
[![Coverage](https://codecov.io/gh/cctbx/dxtbx/branch/master/graph/badge.svg)](https://codecov.io/gh/cctbx/dxtbx)
[![DOI](https://img.shields.io/badge/DOI-10.1107/S1600576714011996-blue.svg)](https://doi.org/10.1107/S1600576714011996)

A [cctbx](https://cctbx.github.io/)-style toolbox to describe single-crystal diffraction experiments, where
a monochromatic beam is used to illuminate a sample which is rotated during
the exposure and diffraction recorded on a flat area detector.

This toolbox will include code for:

 * reading image headers
 * transforming contents of image header to standard (i.e. imgCIF) frame
 * python models of experiment
 * reading a sequence into memory using existing cctbx image reading tools in [iotbx](https://cctbx.github.io/iotbx/index.html)

Initially implemented to support [xia2](https://github.com/xia2/xia2) development, dxtbx is designed to be extensible, to support other applications and to make it easy to work with other detectors, with a generic approach to reading the data files.

A paper describing how to use dxtbx, as well as documenting its development and some of its applications, was published as [J. Appl. Cryst. (2014) **47**, 1459-1465](https://doi.org/10.1107/S1600576714011996).
