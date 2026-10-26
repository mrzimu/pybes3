# BesVis geometry export tools (TOF scintillator / TOF MRPC / MUC / CGEM)

These standalone programs export the geometry tables pybes3 uses. They follow the index
conventions and node-name formulas of the event-display library (`EventDisplay/BesVisLib`)
and write the tables with exactly the columns and units of the corresponding BOSS exporters
in `dev/boss-algs`, so the output is both comparable with the display side and directly
usable by the `export-*.py` scripts of this directory (see
[Related tools](#related-tools)).

| program | geometry file | reference implementation | exported content |
|---|---|---|---|
| `dump_tof_scin_vtx` | `$GDMLMANAGEMENTDATAROOT/dat/Tof.gdml` | `BesVisLib/src/TofROOTGeo.cxx` (non-MRPC branch) + `TofROOTGeo::Init2DGeometry()` | 272 scintillators x 8 vertices -> `tof-scint-vertices.csv` |
| `dump_tof_mrpc` | `$GDMLMANAGEMENTDATAROOT/dat/Tof_mrpc.gdml` | `BesVisLib/src/TofROOTGeo.cxx` (MRPC branch) | 864 endcap MRPC readout strips x 8 vertices -> `tof-mrpc-vertices.csv` |
| `dump_muc_strip_vtx` | `$GDMLMANAGEMENTDATAROOT/dat/Muc.gdml` | `BesVisLib/src/MucROOTGeo.cxx`, `Init2DGeometry()` lines 521-606 | 9152 readout strips x 8 vertices -> `muc-vtx.csv` |
| `dump_cgem_strip` | `$GDMLMANAGEMENTDATAROOT/dat/Cgem.gdml` + `$CGEMGEOMSVCROOT/dat/cgem_model_6_default.txt` | `BesVisLib/src/CgemROOTGeo.cxx` + `Cgem2DStrip.cxx` + `Cgem/CgemGeomSvc` | 3780 X + 6117 V strips, analytic parameters -> `cgem_strip.csv` |

All output is in **cm**; the three vertex tables print with 6 significant digits, i.e. the
very same text as the BOSS exporters that produced the tables the shipped
`src/pybes3/data/*.npz` files were built from (checked byte by byte against the CSVs of
`dev/boss-algs`: `ExportTofScintGeom`, `ExportTofMrpcGeom`, `ExportMucGeom`).

> Scope: of the geometry tables pybes3 ships (`tof_geom.npz`, `muc_geom.npz`, `cgem_geom.npz`,
> `emc_geom.npz`, `mdc_geom.npz`), this directory covers the three that are read from the GDML
> through BesVisLib: TOF, MUC and CGEM. There is no program for EMC (`emc_geom.npz` is
> exported by `ExportEmcGeomAlg` in `dev/boss-algs`) or for MDC (no generator script in this
> repository).

All geometry files are GDML files under `$GDMLMANAGEMENTDATAROOT/dat/*.gdml` (plus the CGEM
layer parameter file under `$CGEMGEOMSVCROOT/dat/`), and they are all read through the BOSS
`TGDMLProcessor` (see [Implementation notes](#implementation-notes-why-not-tgeomanagerimport)).
**A configured BOSS environment is therefore required to read them**: `$GDMLMANAGEMENTDATAROOT`
(and `$CGEMGEOMSVCROOT` for `dump_cgem_strip`) must be set, and ROOT together with
`BesVisLib`/`ROOTGeo` has to be on the include and library search paths. `dump_cgem_strip`
refuses to run and reports the missing variables when they are not set.

## Build and run

A BOSS environment has to be configured first (it provides ROOT, `BesVisLib`/`ROOTGeo`,
`$GDMLMANAGEMENTDATAROOT` and `$CGEMGEOMSVCROOT`, and must be based on a C++20-capable
compiler); use whatever setup script your installation provides. Once the environment is
active, go to this directory and build:

```bash
cd dev/geometry

./build.sh                                 # compile the four programs
./dump_tof_scin_vtx   > tof-scint-vertices.csv   # 272 rows, gid 0..271
./dump_tof_mrpc       > tof-mrpc-vertices.csv    # 864 rows, gid 272..1135
./dump_muc_strip_vtx  > muc-vtx.csv        # 9152 rows, gid 0..9151
./dump_cgem_strip     > cgem_strip.csv     # 9897 rows, gid 0..9896
./dump_cgem_strip --model 3 > cgem_strip_model3.csv   # another layer-parameter model
```

Every program writes one **CSV** table in **cm**, one row per element (see the sections
below).

Index columns per program:

| program | index columns |
|---|---|
| `dump_tof_scin_vtx` | `gid part layer_or_module phi_or_strip` (gid = row index 0..271) |
| `dump_tof_mrpc` | `gid part layer_or_module phi_or_strip` (part 3 = East, 4 = West) |
| `dump_muc_strip_vtx` | `gid part segment layer strip` |
| `dump_cgem_strip` | `gid layer sheet strip_type strip` (`strip_type` = 0 X / 1 V) |

The CSV column names are the ones `export-tof-geom.py` of this directory (and its BOSS
counterparts) expect; `layer_or_module`/`phi_or_strip` are the generic names shared by
scintillators and MRPC strips, and `segment`/`layer` are the MUC names of `seg`/`gap`.

### TOF scintillators: 8-vertex CSV

`dump_tof_scin_vtx` prints exactly the 8 vertices computed by `TofROOTGeo::Init2DGeometry()`
of the display side, so the 2D drawings can be reproduced directly:

```
gid,part,layer_or_module,phi_or_strip,x0,y0,z0,...,x7,y7,z7      (one row per scintillator)
```

gid runs 0..271 in (part, layer, scin) order, `layer_or_module` is `layer` and
`phi_or_strip` is `scin`; the coordinates are in cm.

Vertex order is the display-side order: `i = 0..3 -> local z = -Dz`, `i = 4..7 -> local
z = +Dz`. The two 4-point polygons of the display can be rebuilt from it:

```python
P  = [(x_0,y_0,z_0), ...]                      # the 8 vertices
XY = [(P[j]+P[j+4])/2 for j in range(4)]       # XY view polygon
iseq = [0,3,1,2,5,6,4,7]
ZR = [(P[iseq[2*i]]+P[iseq[2*i+1]])/2 for i in range(4)]   # ZR view polygon
```

Example: for barrel `part=1 layer=0 scin=0` the 8 vertices have z = +/-1150 mm (a long bar
along z); for endcap `part=0 layer=0 scin=0` z = 1332/1380 mm and the XY projection is a
quadrilateral of about 430x107 mm.

### TOF MRPC CSV

`dump_tof_mrpc` exports the 864 endcap MRPC readout strips; the barrel scintillators of the
same GDML are exported by `dump_tof_scin_vtx` and are therefore not repeated here.

```
gid,part,layer_or_module,phi_or_strip,x0,y0,z0,...,x7,y7,z7      (one row per strip)
```

- `part` = 3 (East) / 4 (West) -- the numbering used by the reconstruction and by pybes3,
  while the display uses 0/2 internally (the `ipart` mapping in the source)
- `layer_or_module` = module 0..35, `phi_or_strip` = strip 0..11
- gid runs 272..1135, i.e. it continues after the 272 scintillators

The vertex rule:

| shape | where | vertices from |
|---|---|---|
| `TGeoTrd2` (**does not** inherit `TGeoArb8`) | endcap readout strips | built from `dx1/dx2/dy1/dy2/dz`; order i=0..3 low-z face, i=4..7 high-z face |

> Warning: the MRPC branch of `TofROOTGeo::Init2DGeometry()` casts with
> `(TGeoArb8*)mrpcPhyNode->GetShape()` -- an illegal cross-class cast for `TGeoTrd2`
> (undefined behaviour), so the MRPC 2D drawing of the display is not trustworthy. This
> CSV gives the vertices computed from the correct `TGeoTrd2` geometry.

Measured (all 864 strips agree): `dx1 = dx2` (no taper), `dy1 = dy2 = 0.0175 mm`,
`dz = 12 mm`, i.e. every strip is a 0.035 mm thick, 24 mm wide sheet; its length decreases
with the strip index: `dx = 70.5 - 2.25*strip` mm (strip 0 = 141 mm, strip 11 = 91 mm),
identical for every module. The volume-name index is **inverted** with respect to the strip
index: strip 0 uses `logical_strip_11`, strip 11 uses `logical_strip_0`. The program also
cross checks "the strip found by name" against "the strip taken by copy index inside
pcbBoard1"; currently all 864 strips agree (0 mismatches).

> Note: the barrel scintillators of `Tof_mrpc.gdml` are placed with slightly different
> matrices than in `Tof.gdml` (about 5e-4 mm for the same scintillator centre), which is why
> the definitive scintillator table is the one of `Tof.gdml` (`dump_tof_scin_vtx`).

### MUC readout strips: 8-vertex CSV

`dump_muc_strip_vtx` exports exactly the 8 vertices that `MucROOTGeo::Init2DGeometry()`
computes for the readout strips:

```
gid,part,segment,layer,strip,cx,cy,cz,dx,dy,dz,x0,y0,z0,...,x7,y7,z7
    one row per strip (9152 rows), gid = 0..9151, all lengths in cm
```

- `cx/cy/cz`: global coordinates of the strip node origin; `dx/dy/dz`: local shape half sizes
- `segment`/`layer` are the `seg`/`gap` of the display (`m_kSeg`/`m_kGap`)
- the order of the 8 local corners (**copied from the switch of the display, not a
  convex-hull order**):

| i | local coordinates | | i | local coordinates |
|---|---|---|---|---|
| 0 | (−dx, −dy, −dz) | | 4 | (−dx, −dy, +dz) |
| 1 | (+dx, −dy, −dz) | | 5 | (+dx, −dy, +dz) |
| 2 | (+dx, +dy, −dz) | | 6 | (+dx, +dy, +dz) |
| 3 | (−dx, +dy, −dz) | | 7 | (−dx, +dy, +dz) |

> Note: the display scales `dz` by `m_kStripZMuliple = 12` before drawing (the strips are too
> thin to be visible otherwise: 0.5 mm -> 6 mm on screen); this tool always exports the
> **true** geometry, because that is what the reconstruction needs.

The number of strips is not a constant (this is what makes the MUC different from the other
subdetectors):

| region | strips per gap | subtotal |
|---|---|---|
| East / West endcap (4 seg x 8 gap) | 64 | 2048 x 2 = 4096 |
| Barrel (seg 0,1,3-7, 8+1 gap) | alternating 48 / 96 | 7 x 624 = 4368 |
| Barrel seg 2 (uses another set of SP volumes) | alternating 48 / 112 | 688 |
| **total** | | **9152** |

Measured (all 9152 rows pass): mean of the 8 points = the centre, the three edge lengths =
2dx/2dy/2dz, the three axes are orthogonal, volume = 8*dx*dy*dz; every shape is a
`TGeoBBox` (`dynamic_cast` succeeds) and every shape origin is 0 (so ignoring
`GetOrigin()` in the display is harmless here). Size distribution:

| region | dx (half length, mm) | dy (half length, mm) | dz |
|---|---|---|---|
| endcap | 16.5 ... 1054 (123 values) | 15.5 ... 1045 (100 values, varying with the strip index) | 0.5 |
| Barrel | 9 ... 833 (17 values) | 13 / 18.5 / 1554 / 1589 / 1859 | 0.5 |

#### Shape and orientation (measured)

There is only **one** strip shape: `TGeoBBox`, a **rectangular thin plate centred on the
node origin** (all shape origins are 0). The thickness direction is always 2*dz = **1 mm**
(identical for all 9152 strips); the other two directions vary with the position. Each `SP`
(readout plane) volume of a gap contains **only one orientation**:

| region | strips/gap | long edge direction (global) | strip length | strip width |
|---|---|---|---|---|
| endcap even gap (0,2,4,6) | 64 | along x | 2*dx = 919 ... 2108 mm | 33 / 48 mm |
| endcap odd gap (1,3,5,7) | 64 | along y | 2*dy = 925 ... 2090 mm | 33 ... 53 mm |
| barrel even gap (0,2,4,6,8) | 48 | along z | 2*dy = 3718 mm (fixed) | 18 ... 46 mm |
| barrel odd gap (1,3,5,7) | 96 | tangential (rotated per seg) | 2*dx = 1218 ... 1666 mm | 26 / 37 mm |

- the endcap strips are globally **axis-aligned** boxes (their three edges run along
  x/y/z), because the endcaps are flat; the barrel strips are **rotated** boxes (long edge
  along z or tangential, thickness along the radius), hence they are boxes only in the
  local frame.
- the endcap strip length varies with the position because the strips have to fill the
  "octagonal disc" of `solidMuc` (a box of 2630 minus an R=1700 bore and a hole), so their
  ends are clipped by the boundary; the barrel strips along z have a fixed length of 3718 mm.
- "one orientation per gap" is a fact of the geometry itself, not an oversight of the
  display taking only one daughter: the box (`lMucP0S0G0Al`) has 25-27 daughters, `[0]` = SP
  (the readout plane), `[1][2]` = the aluminium surfaces, `[3..]` = the RPC chambers
  (`R0Pn0B0/B1...`); the display takes daughter 0 = SP, which agrees with the geometry.

The display then collapses these 8 points into two polygons (this tool does **not** export
them; copy the following lines to reproduce):

```python
P = [p0..p7]
# XY view (4 points)
if part == 1: XY = [(P[1]+P[2])/2, (P[0]+P[3])/2, (P[4]+P[7])/2, (P[5]+P[6])/2]
else:         XY = [(P[i]+P[i+4])/2 for i in range(4)]
# ZR view (6 points)
iZR = [4,5,1,2,6,7] if part == 1 else [1,2,3,7,6,5]
ZR  = [P[i] for i in iZR]
```

(the barrel ZR polygon additionally gets `SetRotatable(true)` and is rotated around z by
`viewPhi−180°` when drawn.)

### CGEM X/V strip parameters (`dump_cgem_strip`)

The CGEM readout strips are **not** in the GDML path used by the display:
`CgemROOTGeo::InitGeometry()` takes the parametric model from the Gaudi service
`CgemGeomSvc` (`$CGEMGEOMSVCROOT/dat/cgem_model_6_default.txt`) to build the X/V strips.
This table follows the same route: layer parameters from that file, strip shell radii from
the GDML `Anode_X_Strip_solid<L>` / `Anode_V_Strip_solid<L>` (= `getInnerROfAnodeCu2()` /
`getInnerROfAnode()` of the service).

```
gid,layer,sheet,strip_type,strip,r,phi0,dphi,z0,dz,width,thick
```

| column | meaning |
|---|---|
| `strip_type` | 0 = X strip, 1 = V strip (same convention as `cgem_elec_table.npz`) |
| `r` | strip radius (x -> rx, v -> rv), cm |
| `phi0` | azimuth of the centre line at the **most negative z** end (rad) |
| `dphi` | total azimuth change from that end towards **+z** (**signed**) |
| `z0` | most negative z of the centre line (cm) |
| `dz` | total z change towards +z (>= 0), cm |
| `width` | transverse width of the strip (cm): x strip = 0.058 in the arc direction; v strip = 0.013 in the **perpendicular** direction |
| `thick` | **radial thickness** of the strip (cm) = readout Cu layer thickness = `rmax - rmin` of the strip shell; x strips = Cu2 shell, v strips = Cu1 shell, **0.0005 in the whole table** |

- `(r, phi0, dphi, z0, dz)` give the centre line and `(width, thick)` the cross section ->
  the strip is uniquely reconstructed
- centre line length (if needed) = sqrt((dphi*r)^2 + dz^2), not listed
- X strips run along z: `dphi = 0`, `dz` = full sheet length
- layer 0 has a single sheet covering the whole 2*pi (phi in [-pi, pi]); the longest V strip
  has `dphi = 6.258 rad = 358.6 deg` (it can wind almost once but never leaves +/-pi);
  layers 1/2 cover pi per sheet
- self check: `thick = 0.0005` for the whole table; all X strips have `dphi = 0` and
  `width = 0.058`

The plane constants of each sheet, needed to interpret `(r, phi0, dphi, z0, dz)`, are (mm):

| layer | sheet | rx | rv | rmid | xmin | width | zmin | length | alpha(deg) | zref | nx | nv | vmin |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 90.195 | 90.140 | 90.1675 | −283.27 | 566.71 | −266 | 532 | +46.6877 | 266 | 856 | 1173 | 0.232 |
| 1 | 0 / 1 | 132.555 | 132.500 | 132.5275 | −416.35 / 0 | 416.43 | −345 | 690 | −31.0337 | −345 | 630 | 1077 | 0.594 |
| 2 | 0 / 1 | 175.250 | 175.195 | 175.2225 | −550.48 / 0 | 550.56 | −423.5 | 847 | +32.9244 | 423.5 | 832 | 1395 | 0.298 |

(lengths in mm; `xpitch = vpitch = 0.66`, strip widths `wstrip_x = 0.58`, `wstrip_v = 0.13`;
layer0 has a single sheet covering the full phi, layers 1/2 have 2 sheets each)

For a **V strip** the centre line is, in the unfolded plane (x = phi*r, z), the straight line

$$V = (x - x_0)\cos\alpha - (z - z_{\rm ref})\sin\alpha$$

where `x0` is the origin of the V frame (arc length) and `zref = (k<0) ? zmin :
zmin+length`. The strip is clipped to the x sensitive rectangle
`[x0, x0+(nx-1)*xpitch+wstrip_x] x [zmin, zmin+length]` (slightly smaller than the sheet,
about 0.8 mm on each side), exactly as `CgemVStripCalculator` of the display does; `phi0`,
`dphi`, `z0`, `dz` are the resulting end points. The reconstruction-side service uses a
slightly different rectangle, see the note below.

Measured and cross checked:
- strip counts: X **3780** (856 + 630x2 + 832x2) + V **6117** (1173 + 1077x2 + 1395x2) =
  9897, none invalid
- all 12234 V strip end points lie exactly on the clipping rectangle and satisfy the line
  equation to 9e-7 mm (= the six-decimal rounding of the CSV)
- `length` agrees exactly with the `z` of the X strip shell in the GDML (532 / 690 / 847)
- `xpitch = 0.660` agrees with `dphi*rmin` of the X strip shell (0.6605 / 0.6605 / 0.6601 mm)
- the V strip shell in the GDML is a **full thin ring** with `dphi = 360 deg` (0.094 / 0.166 /
  0.154 mm thick) -- this models "a V strip as thousands of ring slices stacked along z, each
  rotated a bit in phi so that they form a helical band" (`BesCgemConstruction.cc:1100-1210`)

#### The same table from the BOSS service

`ExportCgemGeomAlg` in `dev/boss-algs` is the counterpart of this program: it reads the very
same layer parameters through `CgemGeomSvc` instead of the text file plus the GDML, and
writes a ROOT ntuple with the same 12 columns (opts
`NumAndGeom/opts/ExportCgemGeom.txt`); `src/pybes3/data/cgem_geom.npz` was built from it.
Row-by-row comparison: `gid`, `layer`, `sheet`, `strip_type`, `strip`, `r` and `width` agree
**exactly**; V strips differ by <= 4.4e-4 rad (phi) / 0.13 mm (z, length), coming from the
convention difference between the "display clipping rectangle (`clipXmin/clipWidth`)" and
the "sensitive rectangle of the service `[0, NX*XPitch]x[0,L]`" (origin differs by 0.04 mm,
width by 0.08 mm).

Two caveats:

1. when drawing, the display hard-codes the strip thickness to `0.1 mm` and discretises the
   V strips every `delta = 30 mm` into a polyline; in the XY view the V strip is drawn as a
   **ring segment** (inner r-0.05 / outer r+0.05). These are **rendering-only** quantities
   and are not exported here; the real width and thickness are the `width`/`thick` columns.
2. the accuracy of `phi0`/`dphi`/`z0`/`dz` is cross checked against the service's own
   three-branch formula `CgemGeoReadoutPlane::getVStripLength()`; the difference (at most
   ~0.16 mm in the "strip reaches a corner" case) is reported on stderr. That function is
   itself only used by the diagnostic `testReadoutPlane()` of the service.

## Index and node name conventions (copied from BesVisLib)

### TOF (`part`: 0=East, 1=Barrel, 2=West)

```
Barrel : layer 0..1 (m_kLayerBr=2), scin 0..87 (m_kScinBr=88)
         PVF  = pv_logicalPVFBr<layer+1>_< (2*88*3-1) - (layer*88+scin)*3 >
         Al   = pv_logicalAlBr<layer+1>_0
         Scin = pv_logicalScinBr<layer+1>_0
endcap : layer 0, scin 0..47 (m_kScinEc=48)
         PVF  = pv_logicalPVFEc{East|West}_< (2*48-1) - scin*2 >
         Al   = pv_logicalAlEc{East|West}_0
         Scin = pv_logicalScinEc{East|West}_0
path   : <part>/<PVF>/<Al>/<Scin>            (TofROOTGeo::SetPhysicalNode)
```

### TOF MRPC (endcap)

```
module 0..35 (m_kModuleEc=36), strip 0..11 (m_kStripEc=12)
the module volume name depends on part and module parity:
    part 0: even -> logical_container_m0_<module>, odd -> logical_container_m3_<module>
    part 2: even -> logical_container_m1_<module>, odd -> logical_container_m2_<module>
gasContainer = pv_logical_gasContainer_m<K>_0     (m_kContainerNodeNb = 0)
bareChamber  = pv_logical_bareChamber_6           (m_kChamberNodeNb   = 6)
pcbBoard1    = pv_logical_pcbBoard1_30            (m_kBoard1NodeNb    = 30)
strip        = pv_logical_strip_<11 - strip>_<strip>
path: <part>/<module>/<gasContainer>/<bareChamber>/<pcbBoard1>/<strip>
```

### MUC (`part`: 0=East, 1=Barrel, 2=West)

```
seg  : m_kSeg[3]      = {4, 8, 4}
gap  : m_kGap[3]      = {8, 9, 8}        (the layer of MucID)
absorber: m_kAbsorber[3] = {9, 9, 9}
gap       = pv_lMucP<part>S<seg>G<gap>_<gapCount>        gapCount increases per (part,seg,gap)
stripPlane= pv_lMucP<part>S<segment>G<gap>SP_0           segment = (part==1 && seg==2) ? 2 : 0
strip     = pv_lMucP<part>S<segment>G<gap>s<strip zero-padded to 3>_<strip>
absorber  = pv_lMucP<part>S<seg>Ab<absorber>_<absorberCount>
path: gap -> <gap>/<box>; strip -> <gap>/<box>/<stripPlane>/<strip>
      (box = daughter 0 of gap, stripPlane = daughter 0 of box)
```

## Implementation notes (why not `TGeoManager::Import`)

1. **The BOSS `TGDMLProcessor` must be used** (i.e. `BesVisLib::SubDetectorROOTGeo::ReadGdml`
   / `ROOTGeo::SubDetectorROOTGeo::ReadGdml`, both are the same processor). It assigns the
   **copy number of a physical node = the daughter index inside the parent volume**, which is
   exactly the meaning of the `_527`, `_95`, `_0` suffixes in the BesVisLib names. ROOT's own
   `TGeoManager::Import()` instead sets the copy number of every node without a
   `<copynumber>` to 0 (node names look like `logicalPVFEcEast_0`), so the display-side names
   cannot be reproduced; it also crashes while parsing `Emc.gdml`.
2. the **centre coordinates** are obtained by multiplying the "node matrix chain", which is
   equivalent to how `TGeoPhysicalNode` is used in the event display; since every subdetector
   is placed with the identity matrix in `volBes`, taking the subdetector top volume as the
   root directly gives the global coordinates of the display.
3. before exporting, each program checks whether the node name of every index can be
   resolved and counts the failures (currently **0 failures** for all programs, which means
   these name formulas of BesVisLib still match the current GDML exactly).

## Measured results (current GEANT4/BOSS GDML)

| program | rows | note |
|---|---|---|
| `dump_tof_scin_vtx` | 272 | gid 0..271; endcap scintillators z = 1332/1380 mm, barrel bars have z = +/-1150 mm |
| `dump_tof_mrpc` | 864 | `TGeoTrd2` strips, 0.035 mm thick, 24 mm wide, 91-141 mm long; gid 272..1135 |
| `dump_muc_strip_vtx` | 9152 | gid 0..9151, 8 vertices each = 73216 vertices |
| `dump_cgem_strip` | 9897 | 3780 X strips + 6117 V strips, gid 0..9896 |

## Caveats

- in the MUC, several `seg` of the same `part` **share** the same strip plane / strip
  logical volumes, so names such as `pv_lMucP0S0G0SP_0` and `pv_lMucP0S0G0s000_0` match
  multiple instances in the tree; the display locates them through the "path" (the correct
  gap -> box -> SP -> strip), and `dump_muc_strip_vtx` walks down by daughter index for the
  same reason. The local matrices of those instances are identical, so the coordinates are
  unaffected (the program reports any name/index mismatch on stderr, currently 0).
- `TofROOTGeo::GetVolumePart()` returns the string `logicalEcTofWest` for part 0 (the
  opposite of the daughter order used by `SetPhysicalNode()`); this is a historical naming
  inconsistency of the display. The programs take the node by the daughter order of
  `SetPhysicalNode()` (part 0 -> `logicalEcTofEast`).
- units: the output is in cm, like the BOSS exporters and the `src/pybes3/data/*.npz`
  tables (services such as `EmcRecGeoSvc` also return cm); the GDML and the event display
  work in mm, so multiply by 10 to compare with them.
- to switch to writing a ROOT TTree instead of a CSV (handy for comparing with the pybes3
  tables), see `dev/boss-algs/NumAndGeom/src/ExportEmcGeomAlg.cc`.
- to cross check with the reconstruction-side geometry: the MUC corresponds to
  `Muc/MucGeomSvc` (e.g. `MucGeoGap::GetRotationMatrix` also takes positions from the GDML),
  and the TOF end can use the corresponding `TofGeomSvc`.

## Related tools

- The two Python scripts of this directory turn the CSVs into the tables shipped with the
  package (they can also run the BOSS algorithms directly, when a BOSS job is available):

  ```bash
  ./dump_tof_scin_vtx > tof-scint-vertices.csv
  ./dump_tof_mrpc     > tof-mrpc-vertices.csv
  ./dump_muc_strip_vtx > muc-vtx.csv
  cd ../.. && source .venv/bin/activate
  python dev/geometry/export-tof-geom.py dev/geometry/tof-scint-vertices.csv \
                                         dev/geometry/tof-mrpc-vertices.csv
  python dev/geometry/export-muc-geom.py dev/geometry/muc-vtx.csv
  ```

  Regenerating both npz files this way reproduces the shipped
  `src/pybes3/data/{tof,muc}_geom.npz` **byte by byte** (checked).
- `dev/boss-algs` contains the BOSS algorithms that export the same geometry through the
  Gaudi services (`ExportTofScintGeom`, `ExportTofMrpcGeom`, `ExportMucGeom`,
  `ExportCgemGeomAlg`, `ExportEmcGeomAlg`); they need a configured BOSS job in order to run,
  which is exactly why these standalone programs exist.
- `dev/export-cgem-tables.py` (still in `dev/`) is unrelated to the geometry: it builds
  `cgem_elec_table.npz` from `CgemInfoLuSvc`'s `mapping.txt`. The CGEM geometry table
  (`cgem_geom.npz`) comes from `ExportCgemGeomAlg`, whose standalone counterpart is
  `dump_cgem_strip`.

## Directory contents

```
dev/geometry/
├── geomdump_common.h            shared helpers (read GDML, resolve by name, matrix chain,
│                                Arb8 eight vertices)
├── dump_tof_scin_vtx.cxx        TOF scintillators, 8 vertices (CSV)
├── dump_tof_mrpc.cxx            TOF MRPC readout strips, 8 vertices (CSV)
├── dump_muc_strip_vtx.cxx       MUC readout strips, 8 vertices (CSV)
├── dump_cgem_strip.cxx          CGEM X/V strip parameters (CSV, no ROOT dependency)
├── build.sh                     build script
├── export-tof-geom.py           CSV(s) -> src/pybes3/data/tof_geom.npz
├── export-muc-geom.py           CSV    -> src/pybes3/data/muc_geom.npz
└── .gitignore                   ignores the compiled programs
```
