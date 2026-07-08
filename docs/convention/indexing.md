# Indexing

To uniquely locate each detector element, `pybes3` assigns it a zero-based index. The index starts from 0 and increases sequentially along the detector elements. This is very useful when indexing and mapping detector elements in arrays (e.g. defining an array to store some information for each MDC wire).

The increasing order is described by a tuple-like structure. For example, the MDC index follows the order `(layer, wire)`, meaning it increases first along `wire`, then along `layer`:

```
(layer=0, wire=0) => idx=0
(layer=0, wire=1) => idx=1
...
(layer=0, wire=39) => idx=39
(layer=1, wire=0) => idx=40
(layer=1, wire=1) => idx=41
...
```

!!! note
    This section only describes the index numbering scheme for each detector. In APIs and code examples, the index is abbreviated as `idx`. For how to parse and calculate indices, see the [MDC](../user-manual/detector/mdc.md), [TOF](../user-manual/detector/tof.md), [EMC](../user-manual/detector/emc.md), [CGEM](../user-manual/detector/cgem.md) pages and the [Detector API](../api/pybes3.detectors.md).

## MDC

| Range  | Increasing Order |
| :----: | :--------------: |
| 0-6795 | (layer, wire)    |

!!! success "Same as BOSS"
    The MDC index is the same as the one given by `MdcGeomSvc` in `BOSS`.

## TOF

| Range  |        Increasing Order         |
| :----: | :-----------------------------: |
| 0-1135 | (part, layer/module, phi/strip) |

The convention of `part` field is different from BOSS:

- 0, 1, 2: scintillator endcap 0, barrel, endcap 1
- 3, 4: MRPC endcap 0, endcap 1

The scintillator `layer` and MRPC `module` share the same axis, and the `phi` and `strip` fields also share the same axis.

## EMC

|   Range   | Increasing Order |   Part   |
| :-------: | :--------------: | :------: |
| 0-479     |   (theta, phi)   | Endcap 0 |
| 480-5759  |   (theta, phi)   |  Barrel  |
| 5760-6239 |  (-theta, phi)   | Endcap 1 |

The concrete relationship between the index and `(theta, phi)` for EMC endcap 0 is:

|  Range  | Number of Crystals | Theta |   Description   |
| :-----: | :----------------: | :---: | :-------------: |
| 0-63    |         64         |   0   | Innermost layer |
| 64-127  |         64         |   1   |                 |
| 128-207 |         80         |   2   |                 |
| 208-287 |         80         |   3   |                 |
| 288-383 |         96         |   4   |                 |
| 384-479 |         96         |   5   | Outermost layer |

The concrete relationship between the index and `(theta, phi)` for EMC endcap 1 is:

|   Range   | Number of Crystals | Theta |   Description   |
| :-------: | :----------------: | :---: | :-------------: |
| 5760-5855 |         96         |   5   | Outermost layer |
| 5856-5951 |         96         |   4   |                 |
| 5952-6031 |         80         |   3   |                 |
| 6032-6111 |         80         |   2   |                 |
| 6112-6175 |         64         |   1   |                 |
| 6176-6239 |         64         |   0   | Innermost layer |


!!! success "Same as BOSS"
    The EMC index is the same as the one given by `EmcCalibSvc` in `BOSS`.

## MUC

!!! note "Under development"

## CGEM

| Range  |         Increasing Order          |
| :----: | :-------------------------------: |
| 0-9896 | (layer, sheet, strip_type, strip) |

Where `strip_type=0` for x-strips and `strip_type=1` for v-strips.
