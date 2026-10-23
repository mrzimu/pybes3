# pybes3

## IO

```{eval-rst}
.. autofunction:: pybes3.open

.. autofunction:: pybes3.concatenate

.. autofunction:: pybes3.open_raw

.. autofunction:: pybes3.concatenate_raw
```

## Detectors

```{eval-rst}
.. autofunction:: pybes3.cgem_gid_to_is_vstrip

.. autofunction:: pybes3.cgem_gid_to_is_xstrip

.. autofunction:: pybes3.cgem_gid_to_layer

.. autofunction:: pybes3.cgem_gid_to_sheet

.. autofunction:: pybes3.cgem_gid_to_strip

.. autofunction:: pybes3.cgem_gid_to_strip_type

.. autofunction:: pybes3.get_cgem_gid

.. autofunction:: pybes3.parse_cgem_gid

.. autofunction:: pybes3.get_mdc_geom_table

.. autofunction:: pybes3.get_mdc_gid

.. autofunction:: pybes3.get_mdc_wire_position

.. autofunction:: pybes3.mdc_adc_to_charge

.. autofunction:: pybes3.mdc_gid_to_east_x

.. autofunction:: pybes3.mdc_gid_to_east_y

.. autofunction:: pybes3.mdc_gid_to_east_z

.. autofunction:: pybes3.mdc_gid_to_is_stereo

.. autofunction:: pybes3.mdc_gid_to_layer

.. autofunction:: pybes3.mdc_gid_to_stereo

.. autofunction:: pybes3.mdc_gid_to_superlayer

.. autofunction:: pybes3.mdc_gid_to_west_x

.. autofunction:: pybes3.mdc_gid_to_west_y

.. autofunction:: pybes3.mdc_gid_to_west_z

.. autofunction:: pybes3.mdc_gid_to_wire

.. autofunction:: pybes3.mdc_gid_z_to_x

.. autofunction:: pybes3.mdc_gid_z_to_y

.. autofunction:: pybes3.mdc_layer_to_is_stereo

.. autofunction:: pybes3.mdc_layer_to_superlayer

.. autofunction:: pybes3.mdc_tdc_to_time

.. autofunction:: pybes3.parse_mdc_gid

.. autofunction:: pybes3.get_tof_geom_table

.. autofunction:: pybes3.get_tof_gid

.. autofunction:: pybes3.parse_tof_gid

.. autofunction:: pybes3.parse_tof_hit_status

.. autofunction:: pybes3.tof_adc_to_charge

.. autofunction:: pybes3.tof_gid_to_layer_or_module

.. autofunction:: pybes3.tof_gid_to_part

.. autofunction:: pybes3.tof_gid_to_phi_or_strip

.. autofunction:: pybes3.tof_gid_to_point_x

.. autofunction:: pybes3.tof_gid_to_point_y

.. autofunction:: pybes3.tof_gid_to_point_z

.. autofunction:: pybes3.tof_hit_status_id_to_gid

.. autofunction:: pybes3.tof_hit_status_to_is_barrel

.. autofunction:: pybes3.tof_hit_status_to_is_cluster

.. autofunction:: pybes3.tof_hit_status_to_is_counter

.. autofunction:: pybes3.tof_hit_status_to_is_east

.. autofunction:: pybes3.tof_hit_status_to_is_mrpc

.. autofunction:: pybes3.tof_hit_status_to_is_multihit

.. autofunction:: pybes3.tof_hit_status_to_is_overflow

.. autofunction:: pybes3.tof_hit_status_to_is_raw

.. autofunction:: pybes3.tof_hit_status_to_is_readout

.. autofunction:: pybes3.tof_hit_status_to_layer

.. autofunction:: pybes3.tof_hit_status_to_n_counter

.. autofunction:: pybes3.tof_hit_status_to_n_east

.. autofunction:: pybes3.tof_hit_status_to_n_west

.. autofunction:: pybes3.tof_tdc_to_time

.. autofunction:: pybes3.emc_adc_to_charge

.. autofunction:: pybes3.emc_gid_to_center_x

.. autofunction:: pybes3.emc_gid_to_center_y

.. autofunction:: pybes3.emc_gid_to_center_z

.. autofunction:: pybes3.emc_gid_to_front_center_x

.. autofunction:: pybes3.emc_gid_to_front_center_y

.. autofunction:: pybes3.emc_gid_to_front_center_z

.. autofunction:: pybes3.emc_gid_to_part

.. autofunction:: pybes3.emc_gid_to_phi

.. autofunction:: pybes3.emc_gid_to_point_x

.. autofunction:: pybes3.emc_gid_to_point_y

.. autofunction:: pybes3.emc_gid_to_point_z

.. autofunction:: pybes3.emc_gid_to_theta

.. autofunction:: pybes3.emc_tdc_to_time

.. autofunction:: pybes3.get_emc_crystal_position

.. autofunction:: pybes3.get_emc_geom_table

.. autofunction:: pybes3.get_emc_gid

.. autofunction:: pybes3.parse_emc_gid

.. autofunction:: pybes3.get_muc_geom_table

.. autofunction:: pybes3.get_muc_gid

.. autofunction:: pybes3.muc_gid_to_center_x

.. autofunction:: pybes3.muc_gid_to_center_y

.. autofunction:: pybes3.muc_gid_to_center_z

.. autofunction:: pybes3.muc_gid_to_dx

.. autofunction:: pybes3.muc_gid_to_dy

.. autofunction:: pybes3.muc_gid_to_dz

.. autofunction:: pybes3.muc_gid_to_layer

.. autofunction:: pybes3.muc_gid_to_part

.. autofunction:: pybes3.muc_gid_to_point_x

.. autofunction:: pybes3.muc_gid_to_point_y

.. autofunction:: pybes3.muc_gid_to_point_z

.. autofunction:: pybes3.muc_gid_to_segment

.. autofunction:: pybes3.muc_gid_to_strip

.. autofunction:: pybes3.parse_muc_gid
```

## Helix

```{eval-rst}
.. autoclass:: pybes3.HelixObject
   :members:

.. autofunction:: pybes3.dr_phi0_to_x

.. autofunction:: pybes3.dr_phi0_to_y

.. autofunction:: pybes3.helix_awk

.. autofunction:: pybes3.helix_obj

.. autofunction:: pybes3.kappa_to_charge

.. autofunction:: pybes3.kappa_to_pt

.. autofunction:: pybes3.kappa_to_radius

.. autofunction:: pybes3.phi0_to_phi
```
