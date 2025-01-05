#pragma once

#include <awkward/LayoutBuilder.h>
#include <cstddef>
#include <string>
#include <vector>

enum class SubEvtType { kHeader, kMc, kDigi, kDst, kRec };

using FieldMap = std::map<std::size_t, std::string>;

namespace BesFieldNames {
    using ConstStr    = const std::string;
    using ConstStrVec = const std::vector<std::string>;

    namespace EvtHeader {
        ConstStr rpath = "/Event/Header";

        ConstStr evtNo = "evtNo";
        ConstStr runNo = "runNo";
        ConstStr time  = "time";
        ConstStr tag   = "tag";
        ConstStr flag1 = "flag1";
        ConstStr flag2 = "flag2";
        ConstStr etsT1 = "etsT1";
        ConstStr etsT2 = "etsT2";

        ConstStrVec all = { evtNo, runNo, time, tag, flag1, flag2, etsT1, etsT2 };
    } // namespace EvtHeader

    namespace Mc {
        namespace Mdc {
            ConstStr rpath = "/Event/Mc/Mdc";

            ConstStr identify       = "identify";
            ConstStr trackIndex     = "trackIndex";
            ConstStr curTrkPID      = "curTrkPID";
            ConstStr isSecondary    = "isSecondary";
            ConstStr x              = "x";
            ConstStr y              = "y";
            ConstStr z              = "z";
            ConstStr px             = "px";
            ConstStr py             = "py";
            ConstStr pz             = "pz";
            ConstStr driftDistance  = "driftDistance";
            ConstStr depositEnergy  = "depositEnergy";
            ConstStr posFlag        = "posFlag";
            ConstStr flightLength   = "flightLength";
            ConstStr creatorProcess = "creatorProcess";
            ConstStr digiIndex      = "digiIndex";

            ConstStrVec all = { identify,
                                trackIndex,
                                curTrkPID,
                                isSecondary,
                                x,
                                y,
                                z,
                                px,
                                py,
                                pz,
                                driftDistance,
                                depositEnergy,
                                posFlag,
                                flightLength,
                                creatorProcess,
                                digiIndex };
        } // namespace Mdc

        namespace Emc {
            ConstStr rpath = "/Event/Mc/Emc";

            ConstStr identify      = "identify";
            ConstStr trackIndex    = "trackIndex";
            ConstStr hitEmc        = "hitEmc";
            ConstStr PDGCode       = "PDGCode";
            ConstStr PDGCharge     = "PDGCharge";
            ConstStr time          = "time";
            ConstStr x             = "x";
            ConstStr y             = "y";
            ConstStr z             = "z";
            ConstStr px            = "px";
            ConstStr py            = "py";
            ConstStr pz            = "pz";
            ConstStr depositEnergy = "depositEnergy";
            ConstStr hitMapId      = "hitMapId";
            ConstStr hitMapEnergy  = "hitMapEnergy";

            ConstStrVec all = {
                identify, trackIndex, hitEmc, PDGCode, PDGCharge,     time,     x,           y,
                z,        px,         py,     pz,      depositEnergy, hitMapId, hitMapEnergy };
        } // namespace Emc

        namespace Tof {
            ConstStr rpath = "/Event/Mc/Tof";

            ConstStr identify    = "identify";
            ConstStr trackIndex  = "trackIndex";
            ConstStr x           = "x";
            ConstStr y           = "y";
            ConstStr z           = "z";
            ConstStr px          = "px";
            ConstStr py          = "py";
            ConstStr pz          = "pz";
            ConstStr trackLength = "trackLength";
            ConstStr tof         = "tof";

            ConstStrVec all = { identify, trackIndex, x, y, z, px, py, pz, trackLength, tof };
        } // namespace Tof

        namespace Muc {
            ConstStr rpath = "/Event/Mc/Muc";

            ConstStr identify      = "identify";
            ConstStr trackIndex    = "trackIndex";
            ConstStr x             = "x";
            ConstStr y             = "y";
            ConstStr z             = "z";
            ConstStr px            = "px";
            ConstStr py            = "py";
            ConstStr pz            = "pz";
            ConstStr depositEnergy = "depositEnergy";

            ConstStrVec all = { identify, trackIndex, x, y, z, px, py, pz, depositEnergy };
        } // namespace Muc

        namespace McParticle {
            ConstStr rpath = "/Event/Mc/McParticle";

            ConstStr PDGId           = "PDGId";
            ConstStr trackIndex      = "trackIndex";
            ConstStr vertexIndex0    = "vertexIndex0";
            ConstStr vertexIndex1    = "vertexIndex1";
            ConstStr statusFlags     = "statusFlags";
            ConstStr motherIndex     = "motherIndex";
            ConstStr daughterIndexes = "daughterIndexes";
            ConstStr xInit           = "xInit";
            ConstStr yInit           = "yInit";
            ConstStr zInit           = "zInit";
            ConstStr tInit           = "tInit";
            ConstStr xFinal          = "xFinal";
            ConstStr yFinal          = "yFinal";
            ConstStr zFinal          = "zFinal";
            ConstStr tFinal          = "tFinal";
            ConstStr pxInit          = "pxInit";
            ConstStr pyInit          = "pyInit";
            ConstStr pzInit          = "pzInit";
            ConstStr eInit           = "eInit";

            ConstStrVec all = {
                PDGId,       trackIndex,      vertexIndex0, vertexIndex1, statusFlags,
                motherIndex, daughterIndexes, xInit,        yInit,        zInit,
                tInit,       xFinal,          yFinal,       zFinal,       tFinal,
                pxInit,      pyInit,          pzInit,       eInit };
        } // namespace McParticle

    } // namespace Mc

    namespace Dst {
        namespace Mdc {
            ConstStr rpath = "/Event/Dst/Mdc";

            ConstStr trackIndex = "trackIndex";
            ConstStr helix      = "helix";
            ConstStr helixErr   = "helixErr";
            ConstStr stat       = "stat";
            ConstStr chi2       = "chi2";
            ConstStr ndof       = "ndof";
            ConstStr nster      = "nster";
            ConstStr nlayer     = "nlayers";
            ConstStr firstLayer = "firstLayer";
            ConstStr lastLayer  = "lastLayer";

            ConstStrVec all = { trackIndex, helix, helixErr, stat,       chi2,
                                ndof,       nster, nlayer,   firstLayer, lastLayer };
        } // namespace Mdc

        namespace Emc {
            ConstStr rpath = "/Event/Dst/Emc";

