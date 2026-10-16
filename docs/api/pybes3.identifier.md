# pybes3.identifier

## Parsing methods

These methods parse the given ID and return the corresponding components. They are useful for retrieving the components of an ID when you only have the ID itself.

```{eval-rst}
.. autofunction:: pybes3.identifier.parse_mdc_digi

.. autofunction:: pybes3.identifier.parse_tof_digi

.. autofunction:: pybes3.identifier.parse_emc_digi

.. autofunction:: pybes3.identifier.parse_cgem_digi

.. autofunction:: pybes3.identifier.parse_muc_digi

.. autofunction:: pybes3.identifier.parse_mdc_id

.. autofunction:: pybes3.identifier.parse_emc_id

.. autofunction:: pybes3.identifier.parse_tof_id

.. autofunction:: pybes3.identifier.parse_muc_id

.. autofunction:: pybes3.identifier.parse_cgem_id
```

## MDC

```{eval-rst}
.. autofunction:: pybes3.identifier.check_mdc_id

.. autofunction:: pybes3.identifier.mdc_id_to_gid

.. autofunction:: pybes3.identifier.mdc_id_to_wire

.. autofunction:: pybes3.identifier.mdc_id_to_layer

.. autofunction:: pybes3.identifier.mdc_id_to_is_stereo

.. autofunction:: pybes3.identifier.get_mdc_id
```

## TOF

```{eval-rst}
.. autofunction:: pybes3.identifier.check_tof_id

.. autofunction:: pybes3.identifier.tof_id_to_gid

.. autofunction:: pybes3.identifier.tof_id_to_part

.. autofunction:: pybes3.identifier.tof_id_to_end

.. autofunction:: pybes3.identifier.tof_id_to_layer_or_module

.. autofunction:: pybes3.identifier.tof_id_to_phi_or_strip

.. autofunction:: pybes3.identifier.get_tof_id
```

## EMC

```{eval-rst}
.. autofunction:: pybes3.identifier.check_emc_id

.. autofunction:: pybes3.identifier.emc_id_to_gid

.. autofunction:: pybes3.identifier.emc_id_to_module

.. autofunction:: pybes3.identifier.emc_id_to_theta

.. autofunction:: pybes3.identifier.emc_id_to_phi

.. autofunction:: pybes3.identifier.get_emc_id
```

## MUC

```{eval-rst}
.. autofunction:: pybes3.identifier.check_muc_id

.. autofunction:: pybes3.identifier.muc_id_to_part

.. autofunction:: pybes3.identifier.muc_id_to_segment

.. autofunction:: pybes3.identifier.muc_id_to_layer

.. autofunction:: pybes3.identifier.muc_id_to_channel

.. autofunction:: pybes3.identifier.get_muc_id

.. autofunction:: pybes3.identifier.muc_id_to_gap

.. autofunction:: pybes3.identifier.muc_id_to_strip
```

## CGEM

```{eval-rst}
.. autofunction:: pybes3.identifier.check_cgem_id

.. autofunction:: pybes3.identifier.cgem_id_to_gid

.. autofunction:: pybes3.identifier.cgem_id_to_layer

.. autofunction:: pybes3.identifier.cgem_id_to_sheet

.. autofunction:: pybes3.identifier.cgem_id_to_strip_type

.. autofunction:: pybes3.identifier.cgem_id_to_strip

.. autofunction:: pybes3.identifier.get_cgem_id
```
