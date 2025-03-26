# Global ID (gid)

!!! info
    This page only illustrates the gid of each detector element. To convert gid to other information, please refer to [Geometry](geometry.md).

To better locate each detector element, a global ID (gid) is defined. GID always starts from 0 and increases along the detector elements. The increasing order is described by a tuple-like structure.

For example, MDC gid can be described as `(layer, wire)`, which means it increases first along the `wire` and then along the `layer`, as shown below:

| layer | wire | gid |
| :---: | :--: | :-: |
| 0     | 0    | 0   |
| 0     | 1    | 1   |
| 0     | ...  | ... |
| 1     | 0    | 40  |
| 1     | 1    | 41  |
| ...   | ...  | ... |

> There are 40 wires on layer-0 in MDC.

## MDC

| Range | Increasing Order |
| :---: | :--------------: |
| 0~6795 | (layer, wire) |

!!! success "Same as BOSS"
    MDC gid is same as those given by `MdcGeomSvc` in `BOSS`

## TOF

|   Range   |   Increasing Order   |      Part      |
| :-------: | :------------------: | :------------: |
|   0~95    |     (strip, end)     | Scint Endcap 0 |
|  96~447   |  (layer, phi, end)   |  Scint Barrel  |
|  448~543  |      (phi, end)      | Scint Endcap 1 |
| 544~1407  | (module, strip, end) | MRPC Endcap 0  |
| 1408~2271 | (module, strip, end) | MRPC Endcap 1  |

## EMC

|   Range   | Increasing Order |   Part   |
| :-------: | :--------------: | :------: |
|   0~479   |   (theta, phi)   | Endcap 0 |
| 480~5759  |   (theta, phi)   |  Barrel  |
| 5760~6239 |  (-theta, phi)   | Endcap 1 |

The concrete relationship between gid and `(theta, phi)` for EMC endcap 0 is:

|  Range  | Number of Crystals | Theta |   Description   |
| :-----: | :----------------: | :---: | :-------------: |
|  0~63   |         64         |   0   | Innermost layer |
| 64~127  |         64         |   1   |                 |
| 128~207 |         80         |   2   |                 |
| 208~287 |         80         |   3   |                 |
| 288~383 |         96         |   4   |                 |
| 384~479 |         96         |   5   | Outermost layer |

The concrete relationship between gid and `(theta, phi)` for EMC endcap 1 is:

|   Range   | Number of Crystals | Theta |   Description   |
| :-------: | :----------------: | :---: | :-------------: |
| 5760~5855 |         96         |   5   | Outermost layer |
| 5856~5951 |         96         |   4   |                 |
| 5952~6031 |         80         |   3   |                 |
| 6032~6111 |         80         |   2   |                 |
| 6112~6175 |         64         |   1   |                 |
| 6176~6239 |         64         |   0   | Innermost layer |


!!! success "Same as BOSS"
    EMC gid is same as those given by `EmcCalibSvc` in `BOSS`

## MUC

Under development

## CGEM

Under development