            ConstStr trackIndex   = "trackIndex";
            ConstStr nHits        = "nHits";
            ConstStr status       = "status";
            ConstStr moduleId     = "module";
            ConstStr x            = "x";
            ConstStr y            = "y";
            ConstStr z            = "z";
            ConstStr dTheta       = "dTheta";
            ConstStr dPhi         = "dPhi";
            ConstStr energy       = "energy";
            ConstStr dE           = "dE";
            ConstStr eSeed        = "eSeed";
            ConstStr e3x3         = "e3x3";
            ConstStr e5x5         = "e5x5";
            ConstStr time         = "time";
            ConstStr secondMoment = "secondMoment";
            ConstStr latMoment    = "latMoment";
            ConstStr a20Moment    = "a20Moment";
            ConstStr a42Moment    = "a42Moment";
            ConstStr err          = "err";

            ConstStrVec all = { trackIndex, nHits,  status, moduleId,     x,         y,
                                z,          dTheta, dPhi,   energy,       dE,        eSeed,
                                e3x3,       e5x5,   time,   secondMoment, latMoment, a20Moment,
                                a42Moment,  err };
        } // namespace Emc

        namespace Tof {
            ConstStr rpath = "/Event/Dst/Tof";

            ConstStr trackIndex = "trackIndex";
            ConstStr inTrackId  = "inTrackId"; // Track ID from MDC / Shower ID from EMC.
            ConstStr tofId      = "tofId";
            ConstStr status     = "status";
            ConstStr path       = "path";
            ConstStr zrhit      = "zrhit";
            ConstStr ph         = "ph";
            ConstStr tof        = "tof";
            ConstStr beta       = "beta";
            ConstStr texp       = "texp";
            ConstStr toffset    = "toffset";
            ConstStr sigma      = "sigma";
            ConstStr quality    = "quality";
            ConstStr t0         = "t0";
            ConstStr t0Err      = "t0Err";
            ConstStr zErr       = "zErr";
            ConstStr phi        = "phi";
            ConstStr errphi     = "errphi";
            ConstStr energy     = "energy";
            ConstStr energyErr  = "energyErr";

            ConstStrVec all = { trackIndex, inTrackId, tofId, status,  path,   zrhit,    ph,
                                tof,        beta,      texp,  toffset, sigma,  quality,  t0,
                                t0Err,      zErr,      phi,   errphi,  energy, energyErr };
        } // namespace Tof

        namespace Muc {
            ConstStr rpath = "/Event/Dst/Muc";

            ConstStr trackIndex     = "trackIndex";
            ConstStr id             = "id";
            ConstStr status         = "status";
            ConstStr type           = "type";
            ConstStr startPart      = "startPart";
            ConstStr endPart        = "endPart";
            ConstStr brLastLayer    = "brLastLayer";
            ConstStr ecLastLayer    = "ecLastLayer";
            ConstStr nHits          = "nHits";
            ConstStr nLayers        = "nLayers";
            ConstStr maxHitsInLayer = "maxHitsInLayer";
            ConstStr depth          = "depth";
            ConstStr chi2           = "chi2";
            ConstStr dof            = "dof";
            ConstStr rms            = "rms";
            ConstStr x              = "x";
            ConstStr y              = "y";
            ConstStr z              = "z";
            ConstStr xSigma         = "xSigma";
            ConstStr ySigma         = "ySigma";
            ConstStr zSigma         = "zSigma";
            ConstStr px             = "px";
            ConstStr py             = "py";
            ConstStr pz             = "pz";
            ConstStr distance       = "distance";
            ConstStr deltaPhi       = "deltaPhi";
            ConstStr kalrechi2      = "kalrechi2";
            ConstStr kaldof         = "kaldof";
            ConstStr kalbrLastLayer = "kalbrLastLayer";
            ConstStr kalecLastLayer = "kalecLastLayer";

            ConstStrVec all = { trackIndex,
                                id,
                                status,
                                type,
                                startPart,
                                endPart,
                                brLastLayer,
                                ecLastLayer,
                                nHits,
                                nLayers,
                                maxHitsInLayer,
                                depth,
                                chi2,
                                dof,
                                rms,
                                x,
                                y,
                                z,
                                xSigma,
                                ySigma,
                                zSigma,
                                px,
                                py,
                                pz,
                                distance,
                                deltaPhi,
                                kalrechi2,
                                kaldof,
                                kalbrLastLayer,
                                kalecLastLayer };
        } // namespace Muc

        namespace Dedx {
            ConstStr rpath = "/Event/Dst/Dedx";

            ConstStr trackIndex = "trackIndex";
            ConstStr particleId = "particleId";
            ConstStr status     = "status";
            ConstStr trunc_alg  = "trunc_alg";
            ConstStr chiE       = "chiE";
            ConstStr chiMu      = "chiMu";
            ConstStr chiPi      = "chiPi";
            ConstStr chiK       = "chiK";
            ConstStr chiP       = "chiP";
            ConstStr nGoodHits  = "nGoodHits";
            ConstStr nTotalHits = "nTotalHits";
            ConstStr probPH     = "probPH";
            ConstStr normPH     = "normPH";
            ConstStr errorPH    = "errorPH";
            ConstStr twentyPH   = "twentyPH";

            ConstStrVec all = { trackIndex, particleId, status, trunc_alg, chiE,
                                chiMu,      chiPi,      chiK,   chiP,      nGoodHits,
                                nTotalHits, probPH,     normPH, errorPH,   twentyPH };

        } // namespace Dedx

        namespace Ext {
            ConstStr rpath = "/Event/Dst/Ext";

            ConstStr trackIndex         = "trackIndex";
            ConstStr Tof1X              = "Tof1X";
            ConstStr Tof1Y              = "Tof1Y";
            ConstStr Tof1Z              = "Tof1Z";
            ConstStr Tof1Px             = "Tof1Px";
            ConstStr Tof1Py             = "Tof1Py";
            ConstStr Tof1Pz             = "Tof1Pz";
            ConstStr Tof1VolumeName     = "Tof1VolumeName";
            ConstStr Tof1VolumeNumber   = "Tof1VolumeNumber";
            ConstStr Tof1               = "Tof1";
            ConstStr Tof1Path           = "Tof1Path";
            ConstStr Tof1PosSigmaAlongZ = "Tof1PosSigmaAlongZ";
            ConstStr Tof1PosSigmaAlongT = "Tof1PosSigmaAlongT";
            ConstStr Tof1PosSigmaAlongX = "Tof1PosSigmaAlongX";
            ConstStr Tof1PosSigmaAlongY = "Tof1PosSigmaAlongY";
            ConstStr Tof1ErrorMatrix    = "Tof1ErrorMatrix";

            ConstStr Tof2X              = "Tof2X";
            ConstStr Tof2Y              = "Tof2Y";
            ConstStr Tof2Z              = "Tof2Z";
            ConstStr Tof2Px             = "Tof2Px";
            ConstStr Tof2Py             = "Tof2Py";
            ConstStr Tof2Pz             = "Tof2Pz";
            ConstStr Tof2VolumeName     = "Tof2VolumeName";
            ConstStr Tof2VolumeNumber   = "Tof2VolumeNumber";
            ConstStr Tof2               = "Tof2";
            ConstStr Tof2Path           = "Tof2Path";
            ConstStr Tof2PosSigmaAlongZ = "Tof2PosSigmaAlongZ";
            ConstStr Tof2PosSigmaAlongT = "Tof2PosSigmaAlongT";
            ConstStr Tof2PosSigmaAlongX = "Tof2PosSigmaAlongX";
            ConstStr Tof2PosSigmaAlongY = "Tof2PosSigmaAlongY";
            ConstStr Tof2ErrorMatrix    = "Tof2ErrorMatrix";

