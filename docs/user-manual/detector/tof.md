# TOF

## GID conversion

All `tof_gid_to_*` and `get_tof_gid` are decorated with `@nb.vectorize`.
The calling convention is identical for scalar, NumPy array, and Awkward Array inputs:

=== "Scalar"

    ```python
    import pybes3 as p3

    gid = 0
    part = p3.tof_gid_to_part(gid)          # 0
    layer_or_module = p3.tof_gid_to_layer_or_module(gid)
    phi_or_strip = p3.tof_gid_to_phi_or_strip(gid)

    gid = p3.get_tof_gid(part, layer_or_module, phi_or_strip)
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    gid = np.array([0, 100, 500])
    part = p3.tof_gid_to_part(gid)          # array([0, 1, 3])
    layer_or_module = p3.tof_gid_to_layer_or_module(gid)
    phi_or_strip = p3.tof_gid_to_phi_or_strip(gid)

    gid = p3.get_tof_gid(part, layer_or_module, phi_or_strip)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    gid = ak.Array([[0, 100], [500]])
    part = p3.tof_gid_to_part(gid)          # <Array [[0, 1], [3]] type='...'>
    layer_or_module = p3.tof_gid_to_layer_or_module(gid)
    phi_or_strip = p3.tof_gid_to_phi_or_strip(gid)

    gid = p3.get_tof_gid(part, layer_or_module, phi_or_strip)
    ```

!!! note
    The convention of `part` field is different from BOSS:

    - 0, 1, 2: scintillator endcap 0, barrel, endcap 1
    - 3, 4: MRPC endcap 0, endcap 1

    The scintillator `layer` and MRPC `module` share the same axis, and the `phi` and `strip` fields also share the same axis.

## GID parser

Use `parse_tof_gid` to parse all fields from a gid at once:

```python
# parse all fields; returns a dict (or ak.Array when the input is an ak.Array)
res = p3.parse_tof_gid(gid)
part = res["part"]
layer_or_module = res["layer_or_module"]
phi_or_strip = res["phi_or_strip"]
```

When the input is an `ak.Array`, the result is also an `ak.Array` with record fields.


## Hit status

`pybes3` provides implementation of `TofHitStatus` functions. They are defined as `tof_hit_status_to_*`. All these functions are decorated with `@nb.vectorize`. The calling convention is identical for scalar, NumPy array, and Awkward Array inputs:

=== "Scalar"

    ```python
    import pybes3 as p3

    hit_status = 0
    is_raw = p3.tof_hit_status_to_is_raw(hit_status)
    is_readout = p3.tof_hit_status_to_is_readout(hit_status)
    is_counter = p3.tof_hit_status_to_is_counter(hit_status)
    is_cluster = p3.tof_hit_status_to_is_cluster(hit_status)
    is_barrel = p3.tof_hit_status_to_is_barrel(hit_status)
    is_east = p3.tof_hit_status_to_is_east(hit_status)
    is_overflow = p3.tof_hit_status_to_is_overflow(hit_status)
    is_multihit = p3.tof_hit_status_to_is_multihit(hit_status)
    is_mrpc = p3.tof_hit_status_to_is_mrpc(hit_status)
    layer = p3.tof_hit_status_to_layer(hit_status)
    n_counter = p3.tof_hit_status_to_n_counter(hit_status)
    n_east = p3.tof_hit_status_to_n_east(hit_status)
    n_west = p3.tof_hit_status_to_n_west(hit_status)
    ```

=== "NumPy array"

    ```python
    import numpy as np
    import pybes3 as p3

    hit_status = np.array([0, 1, 256])
    is_raw = p3.tof_hit_status_to_is_raw(hit_status)
    is_readout = p3.tof_hit_status_to_is_readout(hit_status)
    is_counter = p3.tof_hit_status_to_is_counter(hit_status)
    is_cluster = p3.tof_hit_status_to_is_cluster(hit_status)
    is_barrel = p3.tof_hit_status_to_is_barrel(hit_status)
    is_east = p3.tof_hit_status_to_is_east(hit_status)
    is_overflow = p3.tof_hit_status_to_is_overflow(hit_status)
    is_multihit = p3.tof_hit_status_to_is_multihit(hit_status)
    is_mrpc = p3.tof_hit_status_to_is_mrpc(hit_status)
    layer = p3.tof_hit_status_to_layer(hit_status)
    n_counter = p3.tof_hit_status_to_n_counter(hit_status)
    n_east = p3.tof_hit_status_to_n_east(hit_status)
    n_west = p3.tof_hit_status_to_n_west(hit_status)
    ```

=== "Awkward Array"

    ```python
    import awkward as ak
    import pybes3 as p3

    hit_status = ak.Array([[0, 1], [256]])
    is_raw = p3.tof_hit_status_to_is_raw(hit_status)
    is_readout = p3.tof_hit_status_to_is_readout(hit_status)
    is_counter = p3.tof_hit_status_to_is_counter(hit_status)
    is_cluster = p3.tof_hit_status_to_is_cluster(hit_status)
    is_barrel = p3.tof_hit_status_to_is_barrel(hit_status)
    is_east = p3.tof_hit_status_to_is_east(hit_status)
    is_overflow = p3.tof_hit_status_to_is_overflow(hit_status)
    is_multihit = p3.tof_hit_status_to_is_multihit(hit_status)
    is_mrpc = p3.tof_hit_status_to_is_mrpc(hit_status)
    layer = p3.tof_hit_status_to_layer(hit_status)
    n_counter = p3.tof_hit_status_to_n_counter(hit_status)
    n_east = p3.tof_hit_status_to_n_east(hit_status)
    n_west = p3.tof_hit_status_to_n_west(hit_status)
    ```

Use `parse_tof_hit_status` to parse all fields from a hit status at once:

```python
parse_result = p3.parse_tof_hit_status(hit_status)
is_raw = parse_result["is_raw"]
is_readout = parse_result["is_readout"]
is_counter = parse_result["is_counter"]
is_cluster = parse_result["is_cluster"]
is_barrel = parse_result["is_barrel"]
is_east = parse_result["is_east"]
is_overflow = parse_result["is_overflow"]
is_multihit = parse_result["is_multihit"]
is_mrpc = parse_result["is_mrpc"]
layer = parse_result["layer"]
n_counter = parse_result["n_counter"]
n_east = parse_result["n_east"]
n_west = parse_result["n_west"]
```
