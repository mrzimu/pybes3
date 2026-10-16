# pybes3.digi_id (deprecated)

:::{warning}
The `pybes3.digi_id` module is deprecated and will be removed in a future release. Use the `pybes3.identifier` module instead.
:::

## Parsing methods

These methods parse the given ID and return the corresponding components. They are useful for retrieving the components of an ID when you only have the ID itself.

```{eval-rst}
.. autofunction:: pybes3.digi_id.parse_mdc_digi

.. autofunction:: pybes3.digi_id.parse_emc_digi

.. autofunction:: pybes3.digi_id.parse_mdc_digi_id

.. autofunction:: pybes3.digi_id.parse_emc_digi_id

.. autofunction:: pybes3.digi_id.parse_tof_digi_id

.. autofunction:: pybes3.digi_id.parse_muc_digi_id

.. autofunction:: pybes3.digi_id.parse_cgem_digi_id
```

## MDC

```{eval-rst}
.. autofunction:: pybes3.digi_id.check_mdc_id

.. autofunction:: pybes3.digi_id.mdc_id_to_wire

.. autofunction:: pybes3.digi_id.mdc_id_to_layer

.. autofunction:: pybes3.digi_id.mdc_id_to_is_stereo

.. autofunction:: pybes3.digi_id.get_mdc_digi_id
```

## TOF

```{eval-rst}
.. autofunction:: pybes3.digi_id.check_tof_id

.. autofunction:: pybes3.digi_id.tof_id_to_part

.. autofunction:: pybes3.digi_id.tof_id_to_end

.. autofunction:: pybes3.digi_id.tof_id_to_layer_or_module

.. autofunction:: pybes3.digi_id.tof_id_to_phi_or_strip

.. autofunction:: pybes3.digi_id.get_tof_digi_id
```

## EMC

```{eval-rst}
.. autofunction:: pybes3.digi_id.check_emc_id

.. autofunction:: pybes3.digi_id.emc_id_to_module

.. autofunction:: pybes3.digi_id.emc_id_to_theta

.. autofunction:: pybes3.digi_id.emc_id_to_phi

.. autofunction:: pybes3.digi_id.get_emc_digi_id
```

## MUC

```{eval-rst}
.. autofunction:: pybes3.digi_id.check_muc_id

.. autofunction:: pybes3.digi_id.muc_id_to_part

.. autofunction:: pybes3.digi_id.muc_id_to_segment

.. autofunction:: pybes3.digi_id.muc_id_to_layer

.. autofunction:: pybes3.digi_id.muc_id_to_channel

.. autofunction:: pybes3.digi_id.get_muc_digi_id

.. autofunction:: pybes3.digi_id.muc_id_to_gap

.. autofunction:: pybes3.digi_id.muc_id_to_strip
```

## CGEM

```{eval-rst}
.. autofunction:: pybes3.digi_id.check_cgem_id

.. autofunction:: pybes3.digi_id.cgem_id_to_layer

.. autofunction:: pybes3.digi_id.cgem_id_to_sheet

.. autofunction:: pybes3.digi_id.cgem_id_to_strip_type

.. autofunction:: pybes3.digi_id.cgem_id_to_strip

.. autofunction:: pybes3.digi_id.get_cgem_digi_id
```
