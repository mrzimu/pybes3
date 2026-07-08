#include <TFile.h>
#include <TTree.h>
#include <cstdint>

#include <Identifier/CgemID.h>
#include <Identifier/TofID.h>

void write_tof_idx() {
    TTree t( "tof", "tof-idx" );
    uint16_t idx;
    uint8_t part;
    uint8_t layer_or_module;
    uint8_t phi_or_strip;

    t.Branch( "idx", &idx );
    t.Branch( "part", &part );
    t.Branch( "layer_or_module", &layer_or_module );
    t.Branch( "phi_or_strip", &phi_or_strip );

    idx = 0;

    // part=0, endcap0
    part = 0;
    for ( layer_or_module = 0; layer_or_module <= TofID::getLAYER_ENDCAP_MAX();
          layer_or_module++ )
    {
        for ( phi_or_strip = 0; phi_or_strip <= TofID::getPHI_ENDCAP_MAX(); phi_or_strip++ )
        {
            t.Fill();
            idx++;
        }
    }

    // part=1, barrel
    part = 1;
    for ( layer_or_module = 0; layer_or_module <= TofID::getLAYER_BARREL_MAX();
          layer_or_module++ )
    {
        for ( phi_or_strip = 0; phi_or_strip <= TofID::getPHI_BARREL_MAX(); phi_or_strip++ )
        {
            t.Fill();
            idx++;
        }
    }

    // part=2, endcap1
    part = 2;
    for ( layer_or_module = 0; layer_or_module <= TofID::getLAYER_ENDCAP_MAX();
          layer_or_module++ )
    {
        for ( phi_or_strip = 0; phi_or_strip <= TofID::getPHI_ENDCAP_MAX(); phi_or_strip++ )
        {
            t.Fill();
            idx++;
        }
    }

    // part=3, MRPC endcap0
    part = 3;
    for ( layer_or_module = 0; layer_or_module <= TofID::getMODULE_MRPC_MAX();
          layer_or_module++ )
    {
        for ( phi_or_strip = 0; phi_or_strip <= TofID::getSTRIP_MRPC_MAX(); phi_or_strip++ )
        {
            t.Fill();
            idx++;
        }
    }

    // part=4, MRPC endcap1
    part = 4;
    for ( layer_or_module = 0; layer_or_module <= TofID::getMODULE_MRPC_MAX();
          layer_or_module++ )
    {
        for ( phi_or_strip = 0; phi_or_strip <= TofID::getSTRIP_MRPC_MAX(); phi_or_strip++ )
        {
            t.Fill();
            idx++;
        }
    }

    t.Write();
}

void write_cgem_idx() {
    TTree t( "cgem", "cgem-idx" );
    uint16_t idx;
    uint16_t layer;
    uint16_t sheet;
    uint8_t strip_type;
    uint16_t strip;

    t.Branch( "idx", &idx );
    t.Branch( "layer", &layer );
    t.Branch( "sheet", &sheet );
    t.Branch( "strip_type", &strip_type );
    t.Branch( "strip", &strip );

    idx = 0;

    // layer 0
    layer = 0;
    sheet = 0;

    for ( strip_type = 0; strip_type < 2; strip_type++ )
    {
        auto max_strip = strip_type == CgemID::getXSTRIP_TYPE()
                             ? CgemID::getXSTRIP_MAX( layer )
                             : CgemID::getVSTRIP_MAX( layer );

        for ( strip = 0; strip < max_strip; strip++ )
        {
            t.Fill();
            idx++;
        }
    }

    // layer 1, 2
    for ( layer = 1; layer < 3; layer++ )
    {
        for ( sheet = 0; sheet < 2; sheet++ )
        {
            for ( strip_type = 0; strip_type < 2; strip_type++ )
            {
                auto max_strip = strip_type == CgemID::getXSTRIP_TYPE()
                                     ? CgemID::getXSTRIP_MAX( layer )
                                     : CgemID::getVSTRIP_MAX( layer );

                for ( strip = 0; strip < max_strip; strip++ )
                {
                    t.Fill();
                    idx++;
                }
            }
        }
    }

    t.Write();
}

int main() {
    TFile f( "ref-idx.root", "RECREATE" );

    write_tof_idx();
    write_cgem_idx();

    f.Close();
}
