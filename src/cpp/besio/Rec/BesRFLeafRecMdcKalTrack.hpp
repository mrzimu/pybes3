#pragma once

#include "RootEventData/TRecMdcKalTrack.h"
#include "RootEventData/TRecTrackEvent.h"

#include "../BesEventModel.hh"
#include "../BesRootFieldLeaf.hpp"
#include "../Utils.hh"

using RecMdcKalTrackRecord =
    RecordBuilder<RaggedItemField<0, int>,                 // trackId
                  RaggedArrayField<1, 5, double>,          // mass
                  RaggedArrayField<2, 5, double>,          // path
                  RaggedArrayField<3, 5, double>,          // tof
                  RaggedArrayField<4, 5, double>,          // fiTerm
                  RaggedArrayField<5, 5, double>,          // pathSM
                  RaggedArrayField<6, 5, int>,             // nhits
                  RaggedArrayField<7, 5, int>,             // nlayer
                  RaggedArrayArrayField<8, 5, 2, int>,     // stat
                  RaggedArrayArrayField<9, 5, 2, double>,  // chi2
                  RaggedArrayArrayField<10, 5, 2, int>,    // ndof
                  RaggedArrayField<11, 5, int>,            // nSegs
                  RaggedArrayField<12, 3, double>,         // poca
                  RaggedArrayField<13, 3, double>,         // poca_e
                  RaggedArrayField<14, 3, double>,         // poca_mu
                  RaggedArrayField<15, 3, double>,         // poca_k
                  RaggedArrayField<16, 3, double>,         // poca_p
                  RaggedArrayField<17, 3, double>,         // lpoint
                  RaggedArrayField<18, 3, double>,         // lpoint_e
                  RaggedArrayField<19, 3, double>,         // lpoint_mu
                  RaggedArrayField<20, 3, double>,         // lpoint_k
                  RaggedArrayField<21, 3, double>,         // lpoint_p
                  RaggedArrayField<22, 3, double>,         // lpivot
                  RaggedArrayField<23, 3, double>,         // lpivot_e
                  RaggedArrayField<24, 3, double>,         // lpivot_mu
                  RaggedArrayField<25, 3, double>,         // lpivot_k
                  RaggedArrayField<26, 3, double>,         // lpivot_p
                  RaggedArrayField<27, 5, double>,         // zhelix
                  RaggedArrayArrayField<28, 5, 5, double>, // zerror
                  RaggedArrayField<29, 5, double>,         // zhelix_e
                  RaggedArrayArrayField<30, 5, 5, double>, // zerror_e
                  RaggedArrayField<31, 5, double>,         // zhelix_mu
                  RaggedArrayArrayField<32, 5, 5, double>, // zerror_mu
                  RaggedArrayField<33, 5, double>,         // zhelix_k
                  RaggedArrayArrayField<34, 5, 5, double>, // zerror_k
                  RaggedArrayField<35, 5, double>,         // zhelix_p
                  RaggedArrayArrayField<36, 5, 5, double>, // zerror_p
                  RaggedArrayField<37, 5, double>,         // fhelix
                  RaggedArrayArrayField<38, 5, 5, double>, // ferror
                  RaggedArrayField<39, 5, double>,         // fhelix_e
                  RaggedArrayArrayField<40, 5, 5, double>, // ferror_e
                  RaggedArrayField<41, 5, double>,         // fhelix_mu
                  RaggedArrayArrayField<42, 5, 5, double>, // ferror_mu
                  RaggedArrayField<43, 5, double>,         // fhelix_k
                  RaggedArrayArrayField<44, 5, 5, double>, // ferror_k
                  RaggedArrayField<45, 5, double>,         // fhelix_p
                  RaggedArrayArrayField<46, 5, 5, double>, // ferror_p
                  RaggedArrayField<47, 5, double>,         // lhelix
                  RaggedArrayArrayField<48, 5, 5, double>, // lerror
                  RaggedArrayField<49, 5, double>,         // lhelix_e
                  RaggedArrayArrayField<50, 5, 5, double>, // lerror_e
                  RaggedArrayField<51, 5, double>,         // lhelix_mu
                  RaggedArrayArrayField<52, 5, 5, double>, // lerror_mu
                  RaggedArrayField<53, 5, double>,         // lhelix_k
                  RaggedArrayArrayField<54, 5, 5, double>, // lerror_k
                  RaggedArrayField<55, 5, double>,         // lhelix_p
                  RaggedArrayArrayField<56, 5, 5, double>, // lerror_p
                  RaggedArrayField<57, 5, double>,         // thelix
                  RaggedArrayField<58, 15, double>         // terror
                  >;