            ConstStr EmcX                  = "EmcX";
            ConstStr EmcY                  = "EmcY";
            ConstStr EmcZ                  = "EmcZ";
            ConstStr EmcPx                 = "EmcPx";
            ConstStr EmcPy                 = "EmcPy";
            ConstStr EmcPz                 = "EmcPz";
            ConstStr EmcVolumeName         = "EmcVolumeName";
            ConstStr EmcVolumeNumber       = "EmcVolumeNumber";
            ConstStr EmcPosSigmaAlongTheta = "EmcPosSigmaAlongTheta";
            ConstStr EmcPosSigmaAlongPhi   = "EmcPosSigmaAlongPhi";
            ConstStr EmcErrorMatrix        = "EmcErrorMatrix";
            ConstStr EmcPath               = "EmcPath";

            ConstStr MucX              = "MucX";
            ConstStr MucY              = "MucY";
            ConstStr MucZ              = "MucZ";
            ConstStr MucPx             = "MucPx";
            ConstStr MucPy             = "MucPy";
            ConstStr MucPz             = "MucPz";
            ConstStr MucVolumeName     = "MucVolumeName";
            ConstStr MucVolumeNumber   = "MucVolumeNumber";
            ConstStr MucPosSigmaAlongZ = "MucPosSigmaAlongZ";
            ConstStr MucPosSigmaAlongT = "MucPosSigmaAlongT";
            ConstStr MucPosSigmaAlongX = "MucPosSigmaAlongX";
            ConstStr MucPosSigmaAlongY = "MucPosSigmaAlongY";
            ConstStr MucErrorMatrix    = "MucErrorMatrix";

            ConstStrVec all = { trackIndex,
                                Tof1X,
                                Tof1Y,
                                Tof1Z,
                                Tof1Px,
                                Tof1Py,
                                Tof1Pz,
                                Tof1VolumeName,
                                Tof1VolumeNumber,
                                Tof1,
                                Tof1Path,
                                Tof1PosSigmaAlongZ,
                                Tof1PosSigmaAlongT,
                                Tof1PosSigmaAlongX,
                                Tof1PosSigmaAlongY,
                                Tof1ErrorMatrix,
                                Tof2X,
                                Tof2Y,
                                Tof2Z,
                                Tof2Px,
                                Tof2Py,
                                Tof2Pz,
                                Tof2VolumeName,
                                Tof2VolumeNumber,
                                Tof2,
                                Tof2Path,
                                Tof2PosSigmaAlongZ,
                                Tof2PosSigmaAlongT,
                                Tof2PosSigmaAlongX,
                                Tof2PosSigmaAlongY,
                                Tof2ErrorMatrix,
                                EmcX,
                                EmcY,
                                EmcZ,
                                EmcPx,
                                EmcPy,
                                EmcPz,
                                EmcVolumeName,
                                EmcVolumeNumber,
                                EmcPosSigmaAlongTheta,
                                EmcPosSigmaAlongPhi,
                                EmcErrorMatrix,
                                EmcPath,
                                MucX,
                                MucY,
                                MucZ,
                                MucPx,
                                MucPy,
                                MucPz,
                                MucVolumeName,
                                MucVolumeNumber,
                                MucPosSigmaAlongZ,
                                MucPosSigmaAlongT,
                                MucPosSigmaAlongX,
                                MucPosSigmaAlongY,
                                MucErrorMatrix };
        } // namespace Ext

    } // namespace Dst

    namespace Digi {
        ConstStr rpath = "/Event/Digi";

        namespace FromMc {
            ConstStr rpath  = "/Event/Digi/FromMc";
            ConstStr fromMc = "fromMc";

            ConstStrVec all = { fromMc };
        } // namespace FromMc

        namespace Mdc {
            ConstStr rpath = "/Event/Digi/Mdc";

            ConstStr id         = "id";
            ConstStr adc        = "adc";
            ConstStr tdc        = "tdc";
            ConstStr trackIndex = "trackIndex";
            ConstStr overflow   = "overflow";

            ConstStrVec all = { id, adc, tdc, trackIndex, overflow };
        } // namespace Mdc

        namespace Emc {
            ConstStr rpath = "/Event/Digi/Emc";

            ConstStr id         = "id";
            ConstStr adc        = "adc";
            ConstStr tdc        = "tdc";
            ConstStr trackIndex = "trackIndex";
            ConstStr measure    = "measure";

            ConstStrVec all = { id, adc, tdc, trackIndex, measure };
        } // namespace Emc

        namespace Tof {
            ConstStr rpath = "/Event/Digi/Tof";

            ConstStr id         = "id";
            ConstStr adc        = "adc";
            ConstStr tdc        = "tdc";
            ConstStr trackIndex = "trackIndex";
            ConstStr overflow   = "overflow";

            ConstStrVec all = { id, adc, tdc, trackIndex, overflow };
        } // namespace Tof

        namespace Muc {
            ConstStr rpath = "/Event/Digi/Muc";

            ConstStr id         = "id";
            ConstStr adc        = "adc";
            ConstStr tdc        = "tdc";
            ConstStr trackIndex = "trackIndex";

            ConstStrVec all = { id, adc, tdc, trackIndex };
        } // namespace Muc

        namespace Lumi {
            ConstStr rpath = "/Event/Digi/Lumi";

            ConstStr id         = "id";
            ConstStr adc        = "adc";
            ConstStr tdc        = "tdc";
            ConstStr trackIndex = "trackIndex";
            ConstStr overflow   = "overflow";

            ConstStrVec all = { id, adc, tdc, trackIndex, overflow };
        } // namespace Lumi

    } // namespace Digi

    namespace EvtRec {
        ConstStr rpath = "/Event/EvtRec";

        namespace Evt {
            ConstStr rpath = "/Event/EvtRec/Evt";

            ConstStr nTotal   = "nTotal";
            ConstStr nCharged = "nCharged";
            ConstStr nNeutral = "nNeutral";
            ConstStr nVee     = "nVee";
            ConstStr nPi0     = "nPi0";
            ConstStr nEta2gg  = "nEta2gg";
            ConstStr nDTag    = "nDTag";

            ConstStrVec all = { nTotal, nCharged, nNeutral, nVee, nPi0, nEta2gg, nDTag };
        } // namespace Evt

        namespace Trk {
            ConstStr rpath = "/Event/EvtRec/Trk";

