# Digi Identifier

When reading `TDigiEvent`, the `m_intId` field in `mdc`, `tof`, `emc`, `muc`, `cgem` branches are the electronics readout id (TEID), also known as `Identifier` in `BOSS`. `pybes3` provides methods to parse and calculate the digi ID for each detector.

## Digi array parsing

!!! info
    By so far, only MDC and EMC digi parsing is supported. Whole digi parsing for other detectors is still under development. If you need to parse digi ID for other detectors, use the [standalone digi ID parsing methods](#standalone-digi-id-parsing).


```python
import pybes3 as p3

# read raw digi array
mdc_digi = p3.open("test.rtraw")["Event/TDigiEvent/m_mdcDigiCol"].array()

# parse whole digi array
mdc_digi = p3.parse_mdc_digi(mdc_digi)
```

## Standalone digi-ID parsing

When parsing whole digi array is not necesarry/supported, use `parse_xxx_digi_id` methods where `xxx` is the detector name (`cgem`, `mdc`, `tof`, `emc`, `muc`) to parse only the digi ID:

```python
# read raw digi array
tof_digi = p3.open("test.rtraw")["Event/TDigiEvent/m_tofDigiCol"].array()
emc_digi = p3.open("test.rtraw")["Event/TDigiEvent/m_emcDigiCol"].array()

# parse digi ID
tof_digi_id = p3.parse_tof_digi_id(tof_digi["m_intId"])
emc_digi_id = p3.parse_emc_digi_id(emc_digi["m_intId"])
```

!!! info
    As the development of `pybes3.detectors.geometry`, the `parse_xxx_digi_id` methods will be updated to return more fields.

## Convert digi ID to specific field

```python
import pybes3.detectors.digi_id as digi_id

# get TOF part number
tof_part = digi_id.tof_id_to_part(tof_digi["m_intId"])

# get EMC theta number
emc_theta = digi_id.emc_id_to_theta(emc_digi["m_intId"])
```

See [Digi Identify API](../../api/pybes3.detectors/#digi-identify) for all available methods.

## Digi-ID calculation

To calculate `m_intId` of digis, use `get_xxx_digi_id` methods where `xxx` is the detector name (`cgem`, `mdc`, `tof`, `emc`, `muc`):

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
    `pybes3` uses different convention for TOF `part` number:

    - `0,1,2` for scintillator endcap0, barrel, endcap1
    - `3,4` for MRPC endcap0, endcap1.
    
    In this case, TOF ID information can be decoded to 4 fields: `part`, `layer_or_module`, `phi_or_strip`, `end`.