const FieldMap field_map_rec_mdckaltrack = {
    { 0, BesFieldNames::Rec::MdcKalTrack::trackId },
    { 1, BesFieldNames::Rec::MdcKalTrack::mass },
    { 2, BesFieldNames::Rec::MdcKalTrack::path },
    { 3, BesFieldNames::Rec::MdcKalTrack::tof },
    { 4, BesFieldNames::Rec::MdcKalTrack::fiTerm },
    { 5, BesFieldNames::Rec::MdcKalTrack::pathSM },
    { 6, BesFieldNames::Rec::MdcKalTrack::nhits },
    { 7, BesFieldNames::Rec::MdcKalTrack::nlayer },
    { 8, BesFieldNames::Rec::MdcKalTrack::stat },
    { 9, BesFieldNames::Rec::MdcKalTrack::chi2 },
    { 10, BesFieldNames::Rec::MdcKalTrack::ndof },
    { 11, BesFieldNames::Rec::MdcKalTrack::nSegs },
    { 12, BesFieldNames::Rec::MdcKalTrack::poca },
    { 13, BesFieldNames::Rec::MdcKalTrack::poca_e },
    { 14, BesFieldNames::Rec::MdcKalTrack::poca_mu },
    { 15, BesFieldNames::Rec::MdcKalTrack::poca_k },
    { 16, BesFieldNames::Rec::MdcKalTrack::poca_p },
    { 17, BesFieldNames::Rec::MdcKalTrack::lpoint },
    { 18, BesFieldNames::Rec::MdcKalTrack::lpoint_e },
    { 19, BesFieldNames::Rec::MdcKalTrack::lpoint_mu },
    { 20, BesFieldNames::Rec::MdcKalTrack::lpoint_k },
    { 21, BesFieldNames::Rec::MdcKalTrack::lpoint_p },
    { 22, BesFieldNames::Rec::MdcKalTrack::lpivot },
    { 23, BesFieldNames::Rec::MdcKalTrack::lpivot_e },
    { 24, BesFieldNames::Rec::MdcKalTrack::lpivot_mu },
    { 25, BesFieldNames::Rec::MdcKalTrack::lpivot_k },
    { 26, BesFieldNames::Rec::MdcKalTrack::lpivot_p },
    { 27, BesFieldNames::Rec::MdcKalTrack::zhelix },
    { 28, BesFieldNames::Rec::MdcKalTrack::zerror },
    { 29, BesFieldNames::Rec::MdcKalTrack::zhelix_e },
    { 30, BesFieldNames::Rec::MdcKalTrack::zerror_e },
    { 31, BesFieldNames::Rec::MdcKalTrack::zhelix_mu },
    { 32, BesFieldNames::Rec::MdcKalTrack::zerror_mu },
    { 33, BesFieldNames::Rec::MdcKalTrack::zhelix_k },
    { 34, BesFieldNames::Rec::MdcKalTrack::zerror_k },
    { 35, BesFieldNames::Rec::MdcKalTrack::zhelix_p },
    { 36, BesFieldNames::Rec::MdcKalTrack::zerror_p },
    { 37, BesFieldNames::Rec::MdcKalTrack::fhelix },
    { 38, BesFieldNames::Rec::MdcKalTrack::ferror },
    { 39, BesFieldNames::Rec::MdcKalTrack::fhelix_e },
    { 40, BesFieldNames::Rec::MdcKalTrack::ferror_e },
    { 41, BesFieldNames::Rec::MdcKalTrack::fhelix_mu },
    { 42, BesFieldNames::Rec::MdcKalTrack::ferror_mu },
    { 43, BesFieldNames::Rec::MdcKalTrack::fhelix_k },
    { 44, BesFieldNames::Rec::MdcKalTrack::ferror_k },
    { 45, BesFieldNames::Rec::MdcKalTrack::fhelix_p },
    { 46, BesFieldNames::Rec::MdcKalTrack::ferror_p },
    { 47, BesFieldNames::Rec::MdcKalTrack::lhelix },
    { 48, BesFieldNames::Rec::MdcKalTrack::lerror },
    { 49, BesFieldNames::Rec::MdcKalTrack::lhelix_e },
    { 50, BesFieldNames::Rec::MdcKalTrack::lerror_e },
    { 51, BesFieldNames::Rec::MdcKalTrack::lhelix_mu },
    { 52, BesFieldNames::Rec::MdcKalTrack::lerror_mu },
    { 53, BesFieldNames::Rec::MdcKalTrack::lhelix_k },
    { 54, BesFieldNames::Rec::MdcKalTrack::lerror_k },
    { 55, BesFieldNames::Rec::MdcKalTrack::lhelix_p },
    { 56, BesFieldNames::Rec::MdcKalTrack::lerror_p },
    { 57, BesFieldNames::Rec::MdcKalTrack::thelix },
    { 58, BesFieldNames::Rec::MdcKalTrack::terror },
};