            ConstStr trackId       = "trackId";
            ConstStr partId        = "partId";
            ConstStr quality       = "quality";
            ConstStr mdcTrackId    = "mdcTrackId";
            ConstStr mdcKalTrackId = "mdcKalTrackId";
            ConstStr mdcDedxId     = "mdcDedxId";
            ConstStr extTrackId    = "extTrackId";
            ConstStr emcShowerId   = "emcShowerId";
            ConstStr mucTrackId    = "mucTrackId";
            ConstStr tofTrackIds   = "tofTrackIds";

            ConstStrVec all = { trackId,   partId,     quality,     mdcTrackId, mdcKalTrackId,
                                mdcDedxId, extTrackId, emcShowerId, mucTrackId, tofTrackIds };
        } // namespace Trk

        namespace PrimaryVertex {
            ConstStr rpath = "/Event/EvtRec/PrimaryVertex";

            ConstStr isValid     = "isValid";
            ConstStr nTracks     = "nTracks";
            ConstStr trackIdList = "trackIdList";
            ConstStr chi2        = "chi2";
            ConstStr ndof        = "ndof";
            ConstStr fitMethod   = "fitMethod";
            ConstStr x           = "x";
            ConstStr y           = "y";
            ConstStr z           = "z";
            ConstStr errVtx      = "errVtx";

            ConstStrVec all = { isValid,   nTracks, trackIdList, chi2, ndof,
                                fitMethod, x,       y,           z,    errVtx };
        } // namespace PrimaryVertex

        namespace VeeVertex {
            ConstStr rpath = "/Event/EvtRec/VeeVertex";

            ConstStr vtxId     = "vtxId";
            ConstStr vtxType   = "vtxType";
            ConstStr chi2      = "chi2";
            ConstStr ndof      = "ndof";
            ConstStr mass      = "mass";
            ConstStr px        = "px";
            ConstStr py        = "py";
            ConstStr pz        = "pz";
            ConstStr E         = "E";
            ConstStr x         = "x";
            ConstStr y         = "y";
            ConstStr z         = "z";
            ConstStr err       = "err";
            ConstStr pair      = "pair";
            ConstStr nCharge   = "nCharge";
            ConstStr nTracks   = "nTracks";
            ConstStr daughters = "daughters";

            ConstStrVec all = { vtxId, vtxType, chi2,    ndof,    mass,     px,
                                py,    pz,      E,       x,       y,        z,
                                err,   pair,    nCharge, nTracks, daughters };
        } // namespace VeeVertex

        namespace Pi0 {
            ConstStr rpath = "/Event/EvtRec/Pi0";

            ConstStr unconMass = "unconMass";
            ConstStr chi2      = "chi2";
            ConstStr hiPx      = "hiPx";
            ConstStr hiPy      = "hiPy";
            ConstStr hiPz      = "hiPz";
            ConstStr hiE       = "hiE";
            ConstStr loPx      = "loPx";
            ConstStr loPy      = "loPy";
            ConstStr loPz      = "loPz";
            ConstStr loE       = "loE";
            ConstStr hiEnGamma = "hiEnGamma";
            ConstStr loEnGamma = "loEnGamma";

            ConstStrVec all = { unconMass, chi2, hiPx, hiPy, hiPz,      hiE,
                                loPx,      loPy, loPz, loE,  hiEnGamma, loEnGamma };
        } // namespace Pi0

        namespace EtaToGG {
            ConstStr rpath = "/Event/EvtRec/EtaToGG";

            ConstStr unconMass = "unconMass";
            ConstStr chi2      = "chi2";
            ConstStr hiPx      = "hiPx";
            ConstStr hiPy      = "hiPy";
            ConstStr hiPz      = "hiPz";
            ConstStr hiE       = "hiE";
            ConstStr loPx      = "loPx";
            ConstStr loPy      = "loPy";
            ConstStr loPz      = "loPz";
            ConstStr loE       = "loE";
            ConstStr hiEnGamma = "hiEnGamma";
            ConstStr loEnGamma = "loEnGamma";

            ConstStrVec all = { unconMass, chi2, hiPx, hiPy, hiPz,      hiE,
                                loPx,      loPy, loPz, loE,  hiEnGamma, loEnGamma };

        } // namespace EtaToGG

        namespace DTag {
            ConstStr rpath = "/Event/EvtRec/DTag";

            ConstStr decayMode    = "decayMode";
            ConstStr type         = "type";
            ConstStr beamE        = "beamE";
            ConstStr mass         = "mass";
            ConstStr mBC          = "mBC";
            ConstStr deltaE       = "deltaE";
            ConstStr charge       = "charge";
            ConstStr charm        = "charm";
            ConstStr nChild       = "nChild";
            ConstStr px           = "px";
            ConstStr py           = "py";
            ConstStr pz           = "pz";
            ConstStr e            = "e";
            ConstStr tracks       = "tracks";
            ConstStr showers      = "showers";
            ConstStr otherTracks  = "otherTracks";
            ConstStr otherShowers = "otherShowers";
            ConstStr pionId       = "pionId";
            ConstStr kaonId       = "kaonId";

            ConstStrVec all = { decayMode,   type,         beamE,  mass,   mBC,
                                deltaE,      charge,       charm,  nChild, px,
                                py,          pz,           e,      tracks, showers,
                                otherTracks, otherShowers, pionId, kaonId };
        } // namespace DTag
    } // namespace EvtRec

    namespace Rec {
        ConstStr rpath = "/Event/Rec";

        namespace MdcTrack {
            ConstStr rpath = "/Event/Rec/MdcTrack";

            ConstStr trackId = "trackId";
            ConstStr helix   = "helix";
            ConstStr stat    = "stat";
            ConstStr chi2    = "chi2";
            ConstStr ndof    = "ndof";
            ConstStr err     = "err";
            ConstStr nhits   = "nhits";
            ConstStr nster   = "nster";
            ConstStr nlayer  = "nlayer";
            ConstStr vx0     = "vx0";
            ConstStr vy0     = "vy0";
            ConstStr vz0     = "vz0";
            ConstStr fiTerm  = "fiTerm";

            ConstStrVec all = { trackId, helix,  stat, chi2, ndof, err,   nhits,
                                nster,   nlayer, vx0,  vy0,  vz0,  fiTerm };
        } // namespace MdcTrack

        namespace MdcHit {
            ConstStr rpath = "/Event/Rec/MdcHit";

            ConstStr isGrouped         = "isGrouped";
            ConstStr id                = "id";
            ConstStr trkId             = "trkId";
            ConstStr driftDistLeft     = "driftDistLeft";
            ConstStr driftDistRight    = "driftDistRight";
            ConstStr errDriftDistLeft  = "errDriftDistLeft";
            ConstStr errDriftDistRight = "errDriftDistRight";
            ConstStr chi2Contrib       = "chi2Contrib";
            ConstStr leftOrRight       = "leftOrRight";
            ConstStr stat              = "stat";
            ConstStr mdcId             = "mdcId";
            ConstStr tdc               = "tdc";
            ConstStr adc               = "adc";
            ConstStr driftTime         = "driftTime";
            ConstStr doca              = "doca";
            ConstStr entranceAngle     = "entranceAngle";
            ConstStr zHit              = "zHit";
            ConstStr flightLength      = "flightLength";

