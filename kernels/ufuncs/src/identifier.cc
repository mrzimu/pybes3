#include "mod.hh"
#include "ufunc.hh"

#include "identifier.hh"

namespace identifier {
    // ===========================================================================
    // declare_identifier – register all ufuncs into the module dict
    // ===========================================================================
    void declare_identifier( PyObject* d ) {
        if ( _import_array() < 0 ) return;
        if ( _import_umath() < 0 ) return;

        // ---- MDC ----
        decl_ufunc_11<              //
            check_mdc_id<uint32_t>, //
            check_mdc_id<uint64_t>, //
            check_mdc_id<int64_t>>  //
            ( d, "check_mdc_id" );

        decl_ufunc_11<                //
            mdc_id_to_wire<uint32_t>, //
            mdc_id_to_wire<uint64_t>, //
            mdc_id_to_wire<int64_t>>  //
            ( d, "mdc_id_to_wire" );

        decl_ufunc_11<                 //
            mdc_id_to_layer<uint32_t>, //
            mdc_id_to_layer<uint64_t>, //
            mdc_id_to_layer<int64_t>>  //
            ( d, "mdc_id_to_layer" );

        decl_ufunc_11<                     //
            mdc_id_to_is_stereo<uint32_t>, //
            mdc_id_to_is_stereo<uint64_t>, //
            mdc_id_to_is_stereo<int64_t>>  //
            ( d, "mdc_id_to_is_stereo" );

        decl_ufunc_31<            //
            get_mdc_id<uint32_t>, //
            get_mdc_id<uint64_t>, //
            get_mdc_id<int64_t>>  //
            ( d, "get_mdc_id" );

        // ---- TOF ----
        decl_ufunc_11<              //
            check_tof_id<uint32_t>, //
            check_tof_id<uint64_t>, //
            check_tof_id<int64_t>>  //
            ( d, "check_tof_id" );

        decl_ufunc_11<                //
            tof_id_to_part<uint32_t>, //
            tof_id_to_part<uint64_t>, //
            tof_id_to_part<int64_t>>  //
            ( d, "tof_id_to_part" );

        decl_ufunc_11<               //
            tof_id_to_end<uint32_t>, //
            tof_id_to_end<uint64_t>, //
            tof_id_to_end<int64_t>>  //
            ( d, "tof_id_to_end" );

        decl_ufunc_11<                              //
            _tof_id_to_layer_or_module_1<uint32_t>, //
            _tof_id_to_layer_or_module_1<uint64_t>, //
            _tof_id_to_layer_or_module_1<int64_t>>  //
            ( d, "_tof_id_to_layer_or_module_1" );

        decl_ufunc_21<                              //
            _tof_id_to_layer_or_module_2<uint32_t>, //
            _tof_id_to_layer_or_module_2<uint64_t>, //
            _tof_id_to_layer_or_module_2<int64_t>>  //
            ( d, "_tof_id_to_layer_or_module_2" );

        decl_ufunc_11<                           //
            _tof_id_to_phi_or_strip_1<uint32_t>, //
            _tof_id_to_phi_or_strip_1<uint64_t>, //
            _tof_id_to_phi_or_strip_1<int64_t>>  //
            ( d, "_tof_id_to_phi_or_strip_1" );

        decl_ufunc_21<                           //
            _tof_id_to_phi_or_strip_2<uint32_t>, //
            _tof_id_to_phi_or_strip_2<uint64_t>, //
            _tof_id_to_phi_or_strip_2<int64_t>>  //
            ( d, "_tof_id_to_phi_or_strip_2" );

        decl_ufunc_41<            //
            get_tof_id<uint32_t>, //
            get_tof_id<uint64_t>, //
            get_tof_id<int64_t>>  //
            ( d, "get_tof_id" );

        // ---- EMC ----
        decl_ufunc_11<              //
            check_emc_id<uint32_t>, //
            check_emc_id<uint64_t>, //
            check_emc_id<int64_t>>  //
            ( d, "check_emc_id" );

        decl_ufunc_11<                  //
            emc_id_to_module<uint32_t>, //
            emc_id_to_module<uint64_t>, //
            emc_id_to_module<int64_t>>  //
            ( d, "emc_id_to_module" );

        decl_ufunc_11<                 //
            emc_id_to_theta<uint32_t>, //
            emc_id_to_theta<uint64_t>, //
            emc_id_to_theta<int64_t>>  //
            ( d, "emc_id_to_theta" );

        decl_ufunc_11<               //
            emc_id_to_phi<uint32_t>, //
            emc_id_to_phi<uint64_t>, //
            emc_id_to_phi<int64_t>>  //
            ( d, "emc_id_to_phi" );

        decl_ufunc_31<            //
            get_emc_id<uint32_t>, //
            get_emc_id<uint64_t>, //
            get_emc_id<int64_t>>  //
            ( d, "get_emc_id" );

        // ---- MUC ----
        decl_ufunc_11<              //
            check_muc_id<uint32_t>, //
            check_muc_id<uint64_t>, //
            check_muc_id<int64_t>>  //
            ( d, "check_muc_id" );

        decl_ufunc_11<                //
            muc_id_to_part<uint32_t>, //
            muc_id_to_part<uint64_t>, //
            muc_id_to_part<int64_t>>  //
            ( d, "muc_id_to_part" );

        decl_ufunc_11<                   //
            muc_id_to_segment<uint32_t>, //
            muc_id_to_segment<uint64_t>, //
            muc_id_to_segment<int64_t>>  //
            ( d, "muc_id_to_segment" );

        decl_ufunc_11<                 //
            muc_id_to_layer<uint32_t>, //
            muc_id_to_layer<uint64_t>, //
            muc_id_to_layer<int64_t>>  //
            ( d, "muc_id_to_layer" );

        decl_ufunc_11<                   //
            muc_id_to_channel<uint32_t>, //
            muc_id_to_channel<uint64_t>, //
            muc_id_to_channel<int64_t>>  //
            ( d, "muc_id_to_channel" );

        decl_ufunc_41<            //
            get_muc_id<uint32_t>, //
            get_muc_id<uint64_t>, //
            get_muc_id<int64_t>>  //
            ( d, "get_muc_id" );

        // ---- CGEM ----
        decl_ufunc_11<               //
            check_cgem_id<uint32_t>, //
            check_cgem_id<uint64_t>, //
            check_cgem_id<int64_t>>  //
            ( d, "check_cgem_id" );

        decl_ufunc_11<                  //
            cgem_id_to_layer<uint32_t>, //
            cgem_id_to_layer<uint64_t>, //
            cgem_id_to_layer<int64_t>>  //
            ( d, "cgem_id_to_layer" );

        decl_ufunc_11<                  //
            cgem_id_to_sheet<uint32_t>, //
            cgem_id_to_sheet<uint64_t>, //
            cgem_id_to_sheet<int64_t>>  //
            ( d, "cgem_id_to_sheet" );

        decl_ufunc_11<                       //
            cgem_id_to_strip_type<uint32_t>, //
            cgem_id_to_strip_type<uint64_t>, //
            cgem_id_to_strip_type<int64_t>>  //
            ( d, "cgem_id_to_strip_type" );

        decl_ufunc_11<                  //
            cgem_id_to_strip<uint32_t>, //
            cgem_id_to_strip<uint64_t>, //
            cgem_id_to_strip<int64_t>>  //
            ( d, "cgem_id_to_strip" );

        decl_ufunc_41<             //
            get_cgem_id<uint32_t>, //
            get_cgem_id<uint64_t>, //
            get_cgem_id<int64_t>>  //
            ( d, "get_cgem_id" );
    }
} // namespace identifier