class BesRFLeafRecMdcKalTrack : public BesRootFieldLeaf<TRecTrackEvent, RecMdcKalTrackRecord> {
  public:
    BesRFLeafRecMdcKalTrack( TRecTrackEvent* obj )
        : BesRootFieldLeaf<TRecTrackEvent, RecMdcKalTrackRecord>(
              obj, BesFieldNames::Rec::MdcKalTrack::rpath, field_map_rec_mdckaltrack ) {}

    void fill() {
        auto& trackId   = m_builder.content<0>().begin_list();
        auto& mass      = m_builder.content<1>().begin_list();
        auto& path      = m_builder.content<2>().begin_list();
        auto& tof       = m_builder.content<3>().begin_list();
        auto& fiTerm    = m_builder.content<4>().begin_list();
        auto& pathSM    = m_builder.content<5>().begin_list();
        auto& nhits     = m_builder.content<6>().begin_list();
        auto& nlayer    = m_builder.content<7>().begin_list();
        auto& stat      = m_builder.content<8>().begin_list();
        auto& chi2      = m_builder.content<9>().begin_list();
        auto& ndof      = m_builder.content<10>().begin_list();
        auto& nSegs     = m_builder.content<11>().begin_list();
        auto& poca      = m_builder.content<12>().begin_list();
        auto& poca_e    = m_builder.content<13>().begin_list();
        auto& poca_mu   = m_builder.content<14>().begin_list();
        auto& poca_k    = m_builder.content<15>().begin_list();
        auto& poca_p    = m_builder.content<16>().begin_list();
        auto& lpoint    = m_builder.content<17>().begin_list();
        auto& lpoint_e  = m_builder.content<18>().begin_list();
        auto& lpoint_mu = m_builder.content<19>().begin_list();
        auto& lpoint_k  = m_builder.content<20>().begin_list();
        auto& lpoint_p  = m_builder.content<21>().begin_list();
        auto& lpivot    = m_builder.content<22>().begin_list();
        auto& lpivot_e  = m_builder.content<23>().begin_list();
        auto& lpivot_mu = m_builder.content<24>().begin_list();
        auto& lpivot_k  = m_builder.content<25>().begin_list();
        auto& lpivot_p  = m_builder.content<26>().begin_list();
        auto& zhelix    = m_builder.content<27>().begin_list();
        auto& zerror    = m_builder.content<28>().begin_list();
        auto& zhelix_e  = m_builder.content<29>().begin_list();
        auto& zerror_e  = m_builder.content<30>().begin_list();
        auto& zhelix_mu = m_builder.content<31>().begin_list();
        auto& zerror_mu = m_builder.content<32>().begin_list();
        auto& zhelix_k  = m_builder.content<33>().begin_list();
        auto& zerror_k  = m_builder.content<34>().begin_list();
        auto& zhelix_p  = m_builder.content<35>().begin_list();
        auto& zerror_p  = m_builder.content<36>().begin_list();
        auto& fhelix    = m_builder.content<37>().begin_list();
        auto& ferror    = m_builder.content<38>().begin_list();
        auto& fhelix_e  = m_builder.content<39>().begin_list();
        auto& ferror_e  = m_builder.content<40>().begin_list();
        auto& fhelix_mu = m_builder.content<41>().begin_list();
        auto& ferror_mu = m_builder.content<42>().begin_list();
        auto& fhelix_k  = m_builder.content<43>().begin_list();
        auto& ferror_k  = m_builder.content<44>().begin_list();
        auto& fhelix_p  = m_builder.content<45>().begin_list();
        auto& ferror_p  = m_builder.content<46>().begin_list();
        auto& lhelix    = m_builder.content<47>().begin_list();
        auto& lerror    = m_builder.content<48>().begin_list();
        auto& lhelix_e  = m_builder.content<49>().begin_list();
        auto& lerror_e  = m_builder.content<50>().begin_list();
        auto& lhelix_mu = m_builder.content<51>().begin_list();
        auto& lerror_mu = m_builder.content<52>().begin_list();
        auto& lhelix_k  = m_builder.content<53>().begin_list();
        auto& lerror_k  = m_builder.content<54>().begin_list();
        auto& lhelix_p  = m_builder.content<55>().begin_list();
        auto& lerror_p  = m_builder.content<56>().begin_list();
        auto& thelix    = m_builder.content<57>().begin_list();
        auto& terror    = m_builder.content<58>().begin_list();

        for ( auto tobj : *m_obj->getRecMdcKalTrackCol() )
        {
            TRecMdcKalTrack* obj = static_cast<TRecMdcKalTrack*>( tobj );

            trackId.append( obj->getTrackId() );

            auto& subpoca      = poca.begin_list();
            auto& subpoca_e    = poca_e.begin_list();
            auto& subpoca_mu   = poca_mu.begin_list();
            auto& subpoca_k    = poca_k.begin_list();
            auto& subpoca_p    = poca_p.begin_list();
            auto& sublpoint    = lpoint.begin_list();
            auto& sublpoint_e  = lpoint_e.begin_list();
            auto& sublpoint_mu = lpoint_mu.begin_list();
            auto& sublpoint_k  = lpoint_k.begin_list();
            auto& sublpoint_p  = lpoint_p.begin_list();
            auto& sublpivot    = lpivot.begin_list();
            auto& sublpivot_e  = lpivot_e.begin_list();
            auto& sublpivot_mu = lpivot_mu.begin_list();
            auto& sublpivot_k  = lpivot_k.begin_list();
            auto& sublpivot_p  = lpivot_p.begin_list();
            for ( int i = 0; i < 3; i++ )
            {
                subpoca.append( obj->getPoca( i ) );
                subpoca_e.append( obj->getPocaE( i ) );
                subpoca_mu.append( obj->getPocaMu( i ) );
                subpoca_k.append( obj->getPocaK( i ) );
                subpoca_p.append( obj->getPocaP( i ) );
                sublpoint.append( obj->getLPoint( i ) );
                sublpoint_e.append( obj->getLPointE( i ) );
                sublpoint_mu.append( obj->getLPointMu( i ) );
                sublpoint_k.append( obj->getLPointK( i ) );
                sublpoint_p.append( obj->getLPointP( i ) );
                sublpivot.append( obj->getLPivot( i ) );
                sublpivot_e.append( obj->getLPivotE( i ) );
                sublpivot_mu.append( obj->getLPivotMu( i ) );
                sublpivot_k.append( obj->getLPivotK( i ) );
                sublpivot_p.append( obj->getLPivotP( i ) );
            }
            poca.end_list();
            poca_e.end_list();
            poca_mu.end_list();
            poca_k.end_list();
            poca_p.end_list();
            lpoint.end_list();
            lpoint_e.end_list();
            lpoint_mu.end_list();
            lpoint_k.end_list();
            lpoint_p.end_list();
            lpivot.end_list();
            lpivot_e.end_list();
            lpivot_mu.end_list();
            lpivot_k.end_list();
            lpivot_p.end_list();

            auto& subterror = terror.begin_list();
            for ( int i = 0; i < 15; i++ ) { subterror.append( obj->getTError( i ) ); }
            terror.end_list();

            /* PID loop */
            auto& submass      = mass.begin_list();
            auto& subpath      = path.begin_list();
            auto& subtof       = tof.begin_list();
            auto& subfiTerm    = fiTerm.begin_list();
            auto& subpathSM    = pathSM.begin_list();
            auto& subnhits     = nhits.begin_list();
            auto& subnlayer    = nlayer.begin_list();
            auto& substat      = stat.begin_list();
            auto& subchi2      = chi2.begin_list();
            auto& subndof      = ndof.begin_list();
            auto& subnSegs     = nSegs.begin_list();
            auto& subzhelix    = zhelix.begin_list();
            auto& subzerror    = zerror.begin_list();
            auto& subzhelix_e  = zhelix_e.begin_list();
            auto& subzerror_e  = zerror_e.begin_list();
            auto& subzhelix_mu = zhelix_mu.begin_list();
            auto& subzerror_mu = zerror_mu.begin_list();
            auto& subzhelix_k  = zhelix_k.begin_list();
            auto& subzerror_k  = zerror_k.begin_list();
            auto& subzhelix_p  = zhelix_p.begin_list();
            auto& subzerror_p  = zerror_p.begin_list();
            auto& subfhelix    = fhelix.begin_list();
            auto& subferror    = ferror.begin_list();
            auto& subfhelix_e  = fhelix_e.begin_list();
            auto& subferror_e  = ferror_e.begin_list();
            auto& subfhelix_mu = fhelix_mu.begin_list();
            auto& subferror_mu = ferror_mu.begin_list();
            auto& subfhelix_k  = fhelix_k.begin_list();
            auto& subferror_k  = ferror_k.begin_list();
            auto& subfhelix_p  = fhelix_p.begin_list();
            auto& subferror_p  = ferror_p.begin_list();
            auto& sublhelix    = lhelix.begin_list();
            auto& sublerror    = lerror.begin_list();
            auto& sublhelix_e  = lhelix_e.begin_list();
            auto& sublerror_e  = lerror_e.begin_list();
            auto& sublhelix_mu = lhelix_mu.begin_list();
            auto& sublerror_mu = lerror_mu.begin_list();
            auto& sublhelix_k  = lhelix_k.begin_list();
            auto& sublerror_k  = lerror_k.begin_list();
            auto& sublhelix_p  = lhelix_p.begin_list();
            auto& sublerror_p  = lerror_p.begin_list();
            auto& subthelix    = thelix.begin_list();
            for ( int pid = 0; pid < 5; pid++ )
            {
                submass.append( obj->getMass( pid ) );
                subpath.append( obj->getLength( pid ) );
                subtof.append( obj->getTof( pid ) );
                subfiTerm.append( obj->getfiTerm( pid ) );
                subpathSM.append( obj->getPathSM( pid ) );
                subnhits.append( obj->getNhits( pid ) );
                subnlayer.append( obj->getNlayer( pid ) );

                auto& subsubstat = substat.begin_list();
                auto& subsubchi2 = subchi2.begin_list();
                auto& subsubndof = subndof.begin_list();
                for ( int i = 0; i < 2; i++ )
                {
                    subsubstat.append( obj->getStat( i, pid ) );
                    subsubchi2.append( obj->getChisq( i, pid ) );
                    subsubndof.append( obj->getNdf( i, pid ) );
                }
                substat.end_list();
                subchi2.end_list();
                subndof.end_list();

                subnSegs.append( obj->getNseg( pid ) );
                subzhelix.append( obj->getZHelix( pid ) );
                subzhelix_e.append( obj->getZHelixE( pid ) );
                subzhelix_mu.append( obj->getZHelixMu( pid ) );
                subzhelix_k.append( obj->getZHelixK( pid ) );
                subzhelix_p.append( obj->getZHelixP( pid ) );
                subfhelix.append( obj->getFHelix( pid ) );
                subfhelix_e.append( obj->getFHelixE( pid ) );
                subfhelix_mu.append( obj->getFHelixMu( pid ) );
                subfhelix_k.append( obj->getFHelixK( pid ) );
                subfhelix_p.append( obj->getFHelixP( pid ) );
                sublhelix.append( obj->getLHelix( pid ) );
                sublhelix_e.append( obj->getLHelixE( pid ) );
                sublhelix_mu.append( obj->getLHelixMu( pid ) );
                sublhelix_k.append( obj->getLHelixK( pid ) );
                sublhelix_p.append( obj->getLHelixP( pid ) );
                subthelix.append( obj->getTHelix( pid ) );

                auto& subsubzerror    = subzerror.begin_list();
                auto& subsubzerror_e  = subzerror_e.begin_list();
                auto& subsubzerror_mu = subzerror_mu.begin_list();
                auto& subsubzerror_k  = subzerror_k.begin_list();
                auto& subsubzerror_p  = subzerror_p.begin_list();
                auto& subsubferror    = subferror.begin_list();
                auto& subsubferror_e  = subferror_e.begin_list();
                auto& subsubferror_mu = subferror_mu.begin_list();
                auto& subsubferror_k  = subferror_k.begin_list();
                auto& subsubferror_p  = subferror_p.begin_list();
                auto& subsublerror    = sublerror.begin_list();
                auto& subsublerror_e  = sublerror_e.begin_list();
                auto& subsublerror_mu = sublerror_mu.begin_list();
                auto& subsublerror_k  = sublerror_k.begin_list();
                auto& subsublerror_p  = sublerror_p.begin_list();
                for ( int i = 0; i < 5; i++ )
                {
                    subsubzerror.append( obj->getZError( pid, i ) );
                    subsubzerror_e.append( obj->getZErrorE( pid, i ) );
                    subsubzerror_mu.append( obj->getZErrorMu( pid, i ) );
                    subsubzerror_k.append( obj->getZErrorK( pid, i ) );
                    subsubzerror_p.append( obj->getZErrorP( pid, i ) );
                    subsubferror.append( obj->getFError( pid, i ) );
                    subsubferror_e.append( obj->getFErrorE( pid, i ) );
                    subsubferror_mu.append( obj->getFErrorMu( pid, i ) );
                    subsubferror_k.append( obj->getFErrorK( pid, i ) );
                    subsubferror_p.append( obj->getFErrorP( pid, i ) );
                    subsublerror.append( obj->getLError( pid, i ) );
                    subsublerror_e.append( obj->getLErrorE( pid, i ) );
                    subsublerror_mu.append( obj->getLErrorMu( pid, i ) );
                    subsublerror_k.append( obj->getLErrorK( pid, i ) );
                    subsublerror_p.append( obj->getLErrorP( pid, i ) );
                }
                subzerror.end_list();
                subzerror_e.end_list();
                subzerror_mu.end_list();
                subzerror_k.end_list();
                subzerror_p.end_list();
                subferror.end_list();
                subferror_e.end_list();
                subferror_mu.end_list();
                subferror_k.end_list();
                subferror_p.end_list();
                sublerror.end_list();
                sublerror_e.end_list();
                sublerror_mu.end_list();
                sublerror_k.end_list();
                sublerror_p.end_list();
            }
        }

        m_builder.content<0>().end_list();
        m_builder.content<1>().end_list();
        m_builder.content<2>().end_list();
        m_builder.content<3>().end_list();
        m_builder.content<4>().end_list();
        m_builder.content<5>().end_list();
        m_builder.content<6>().end_list();
        m_builder.content<7>().end_list();
        m_builder.content<8>().end_list();
        m_builder.content<9>().end_list();
        m_builder.content<10>().end_list();
        m_builder.content<11>().end_list();
        m_builder.content<12>().end_list();
        m_builder.content<13>().end_list();
        m_builder.content<14>().end_list();
        m_builder.content<15>().end_list();
        m_builder.content<16>().end_list();
        m_builder.content<17>().end_list();
        m_builder.content<18>().end_list();
        m_builder.content<19>().end_list();
        m_builder.content<20>().end_list();
        m_builder.content<21>().end_list();
        m_builder.content<22>().end_list();
        m_builder.content<23>().end_list();
        m_builder.content<24>().end_list();
        m_builder.content<25>().end_list();
        m_builder.content<26>().end_list();
        m_builder.content<27>().end_list();
        m_builder.content<28>().end_list();
        m_builder.content<29>().end_list();
        m_builder.content<30>().end_list();
        m_builder.content<31>().end_list();
        m_builder.content<32>().end_list();
        m_builder.content<33>().end_list();
        m_builder.content<34>().end_list();
        m_builder.content<35>().end_list();
        m_builder.content<36>().end_list();
        m_builder.content<37>().end_list();
        m_builder.content<38>().end_list();
        m_builder.content<39>().end_list();
        m_builder.content<40>().end_list();
        m_builder.content<41>().end_list();
        m_builder.content<42>().end_list();
        m_builder.content<43>().end_list();
        m_builder.content<44>().end_list();
        m_builder.content<45>().end_list();
        m_builder.content<46>().end_list();
        m_builder.content<47>().end_list();
        m_builder.content<48>().end_list();
        m_builder.content<49>().end_list();
        m_builder.content<50>().end_list();
        m_builder.content<51>().end_list();
        m_builder.content<52>().end_list();
        m_builder.content<53>().end_list();
        m_builder.content<54>().end_list();
        m_builder.content<55>().end_list();
        m_builder.content<56>().end_list();
        m_builder.content<57>().end_list();
        m_builder.content<58>().end_list();
    }
};