            ConstStrVec all = { isGrouped,
                                id,
                                trkId,
                                driftDistLeft,
                                driftDistRight,
                                errDriftDistLeft,
                                errDriftDistRight,
                                chi2Contrib,
                                leftOrRight,
                                stat,
                                mdcId,
                                tdc,
                                adc,
                                driftTime,
                                doca,
                                entranceAngle,
                                zHit,
                                flightLength };
        } // namespace MdcHit

        namespace TofTrack {
            ConstStr rpath = "/Event/Rec/TofTrack";

            ConstStr trackId   = "trackId";
            ConstStr inTrackId = "inTrackId";
            ConstStr tofId     = "tofId";
            ConstStr status    = "status";
            ConstStr path      = "path";
            ConstStr zrhit     = "zrhit";
            ConstStr ph        = "ph";
            ConstStr tof       = "tof";
            ConstStr beta      = "beta";
            ConstStr texp      = "texp";
            ConstStr toffset   = "toffset";
            ConstStr sigma     = "sigma";
            ConstStr quality   = "quality";
            ConstStr t0        = "t0";
            ConstStr errt0     = "errt0";
            ConstStr errz      = "errz";
            ConstStr phi       = "phi";
            ConstStr errphi    = "errphi";
            ConstStr energy    = "energy";
            ConstStr errenergy = "errenergy";

            ConstStrVec all = { trackId, inTrackId, tofId, status,  path,   zrhit,    ph,
                                tof,     beta,      texp,  toffset, sigma,  quality,  t0,
                                errt0,   errz,      phi,   errphi,  energy, errenergy };
        } // namespace TofTrack

        namespace EmcHit {
            ConstStr rpath = "/Event/Rec/EmcHit";

            ConstStr cellId = "cellId";
            ConstStr energy = "energy";
            ConstStr time   = "time";

            ConstStrVec all = { cellId, energy, time };
        } // namespace EmcHit

        namespace EmcCluster {
            ConstStr rpath = "/Event/Rec/EmcCluster";

            ConstStr clusterId = "clusterId";
            ConstStr hits      = "hits";
            ConstStr seeds     = "seeds";
            ConstStr showers   = "showers";

            ConstStrVec all = { clusterId, hits, seeds, showers };
        } // namespace EmcCluster

        namespace EmcShower {
            ConstStr rpath = "/Event/Rec/EmcShower";

            ConstStr trackId         = "trackId";
            ConstStr nhits           = "nhits";
            ConstStr status          = "status";
            ConstStr cellId          = "cellId";
            ConstStr module          = "module";
            ConstStr x               = "x";
            ConstStr y               = "y";
            ConstStr z               = "z";
            ConstStr dTheta          = "dTheta";
            ConstStr dPhi            = "dPhi";
            ConstStr energy          = "energy";
            ConstStr dE              = "dE";
            ConstStr eSeed           = "eSeed";
            ConstStr e3x3            = "e3x3";
            ConstStr e5x5            = "e5x5";
            ConstStr eall            = "eall";
            ConstStr eLepton         = "eLepton";
            ConstStr time            = "time";
            ConstStr secondMoment    = "secondMoment";
            ConstStr latMoment       = "latMoment";
            ConstStr a20Moment       = "a20Moment";
            ConstStr a42Moment       = "a42Moment";
            ConstStr err             = "err";
            ConstStr cellIdMapId     = "cellIdMapId";
            ConstStr cellIdMapEnergy = "cellIdMapEnergy";
            ConstStr cellId3x3       = "cellId3x3";
            ConstStr cellId5x5       = "cellId5x5";
            ConstStr clusterId       = "clusterId";

            ConstStrVec all = { trackId,   nhits,     status,   cellId,       module,
                                x,         y,         z,        dTheta,       dPhi,
                                energy,    dE,        eSeed,    e3x3,         e5x5,
                                eall,      eLepton,   time,     secondMoment, latMoment,
                                a20Moment, a42Moment, err,      cellIdMapId,  cellIdMapEnergy,
                                cellId3x3, cellId5x5, clusterId };
        } // namespace EmcShower

        namespace MucTrack {
            ConstStr rpath = "/Event/Rec/MucTrack";

            ConstStr trackId        = "trackId";
            ConstStr id             = "id";
            ConstStr status         = "status";
            ConstStr type           = "type";
            ConstStr startPart      = "startPart";
            ConstStr endPart        = "endPart";
            ConstStr brLastLayer    = "brLastLayer";
            ConstStr ecLastLayer    = "ecLastLayer";
            ConstStr numHits        = "numHits";
            ConstStr numLayers      = "numLayers";
            ConstStr maxHitsInLayer = "maxHitsInLayer";
            ConstStr depth          = "depth";
            ConstStr chi2           = "chi2";
            ConstStr dof            = "dof";
            ConstStr rms            = "rms";
            ConstStr xPos           = "xPos";
            ConstStr yPos           = "yPos";
            ConstStr zPos           = "zPos";
            ConstStr xPosSigma      = "xPosSigma";
            ConstStr yPosSigma      = "yPosSigma";
            ConstStr zPosSigma      = "zPosSigma";
            ConstStr px             = "px";
            ConstStr py             = "py";
            ConstStr pz             = "pz";
            ConstStr distance       = "distance";
            ConstStr deltaPhi       = "deltaPhi";
            ConstStr hits           = "hits";
            ConstStr expHits        = "expHits";
            ConstStr distHits       = "distHits";
            ConstStr kalrechi2      = "kalrechi2";
            ConstStr kaldof         = "kaldof";
            ConstStr kaldepth       = "kaldepth";
            ConstStr kalbrLastLayer = "kalbrLastLayer";
            ConstStr kalecLastLayer = "kalecLastLayer";

            ConstStrVec all = { trackId,
                                id,
                                status,
                                type,
                                startPart,
                                endPart,
                                brLastLayer,
                                ecLastLayer,
                                numHits,
                                numLayers,
                                maxHitsInLayer,
                                depth,
                                chi2,
                                dof,
                                rms,
                                xPos,
                                yPos,
                                zPos,
                                xPosSigma,
                                yPosSigma,
                                zPosSigma,
                                px,
                                py,
                                pz,
                                distance,
                                deltaPhi,
                                hits,
                                expHits,
                                distHits,
                                kalrechi2,
                                kaldof,
                                kaldepth,
                                kalbrLastLayer,
                                kalecLastLayer };
        } // namespace MucTrack

        namespace MdcDedx {
            ConstStr rpath = "/Event/Rec/MdcDedx";

