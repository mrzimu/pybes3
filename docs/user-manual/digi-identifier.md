# Digi identifier

When reading `TDigiEvent`, the `m_intId` field in `mdc`, `tof`, `emc`, `muc`, and `cgem` branches represents the electronics readout ID (TEID), also known as `Identifier` in `BOSS`. `pybes3` provides methods to parse and calculate the digi ID for each detector.

## Digi array parsing

!!! info
    Currently, only MDC and EMC full digi parsing is supported. Support for other detectors is under development. For unsupported detectors, use the [standalone digi ID parsing methods](#standalone-digi-id-parsing).


```python
import pybes3.identifier as p3id
import uproot

# read raw digi array
mdc_digi = uproot.open("test.rtraw")["Event/TDigiEvent/m_mdcDigiCol"].array()

# parse whole digi array
mdc_digi = p3id.parse_mdc_digi(mdc_digi)
```

## Standalone digi-ID parsing

When full digi array parsing is not necessary or not yet supported, use `parse_xxx_id` methods (where `xxx` is the detector name: `cgem`, `mdc`, `tof`, `emc`, `muc`) to parse only the digi ID:

```python
import pybes3.identifier as p3id
import uproot

# read raw digi array
tof_digi = uproot.open("test.rtraw")["Event/TDigiEvent/m_tofDigiCol"].array()
emc_digi = uproot.open("test.rtraw")["Event/TDigiEvent/m_emcDigiCol"].array()

# parse digi ID
tof_id = p3id.parse_tof_id(tof_digi["m_intId"])
emc_id = p3id.parse_emc_id(emc_digi["m_intId"])
```

!!! info
    `parse_mdc_id` and `parse_emc_id` currently return detector ID-related fields only.

## Convert digi ID to a specific field

```python
import pybes3.identifier as p3id

# get TOF part number
tof_part = p3id.tof_id_to_part(tof_digi["m_intId"])

# get EMC theta number
emc_theta = p3id.emc_id_to_theta(emc_digi["m_intId"])

# get detector gid from electronics ID
tof_gid = p3id.tof_id_to_gid(tof_digi["m_intId"])
```

See the [Identifier API](../api/pybes3.identifier.md) for all available methods.

## Digi-ID calculation

To compute `m_intId` from geometry numbers, use `get_xxx_id` methods (where `xxx` is the detector name: `cgem`, `mdc`, `tof`, `emc`, `muc`):

```python
import pybes3.identifier as p3id

# get TOF digi geometry numbers
part = tof_id["part"]
layer_or_module = tof_id["layer_or_module"]
phi_or_strip = tof_id["phi_or_strip"]
end = tof_id["end"]

# calculate TOF digi ID
tof_int_id = p3id.get_tof_id(part, layer_or_module, phi_or_strip, end)
```

!!! info
    `pybes3` uses a different convention for the TOF `part` number:

    - `0`, `1`, `2` for scintillator endcap 0, barrel, and endcap 1
    - `3`, `4` for MRPC endcap 0 and endcap 1

    With this convention, TOF ID information can be decoded into 4 fields: `part`, `layer_or_module`, `phi_or_strip`, and `end`.
