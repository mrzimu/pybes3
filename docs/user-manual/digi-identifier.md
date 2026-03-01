# Digi Identifier

When reading `TDigiEvent`, the `m_intId` field in `mdc`, `tof`, `emc`, `muc`, and `cgem` branches represents the electronics readout ID (TEID), also known as `Identifier` in `BOSS`. `pybes3` provides methods to parse and calculate the digi ID for each detector.

## Digi array parsing

!!! info
    Currently, only MDC and EMC full digi parsing is supported. Support for other detectors is under development. For unsupported detectors, use the [standalone digi ID parsing methods](#standalone-digi-id-parsing).


```python
import pybes3 as p3
import uproot

# read raw digi array
mdc_digi = uproot.open("test.rtraw")["Event/TDigiEvent/m_mdcDigiCol"].array()

# parse whole digi array
mdc_digi = p3.parse_mdc_digi(mdc_digi)
```

## Standalone digi-ID parsing

When full digi array parsing is not necessary or not yet supported, use `parse_xxx_digi_id` methods (where `xxx` is the detector name: `cgem`, `mdc`, `tof`, `emc`, `muc`) to parse only the digi ID:

```python
# read raw digi array
tof_digi = uproot.open("test.rtraw")["Event/TDigiEvent/m_tofDigiCol"].array()
emc_digi = uproot.open("test.rtraw")["Event/TDigiEvent/m_emcDigiCol"].array()

# parse digi ID
tof_digi_id = p3.parse_tof_digi_id(tof_digi["m_intId"])
emc_digi_id = p3.parse_emc_digi_id(emc_digi["m_intId"])
```

!!! info
    As `pybes3.detectors.geometry` continues to develop, the `parse_xxx_digi_id` methods will be updated to return additional fields.

## Convert digi ID to a specific field

```python
import pybes3.detectors.digi_id as digi_id

# get TOF part number
tof_part = digi_id.tof_id_to_part(tof_digi["m_intId"])

# get EMC theta number
emc_theta = digi_id.emc_id_to_theta(emc_digi["m_intId"])
```

See the [Digi Identifier API](../api/pybes3.detectors.md#digi-identifier) for all available methods.

## Digi-ID calculation

To compute `m_intId` from geometry numbers, use `get_xxx_digi_id` methods (where `xxx` is the detector name: `cgem`, `mdc`, `tof`, `emc`, `muc`):

```python
import pybes3.detectors as p3det

# get TOF digi geometry numbers
part = tof_digi_id["part"]
layer_or_module = tof_digi_id["layer_or_module"]
phi_or_strip = tof_digi_id["phi_or_strip"]
end = tof_digi_id["end"]

# calculate TOF digi ID
tof_digi_id = p3det.get_tof_digi_id(part, layer_or_module, phi_or_strip, end)
```

!!! info
    `pybes3` uses a different convention for the TOF `part` number:

    - `0`, `1`, `2` for scintillator endcap 0, barrel, and endcap 1
    - `3`, `4` for MRPC endcap 0 and endcap 1

    With this convention, TOF ID information can be decoded into 4 fields: `part`, `layer_or_module`, `phi_or_strip`, and `end`.