            ConstStr dedx_hit      = "dedx_hit";
            ConstStr dedx_esat     = "dedx_esat";
            ConstStr dedx_norun    = "dedx_norun";
            ConstStr dedx_momentum = "dedx_momentum";
            ConstStr trackId       = "trackId";
            ConstStr mdcTrackId    = "mdcTrackId";
            ConstStr mdcKalTrackId = "mdcKalTrackId";
            ConstStr particleId    = "particleId";
            ConstStr status        = "status";
            ConstStr trunc_alg     = "trunc_alg";
            ConstStr chiE          = "chiE";
            ConstStr chiMu         = "chiMu";
            ConstStr chiPi         = "chiPi";
            ConstStr chiK          = "chiK";
            ConstStr chiP          = "chiP";
            ConstStr numGoodHits   = "numGoodHits";
            ConstStr numTotalHits  = "numTotalHits";
            ConstStr probPH        = "probPH";
            ConstStr normPH        = "normPH";
            ConstStr errorPH       = "errorPH";
            ConstStr twentyPH      = "twentyPH";
            ConstStr chi           = "chi";
            ConstStr dedx_exp      = "dedx_exp";
            ConstStr sigma_dedx    = "sigma_dedx";
            ConstStr pid_prob      = "pid_prob";

            ConstStrVec all = {
                dedx_hit,    dedx_esat,     dedx_norun, dedx_momentum, trackId,
                mdcTrackId,  mdcKalTrackId, particleId, status,        trunc_alg,
                chiE,        chiMu,         chiPi,      chiK,          chiP,
                numGoodHits, numTotalHits,  probPH,     normPH,        errorPH,
                twentyPH,    chi,           dedx_exp,   sigma_dedx,    pid_prob };
        } // namespace MdcDedx

        namespace MdcDedxHit {
            ConstStr rpath = "/Event/Rec/MdcDedxHit";

            ConstStr isGrouped        = "isGrouped";
            ConstStr trkId            = "trkId";
            ConstStr mdcHitId         = "mdcHitId";
            ConstStr mdcKalHelixSegId = "mdcKalHelixSegId";
            ConstStr leftOrRight      = "leftOrRight";
            ConstStr mdcId            = "mdcId";
            ConstStr path             = "path";
            ConstStr dedx             = "dedx";

            ConstStrVec all = { isGrouped,   trkId, mdcHitId, mdcKalHelixSegId,
                                leftOrRight, mdcId, path,     dedx };
        } // namespace MdcDedxHit

        namespace ExtTrack {
            ConstStr rpath = "/Event/Rec/ExtTrack";

            ConstStr trackId               = "trackId";
            ConstStr tof1X                 = "tof1X";
            ConstStr tof1Y                 = "tof1Y";
            ConstStr tof1Z                 = "tof1Z";
            ConstStr tof1Px                = "tof1Px";
            ConstStr tof1Py                = "tof1Py";
            ConstStr tof1Pz                = "tof1Pz";
            ConstStr tof1VolumeName        = "tof1VolumeName";
            ConstStr tof1VolumeNumber      = "tof1VolumeNumber";
            ConstStr tof1                  = "tof1";
            ConstStr tof1Path              = "tof1Path";
            ConstStr tof1PosSigmaAlongZ    = "tof1PosSigmaAlongZ";
            ConstStr tof1PosSigmaAlongT    = "tof1PosSigmaAlongT";
            ConstStr tof1PosSigmaAlongX    = "tof1PosSigmaAlongX";
            ConstStr tof1PosSigmaAlongY    = "tof1PosSigmaAlongY";
            ConstStr tof1ErrorMatrix       = "tof1ErrorMatrix";
            ConstStr tof2X                 = "tof2X";
            ConstStr tof2Y                 = "tof2Y";
            ConstStr tof2Z                 = "tof2Z";
            ConstStr tof2Px                = "tof2Px";
            ConstStr tof2Py                = "tof2Py";
            ConstStr tof2Pz                = "tof2Pz";
            ConstStr tof2VolumeName        = "tof2VolumeName";
            ConstStr tof2VolumeNumber      = "tof2VolumeNumber";
            ConstStr tof2                  = "tof2";
            ConstStr tof2Path              = "tof2Path";
            ConstStr tof2PosSigmaAlongZ    = "tof2PosSigmaAlongZ";
            ConstStr tof2PosSigmaAlongT    = "tof2PosSigmaAlongT";
            ConstStr tof2PosSigmaAlongX    = "tof2PosSigmaAlongX";
            ConstStr tof2PosSigmaAlongY    = "tof2PosSigmaAlongY";
            ConstStr tof2ErrorMatrix       = "tof2ErrorMatrix";
            ConstStr emcX                  = "emcX";
            ConstStr emcY                  = "emcY";
            ConstStr emcZ                  = "emcZ";
            ConstStr emcPx                 = "emcPx";
            ConstStr emcPy                 = "emcPy";
            ConstStr emcPz                 = "emcPz";
            ConstStr emcVolumeName         = "emcVolumeName";
            ConstStr emcVolumeNumber       = "emcVolumeNumber";
            ConstStr emcPosSigmaAlongTheta = "emcPosSigmaAlongTheta";
            ConstStr emcPosSigmaAlongPhi   = "emcPosSigmaAlongPhi";
            ConstStr emcErrorMatrix        = "emcErrorMatrix";
            ConstStr emcPath               = "emcPath";
            ConstStr mucX                  = "mucX";
            ConstStr mucY                  = "mucY";
            ConstStr mucZ                  = "mucZ";
            ConstStr mucPx                 = "mucPx";
            ConstStr mucPy                 = "mucPy";
            ConstStr mucPz                 = "mucPz";
            ConstStr mucVolumeName         = "mucVolumeName";
            ConstStr mucVolumeNumber       = "mucVolumeNumber";
            ConstStr mucPosSigmaAlongZ     = "mucPosSigmaAlongZ";
            ConstStr mucPosSigmaAlongT     = "mucPosSigmaAlongT";
            ConstStr mucPosSigmaAlongX     = "mucPosSigmaAlongX";
            ConstStr mucPosSigmaAlongY     = "mucPosSigmaAlongY";
            ConstStr mucErrorMatrix        = "mucErrorMatrix";
            ConstStr mucHitVecSize         = "mucHitVecSize";
            ConstStr mucHitX               = "mucHitX";
            ConstStr mucHitY               = "mucHitY";
            ConstStr mucHitZ               = "mucHitZ";
            ConstStr mucHitPx              = "mucHitPx";
            ConstStr mucHitPy              = "mucHitPy";
            ConstStr mucHitPz              = "mucHitPz";
            ConstStr mucHitVolumeName      = "mucHitVolumeName";
            ConstStr mucHitVolumeNumber    = "mucHitVolumeNumber";
            ConstStr mucHitPosSigmaAlongZ  = "mucHitPosSigmaAlongZ";
            ConstStr mucHitPosSigmaAlongT  = "mucHitPosSigmaAlongT";
            ConstStr mucHitPosSigmaAlongX  = "mucHitPosSigmaAlongX";
            ConstStr mucHitPosSigmaAlongY  = "mucHitPosSigmaAlongY";
            ConstStr mucHitErrorMatrix     = "mucHitErrorMatrix";

            ConstStrVec all = { trackId,
                                tof1X,
                                tof1Y,
                                tof1Z,
                                tof1Px,
                                tof1Py,
                                tof1Pz,
                                tof1VolumeName,
                                tof1VolumeNumber,
                                tof1,
                                tof1Path,
                                tof1PosSigmaAlongZ,
                                tof1PosSigmaAlongT,
                                tof1PosSigmaAlongX,
                                tof1PosSigmaAlongY,
                                tof1ErrorMatrix,
                                tof2X,
                                tof2Y,
                                tof2Z,
                                tof2Px,
                                tof2Py,
                                tof2Pz,
                                tof2VolumeName,
                                tof2VolumeNumber,
                                tof2,
                                tof2Path,
                                tof2PosSigmaAlongZ,
                                tof2PosSigmaAlongT,
                                tof2PosSigmaAlongX,
                                tof2PosSigmaAlongY,
                                tof2ErrorMatrix,
                                emcX,
                                emcY,
                                emcZ,
                                emcPx,
                                emcPy,
                                emcPz,
                                emcVolumeName,
                                emcVolumeNumber,
                                emcPosSigmaAlongTheta,
                                emcPosSigmaAlongPhi,
                                emcErrorMatrix,
                                emcPath,
                                mucX,
                                mucY,
                                mucZ,
                                mucPx,
                                mucPy,
                                mucPz,
                                mucVolumeName,
                                mucVolumeNumber,
                                mucPosSigmaAlongZ,
                                mucPosSigmaAlongT,
                                mucPosSigmaAlongX,
                                mucPosSigmaAlongY,
                                mucErrorMatrix,
                                mucHitVecSize,
                                mucHitX,
                                mucHitY,
                                mucHitZ,
                                mucHitPx,
                                mucHitPy,
                                mucHitPz,
                                mucHitVolumeName,
                                mucHitVolumeNumber,
                                mucHitPosSigmaAlongZ,
                                mucHitPosSigmaAlongT,
                                mucHitPosSigmaAlongX,
                                mucHitPosSigmaAlongY,
                                mucHitErrorMatrix };
        } // namespace ExtTrack

        namespace MdcKalTrack {
            ConstStr rpath = "/Event/Rec/MdcKalTrack";

            ConstStr trackId   = "trackId";
            ConstStr mass      = "mass";
            ConstStr path      = "path";
            ConstStr tof       = "tof";
            ConstStr fiTerm    = "fiTerm";
            ConstStr pathSM    = "pathSM";
            ConstStr nhits     = "nhits";
            ConstStr nlayer    = "nlayer";
            ConstStr stat      = "stat";
            ConstStr chi2      = "chi2";
            ConstStr ndof      = "ndof";
            ConstStr nSegs     = "nSegs";
            ConstStr poca      = "poca";
            ConstStr poca_e    = "poca_e";
            ConstStr poca_mu   = "poca_mu";
            ConstStr poca_k    = "poca_k";
            ConstStr poca_p    = "poca_p";
            ConstStr lpoint    = "lpoint";
            ConstStr lpoint_e  = "lpoint_e";
            ConstStr lpoint_mu = "lpoint_mu";
            ConstStr lpoint_k  = "lpoint_k";
            ConstStr lpoint_p  = "lpoint_p";
            ConstStr lpivot    = "lpivot";
            ConstStr lpivot_e  = "lpivot_e";
            ConstStr lpivot_mu = "lpivot_mu";
            ConstStr lpivot_k  = "lpivot_k";
            ConstStr lpivot_p  = "lpivot_p";
            ConstStr zhelix    = "zhelix";
            ConstStr zerror    = "zerror";
            ConstStr zhelix_e  = "zhelix_e";
            ConstStr zerror_e  = "zerror_e";
            ConstStr zhelix_mu = "zhelix_mu";
            ConstStr zerror_mu = "zerror_mu";
            ConstStr zhelix_k  = "zhelix_k";
            ConstStr zerror_k  = "zerror_k";
            ConstStr zhelix_p  = "zhelix_p";
            ConstStr zerror_p  = "zerror_p";
            ConstStr fhelix    = "fhelix";
            ConstStr ferror    = "ferror";
            ConstStr fhelix_e  = "fhelix_e";
            ConstStr ferror_e  = "ferror_e";
            ConstStr fhelix_mu = "fhelix_mu";
            ConstStr ferror_mu = "ferror_mu";
            ConstStr fhelix_k  = "fhelix_k";
            ConstStr ferror_k  = "ferror_k";
            ConstStr fhelix_p  = "fhelix_p";
            ConstStr ferror_p  = "ferror_p";
            ConstStr lhelix    = "lhelix";
            ConstStr lerror    = "lerror";
            ConstStr lhelix_e  = "lhelix_e";
            ConstStr lerror_e  = "lerror_e";
            ConstStr lhelix_mu = "lhelix_mu";
            ConstStr lerror_mu = "lerror_mu";
            ConstStr lhelix_k  = "lhelix_k";
            ConstStr lerror_k  = "lerror_k";
            ConstStr lhelix_p  = "lhelix_p";
            ConstStr lerror_p  = "lerror_p";
            ConstStr thelix    = "thelix";
            ConstStr terror    = "terror";

            ConstStrVec all = {
                trackId,   mass,     path,      tof,       fiTerm,    pathSM,    nhits,
                nlayer,    stat,     chi2,      ndof,      nSegs,     poca,      poca_e,
                poca_mu,   poca_k,   poca_p,    lpoint,    lpoint_e,  lpoint_mu, lpoint_k,
                lpoint_p,  lpivot,   lpivot_e,  lpivot_mu, lpivot_k,  lpivot_p,  zhelix,
                zerror,    zhelix_e, zerror_e,  zhelix_mu, zerror_mu, zhelix_k,  zerror_k,
                zhelix_p,  zerror_p, fhelix,    ferror,    fhelix_e,  ferror_e,  fhelix_mu,
                ferror_mu, fhelix_k, ferror_k,  fhelix_p,  ferror_p,  lhelix,    lerror,
                lhelix_e,  lerror_e, lhelix_mu, lerror_mu, lhelix_k,  lerror_k,  lhelix_p,
                lerror_p,  thelix,   terror };
        } // namespace MdcKalTrack

        namespace MdcKalHelixSeg {
            ConstStr rpath = "/Event/Rec/MdcKalHelixSeg";

            ConstStr trackId       = "trackId";
            ConstStr leftOrRight   = "leftOrRight";
            ConstStr mdcId         = "mdcId";
            ConstStr tdc           = "tdc";
            ConstStr adc           = "adc";
            ConstStr zhit          = "zhit";
            ConstStr tof           = "tof";
            ConstStr docaInCell    = "docaInCell";
            ConstStr docaExCell    = "docaExCell";
            ConstStr driftDistance = "driftDistance";
            ConstStr entranceAngle = "entranceAngle";
            ConstStr driftTime     = "driftTime";
            ConstStr helixInCell   = "helixInCell";
            ConstStr helixExCell   = "helixExCell";

            ConstStrVec all = { trackId,     leftOrRight,   mdcId,         tdc,
                                adc,         zhit,          tof,           docaInCell,
                                docaExCell,  driftDistance, entranceAngle, driftTime,
                                helixInCell, helixExCell };
        } // namespace MdcKalHelixSeg

        namespace EvTime {
            ConstStr rpath = "/Event/Rec/EvTime";

            ConstStr status  = "status";
            ConstStr estime  = "estime";
            ConstStr quality = "quality";

            ConstStrVec all = { status, estime, quality };
        } // namespace EvTime

        namespace Zdd {
            ConstStr rpath = "/Event/Rec/Zdd";

            ConstStr channelId  = "channelId";
            ConstStr scanCode   = "scanCode";
            ConstStr baseLine   = "baseLine";
            ConstStr phase      = "phase";
            ConstStr fragTime   = "fragTime";
            ConstStr fragEnergy = "fragEnergy";

            ConstStrVec all = { channelId, scanCode, baseLine, phase, fragTime, fragEnergy };
        } // namespace Zdd

    } // namespace Rec

    namespace Hlt {
        ConstStr rpath = "/Event/Hlt";

        namespace Raw {
            ConstStr rpath = "/Event/Hlt/Raw";

            ConstStr id         = "id";
            ConstStr adc        = "adc";
            ConstStr tdc        = "tdc";
            ConstStr trackIndex = "trackIndex";

            ConstStrVec all = { id, adc, tdc, trackIndex };
        } // namespace Raw

        namespace Inf {
            ConstStr rpath = "/Event/Hlt/Inf";

            ConstStr evtType    = "evtType";
            ConstStr algProcess = "algProcess";
            ConstStr criTable   = "criTable";
            ConstStr verNumber  = "verNumber";
            ConstStr eTotal     = "eTotal";
            ConstStr subNumber  = "subNumber";
            ConstStr conNumber  = "conNumber";
            ConstStr mdcData    = "mdcData";
            ConstStr tofData    = "tofData";
            ConstStr emcData    = "emcData";
            ConstStr mucData    = "mucData";
            ConstStr conData    = "conData";

            ConstStrVec all = { evtType,   algProcess, criTable, verNumber, eTotal,  subNumber,
                                conNumber, mdcData,    tofData,  emcData,   mucData, conData };
        } // namespace Inf

        namespace DstInf {
            ConstStr rpath = "/Event/Hlt/DstInf";

            ConstStr evtType    = "evtType";
            ConstStr algProcess = "algProcess";
            ConstStr criTable   = "criTable";
            ConstStr verNumber  = "verNumber";
            ConstStr eTotal     = "eTotal";
            ConstStr subNumber  = "subNumber";
            ConstStr conNumber  = "conNumber";

            ConstStrVec all = { evtType, algProcess, criTable, verNumber,
                                eTotal,  subNumber,  conNumber };
        } // namespace DstInf
    } // namespace Hlt

    namespace Trig {

        ConstStr rpath = "/Event/Trig";

        ConstStr preScale       = "preScale";
        ConstStr trigConditions = "trigConditions";
        ConstStr trigChannel    = "trigChannel";
        ConstStr timeWindows    = "timeWindows";
        ConstStr timingType     = "timingType";

        ConstStrVec all = { preScale, trigConditions, trigChannel, timeWindows, timingType };

    } // namespace Trig

    const std::map<std::string, std::string> field2branch = {
        // TEventHeader
        { EvtHeader::rpath, "TEvtHeader" },

        // Trig Event
        { Trig::rpath, "TTrigEvent" },

        // RecObject
        { EvtRec::Evt::rpath, "TEvtRecObject" },
        { EvtRec::Trk::rpath, "TEvtRecObject" },
        { EvtRec::Pi0::rpath, "TEvtRecObject" },
        { EvtRec::EtaToGG::rpath, "TEvtRecObject" },
        { EvtRec::PrimaryVertex::rpath, "TEvtRecObject" },
        { EvtRec::VeeVertex::rpath, "TEvtRecObject" },
        { EvtRec::DTag::rpath, "TEvtRecObject" },

        // Mc Event
        { Mc::Mdc::rpath, "TMcEvent" },
        { Mc::Emc::rpath, "TMcEvent" },
        { Mc::Tof::rpath, "TMcEvent" },
        { Mc::Muc::rpath, "TMcEvent" },
        { Mc::McParticle::rpath, "TMcEvent" },

        // Digi Event
        { Digi::FromMc::rpath, "TDigiEvent" },
        { Digi::Mdc::rpath, "TDigiEvent" },
        { Digi::Emc::rpath, "TDigiEvent" },
        { Digi::Tof::rpath, "TDigiEvent" },
        { Digi::Muc::rpath, "TDigiEvent" },
        { Digi::Lumi::rpath, "TDigiEvent" },

        // Dst Event
        { Dst::Mdc::rpath, "TDstEvent" },
        { Dst::Emc::rpath, "TDstEvent" },
        { Dst::Tof::rpath, "TDstEvent" },
        { Dst::Muc::rpath, "TDstEvent" },
        { Dst::Dedx::rpath, "TDstEvent" },
        { Dst::Ext::rpath, "TDstEvent" },

        // Rec Event
        { Rec::MdcTrack::rpath, "TRecEvent" },
        { Rec::MdcHit::rpath, "TRecEvent" },
        { Rec::TofTrack::rpath, "TRecEvent" },
        { Rec::EmcHit::rpath, "TRecEvent" },
        { Rec::EmcCluster::rpath, "TRecEvent" },
        { Rec::EmcShower::rpath, "TRecEvent" },
        { Rec::MucTrack::rpath, "TRecEvent" },
        { Rec::MdcDedx::rpath, "TRecEvent" },
        { Rec::MdcDedxHit::rpath, "TRecEvent" },
        { Rec::ExtTrack::rpath, "TRecEvent" },
        { Rec::MdcKalTrack::rpath, "TRecEvent" },
        { Rec::MdcKalHelixSeg::rpath, "TRecEvent" },
        { Rec::EvTime::rpath, "TRecEvent" },
        { Rec::Zdd::rpath, "TRecEvent" },

        // Hlt Event
        { Hlt::Raw::rpath, "THltEvent" },
        { Hlt::Inf::rpath, "THltEvent" },
        { Hlt::DstInf::rpath, "THltEvent" },
    };

} // namespace BesFieldNames
