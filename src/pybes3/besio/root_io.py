from __future__ import annotations

import awkward as ak
import awkward.contents
import awkward.index
import numpy as np
import uproot
import uproot.behaviors.TBranch
import uproot.extras
import uproot.interpretation
import uproot_custom.readers.cpp
import uproot_custom.readers.python
import array
from uproot_custom import (
    AnyClassFactory,
    AsCustom,
    EmptyFactory,
    Factory,
    GroupFactory,
    PrimitiveFactory,
    build_factory,
    regularize_object_path,
)

from pybes3.besio import besio_cpp as bcpp

bes3_branch2types = {
    "/Event:TMcEvent/m_mdcMcHitCol": "TMdcMc",
    "/Event:TMcEvent/m_cgemMcHitCol": "TCgemMc",
    "/Event:TMcEvent/m_emcMcHitCol": "TEmcMc",
    "/Event:TMcEvent/m_tofMcHitCol": "TTofMc",
    "/Event:TMcEvent/m_mucMcHitCol": "TMucMc",
    "/Event:TMcEvent/m_mcParticleCol": "TMcParticle",
    "/Event:TDigiEvent/m_mdcDigiCol": "TMdcDigi",
    "/Event:TDigiEvent/m_cgemDigiCol": "TCgemDigi",
    "/Event:TDigiEvent/m_emcDigiCol": "TEmcDigi",
    "/Event:TDigiEvent/m_tofDigiCol": "TTofDigi",
    "/Event:TDigiEvent/m_mucDigiCol": "TMucDigi",
    "/Event:TDigiEvent/m_lumiDigiCol": "TLumiDigi",
    "/Event:TDstEvent/m_mdcTrackCol": "TMdcTrack",
    "/Event:TDstEvent/m_emcTrackCol": "TEmcTrack",
    "/Event:TDstEvent/m_tofTrackCol": "TTofTrack",
    "/Event:TDstEvent/m_mucTrackCol": "TMucTrack",
    "/Event:TDstEvent/m_mdcDedxCol": "TMdcDedx",
    "/Event:TDstEvent/m_extTrackCol": "TExtTrack",
    "/Event:TDstEvent/m_mdcKalTrackCol": "TMdcKalTrack",
    "/Event:TRecEvent/m_recCgemClusterCol": "TRecCgemCluster",
    "/Event:TRecEvent/m_recMdcTrackCol": "TRecMdcTrack",
    "/Event:TRecEvent/m_recMdcHitCol": "TRecMdcHit",
    "/Event:TRecEvent/m_recEmcHitCol": "TRecEmcHit",
    "/Event:TRecEvent/m_recEmcClusterCol": "TRecEmcCluster",
    "/Event:TRecEvent/m_recEmcShowerCol": "TRecEmcShower",
    "/Event:TRecEvent/m_recTofTrackCol": "TRecTofTrack",
    "/Event:TRecEvent/m_recMucTrackCol": "TRecMucTrack",
    "/Event:TRecEvent/m_recMdcDedxCol": "TRecMdcDedx",
    "/Event:TRecEvent/m_recMdcDedxHitCol": "TRecMdcDedxHit",
    "/Event:TRecEvent/m_recExtTrackCol": "TRecExtTrack",
    "/Event:TRecEvent/m_recMdcKalTrackCol": "TRecMdcKalTrack",
    "/Event:TRecEvent/m_recMdcKalHelixSegCol": "TRecMdcKalHelixSeg",
    "/Event:TRecEvent/m_recEvTimeCol": "TRecEvTime",
    "/Event:TRecEvent/m_recZddChannelCol": "TRecZddChannel",
    "/Event:TEvtRecObject/m_evtRecTrackCol": "TEvtRecTrack",
    "/Event:TEvtRecObject/m_evtRecVeeVertexCol": "TEvtRecVeeVertex",
    "/Event:TEvtRecObject/m_evtRecPi0Col": "TEvtRecPi0",
    "/Event:TEvtRecObject/m_evtRecEtaToGGCol": "TEvtRecEtaToGG",
    "/Event:TEvtRecObject/m_evtRecDTagCol": "TEvtRecDTag",
    "/Event:THltEvent/m_hltRawCol": "THltRaw",
    "/Event:EventNavigator/m_mcMdcMcHits": None,
    "/Event:EventNavigator/m_mcMdcTracks": None,
    "/Event:EventNavigator/m_mcEmcMcHits": None,
    "/Event:EventNavigator/m_mcEmcRecShowers": None,
}


class Bes3PyTObjArrayReader(uproot_custom.readers.python.IReader):
    def __init__(self, name, element_reader: uproot_custom.readers.python.IReader):
        super().__init__(name)
        self.element_reader = element_reader
        self.offsets = array.array("I", [0])

    def read(self, stream):
        stream.skip_fNBytes()
        stream.skip_fVersion()
        stream.skip_fVersion()
        stream.skip(4)
        stream.skip(4)

        stream.skip(1)
        fSize = stream.read_uint32()
        stream.skip(4)

        self.offsets.append(self.offsets[-1] + fSize)

        for _ in range(fSize):
            stream.skip_obj_header()
            self.element_reader.read(stream)

    def data(self):
        element_data = self.element_reader.data()
        return np.asarray(self.offsets), element_data


class Bes3TObjArrayFactory(Factory):
    @classmethod
    def priority(cls):
        return 50

    @classmethod
    def build_factory(
        cls,
        top_type_name: str,
        cur_streamer_info: dict,
        all_streamer_info: dict,
        item_path: str,
        **kwargs,
    ):
        if top_type_name != "TObjArray":
            return None

        item_path = item_path.replace(".TObjArray*", "")
        obj_typename = bes3_branch2types.get(item_path)
        if obj_typename is None:
            return None

        if obj_typename not in all_streamer_info:
            return cls(
                name=cur_streamer_info["fName"],
                element_factory=EmptyFactory(obj_typename),
            )

        sub_factories = []
        for s in all_streamer_info[obj_typename]:
            sub_factories.append(
                build_factory(
                    cur_streamer_info=s,
                    all_streamer_info=all_streamer_info,
                    item_path=f"{item_path}.{obj_typename}",
                )
            )

        return cls(
            name=cur_streamer_info["fName"],
            element_factory=AnyClassFactory(
                name=obj_typename,
                sub_factories=sub_factories,
            ),
        )

    def __init__(self, name: str, element_factory: Factory):
        super().__init__(name)
        self.element_factory = element_factory

    def build_cpp_reader(self):
        element_reader = self.element_factory.build_cpp_reader()
        return bcpp.Bes3TObjArrayReader(self.name, element_reader)

    def build_python_reader(self):
        element_reader = self.element_factory.build_python_reader()
        return Bes3PyTObjArrayReader(self.name, element_reader)

    def make_awkward_content(self, raw_data):
        offsets, element_raw_data = raw_data
        element_content = self.element_factory.make_awkward_content(element_raw_data)
        return awkward.contents.ListOffsetArray(
            awkward.index.Index64(offsets),
            element_content,
        )

    def make_awkward_form(self):
        element_form = self.element_factory.make_awkward_form()
        return awkward.forms.ListOffsetForm("i64", element_form)


class Bes3BaseObjectFactory(GroupFactory):
    @classmethod
    def priority(cls):
        return 40

    @classmethod
    def build_factory(
        cls,
        top_type_name,
        cls_streamer_info,
        all_streamer_info,
        item_path,
        **kwargs,
    ):
        if top_type_name != "BASE":
            return None

        fType = cls_streamer_info["fType"]
        if fType != 0:
            return None

        # limit to bes3 relevant branches
        if all(k not in item_path for k in bes3_branch2types.keys()):
            return None

        fName = cls_streamer_info["fName"]
        sub_streamers: list[dict] = all_streamer_info[fName]
        sub_factories = [build_factory(s, all_streamer_info, item_path) for s in sub_streamers]

        return cls(name=fName, sub_factories=sub_factories)

    def build_cpp_reader(self):
        sub_readers = [s.build_cpp_reader() for s in self.sub_factories]
        # In TObjArray, base class always contains fNBytes+fVersion header,
        # so use `AnyClassReader` instead of `GroupReader` to read it.
        return uproot_custom.readers.cpp.AnyClassReader(self.name, sub_readers)

    def build_python_reader(self):
        sub_readers = [s.build_python_reader() for s in self.sub_factories]
        return uproot_custom.readers.python.AnyClassReader(self.name, sub_readers)


class Bes3PyCgemClusterColReader(uproot_custom.readers.python.IReader):
    def __init__(self, name):
        super().__init__(name)

        self.version = -1  # -1: unknown, 0: with recpositiony, 1: without recpositiony

        self.offsets = array.array("I", [0])
        self.clusterid = array.array("i")
        self.trkid = array.array("i")
        self.layerid = array.array("i")
        self.sheetid = array.array("i")
        self.flag = array.array("i")
        self.energydeposit = array.array("d")
        self.recphi = array.array("d")
        self.recpositiony = array.array("d")
        self.recv = array.array("d")
        self.recZ = array.array("d")
        self.clusterflag = array.array("i")
        self.stripid = array.array("i")

    def read(self, stream):
        stream.skip_obj_header()

        # TObjArray
        stream.skip_fNBytes()
        stream.skip(13)  # fVersion(2) + fVersion(2) + fUniqueID(4) + fBits(4) + fName(1)
        fSize = stream.read_uint32()
        stream.skip(4)  # fLowerBound

        self.offsets.append(self.offsets[-1] + fSize)

        for _ in range(fSize):
            stream.skip_obj_header()

            fNBytes = stream.read_fNBytes()
            stream.skip_fVersion()

            if self.version == -1:
                assert fNBytes in (
                    96,
                    88,
                ), f"Unknown TCgemCluster version with FNBytes = {fNBytes}"

                self.version = 0 if fNBytes == 96 else 1

            stream.skip_TObject()

            self.clusterid.append(stream.read_int32())
            self.trkid.append(stream.read_int32())
            self.layerid.append(stream.read_int32())
            self.sheetid.append(stream.read_int32())
            self.flag.append(stream.read_int32())
            self.energydeposit.append(stream.read_double())
            self.recphi.append(stream.read_double())

            if self.version == 0:
                self.recpositiony.append(stream.read_double())

            self.recv.append(stream.read_double())
            self.recZ.append(stream.read_double())

            # m_clusterflag is int[2]
            for _ in range(2):
                self.clusterflag.append(stream.read_int32())

            # m_stripid is int[2][2]
            for _ in range(4):
                self.stripid.append(stream.read_int32())

    def data(self):
        result = {}

        result["offsets"] = np.asarray(self.offsets)
        result["m_clusterID"] = np.asarray(self.clusterid)
        result["m_trkID"] = np.asarray(self.trkid)
        result["m_layerID"] = np.asarray(self.layerid)
        result["m_sheetID"] = np.asarray(self.sheetid)
        result["m_flag"] = np.asarray(self.flag)
        result["m_energyDeposit"] = np.asarray(self.energydeposit)
        result["m_recPhi"] = np.asarray(self.recphi)

        if self.version == 0:
            result["m_recPositionY"] = np.asarray(self.recpositiony)

        result["m_recV"] = np.asarray(self.recv)
        result["m_recZ"] = np.asarray(self.recZ)
        result["m_clusterFlag"] = np.asarray(self.clusterflag)
        result["m_stripID"] = np.asarray(self.stripid)

        return result


class Bes3CgemClusterColFactory(Factory):
    @classmethod
    def priority(cls):
        return 55

    @classmethod
    def build_factory(
        cls,
        top_type_name: str,
        cur_streamer_info: dict,
        all_streamer_info: dict,
        item_path: str,
        **kwargs,
    ):
        item_path = item_path.replace(".TObjArray*", "")
        if item_path != "/Event:TRecEvent/m_recCgemClusterCol":
            return None

        if all_streamer_info.get("TCgemCluster") is not None:
            return None  # Let Bes3TObjArrayReader handle it

        return cls(name=cur_streamer_info["fName"])

    def build_cpp_reader(self):
        return bcpp.Bes3CgemClusterColReader(self.name)

    def build_python_reader(self):
        return Bes3PyCgemClusterColReader(self.name)

    def make_awkward_content(self, raw_data: dict):
        offsets = raw_data.pop("offsets")

        record_contents = []
        for k, v in raw_data.items():
            tmp_content = awkward.contents.NumpyArray(v)

            if k == "m_clusterFlag":
                tmp_content = awkward.contents.RegularArray(tmp_content, 2)

            if k == "m_stripID":
                tmp_content = awkward.contents.RegularArray(tmp_content, 2)
                tmp_content = awkward.contents.RegularArray(tmp_content, 2)

            record_contents.append(tmp_content)

        return awkward.contents.ListOffsetArray(
            awkward.index.Index64(offsets),
            awkward.contents.RecordArray(record_contents, list(raw_data.keys())),
        )

    def make_awkward_form(self):
        raise NotImplementedError(
            "make_awkward_form is not implemented for Bes3CgemClusterColFactory"
        )


class Bes3PySymMatrixArrayReader(uproot_custom.readers.python.IReader):
    def __init__(self, name: str, flat_size: int, full_dim: int):
        super().__init__(name)

        self.flat_size = flat_size
        self.full_dim = full_dim
        self._data = array.array("d")

        self._sym_idx = np.empty((full_dim, full_dim), dtype=np.int64)
        for i in range(full_dim):
            for j in range(full_dim):
                idx = self.get_symmetric_matrix_index(i, j)
                if idx >= flat_size:
                    raise ValueError(
                        f"Invalid flat size: {flat_size}, full dim: {full_dim}, "
                        f"i: {i}, j: {j}, idx: {idx}"
                    )
                self._sym_idx[i, j] = idx

    @staticmethod
    def get_symmetric_matrix_index(i: int, j: int) -> int:
        return j * (j + 1) // 2 + i if i < j else i * (i + 1) // 2 + j

    def read(self, stream):
        flat_array = np.empty(self.flat_size, dtype=np.float64)
        for i in range(self.flat_size):
            flat_array[i] = stream.read_double()

        self._data.extend(flat_array[self._sym_idx].ravel())

    def data(self):
        return np.asarray(self._data)


class Bes3SymMatrixArrayFactory(Factory):
    target_items = {
        "/Event:TDstEvent/m_mdcTrackCol.TMdcTrack.m_err",
        "/Event:TDstEvent/m_emcTrackCol.TEmcTrack.m_err",
        "/Event:TDstEvent/m_extTrackCol.TExtTrack.myTof1ErrorMatrix",
        "/Event:TDstEvent/m_extTrackCol.TExtTrack.myTof2ErrorMatrix",
        "/Event:TDstEvent/m_extTrackCol.TExtTrack.myEmcErrorMatrix",
        "/Event:TDstEvent/m_extTrackCol.TExtTrack.myMucErrorMatrix",
        "/Event:TDstEvent/m_mdcKalTrackCol.TMdcKalTrack.m_zerror",
        "/Event:TDstEvent/m_mdcKalTrackCol.TMdcKalTrack.m_zerror_e",
        "/Event:TDstEvent/m_mdcKalTrackCol.TMdcKalTrack.m_zerror_mu",
        "/Event:TDstEvent/m_mdcKalTrackCol.TMdcKalTrack.m_zerror_k",
        "/Event:TDstEvent/m_mdcKalTrackCol.TMdcKalTrack.m_zerror_p",
        "/Event:TDstEvent/m_mdcKalTrackCol.TMdcKalTrack.m_ferror",
        "/Event:TDstEvent/m_mdcKalTrackCol.TMdcKalTrack.m_ferror_e",
        "/Event:TDstEvent/m_mdcKalTrackCol.TMdcKalTrack.m_ferror_mu",
        "/Event:TDstEvent/m_mdcKalTrackCol.TMdcKalTrack.m_ferror_k",
        "/Event:TDstEvent/m_mdcKalTrackCol.TMdcKalTrack.m_ferror_p",
        "/Event:TEvtRecObject/m_evtRecVeeVertexCol.TEvtRecVeeVertex.m_Ew",
        "/Event:TEvtRecObject/m_evtRecPrimaryVertex.m_Evtx",  # TODO: use BES3 interpretation
        "/Event:TRecEvent/m_recMdcTrackCol.TRecMdcTrack.m_err",
        "/Event:TRecEvent/m_recEmcShowerCol.TRecEmcShower.m_err",
        "/Event:TRecEvent/m_recMdcKalTrackCol.TRecMdcKalTrack.m_terror",
    }

    @classmethod
    def priority(cls):
        return 40

    @classmethod
    def build_factory(
        cls,
        top_type_name,
        cur_streamer_info,
        all_streamer_info,
        item_path,
        **kwargs,
    ):
        if item_path not in Bes3SymMatrixArrayFactory.target_items:
            return None

        fArrayDim = cur_streamer_info["fArrayDim"]
        fMaxIndex = cur_streamer_info["fMaxIndex"]
        dtype = PrimitiveFactory.typename2dtype[top_type_name]

        flat_size = np.prod(fMaxIndex[:fArrayDim])
        assert flat_size > 0, f"flatten_size should be greater than 0, but got {flat_size}"

        full_dim = int((np.sqrt(1 + 8 * flat_size) - 1) / 2)

        return cls(
            name=cur_streamer_info["fName"],
            dtype=dtype,
            flat_size=flat_size,
            full_dim=full_dim,
        )

    def __init__(self, name: str, dtype: str, flat_size: int, full_dim: int):
        super().__init__(name)
        assert dtype == "float64", "Only float64 symmetric matrix is supported."
        self.dtype = dtype
        self.flat_size = flat_size
        self.full_dim = full_dim

    def build_cpp_reader(self):
        return bcpp.Bes3SymMatrixArrayReader(self.name, self.flat_size, self.full_dim)

    def build_python_reader(self):
        return Bes3PySymMatrixArrayReader(self.name, self.flat_size, self.full_dim)

    def make_awkward_content(self, raw_data: np.ndarray):
        return awkward.contents.NumpyArray(raw_data.reshape(-1, self.full_dim, self.full_dim))

    def make_awkward_form(self):
        return awkward.forms.NumpyForm(self.dtype, inner_shape=[self.full_dim, self.full_dim])


uproot_custom.registered_factories |= {
    Bes3TObjArrayFactory,
    Bes3SymMatrixArrayFactory,
    Bes3CgemClusterColFactory,
    Bes3BaseObjectFactory,
}


##########################################################################################
#                                     Array Preprocess
##########################################################################################


#############################################
# TDigiEvent
#############################################
def process_digi_subbranch(org_arr: ak.Array) -> ak.Array:
    """
    Processes the `TRawData` subbranch of the input awkward array and returns a new array with the subbranch fields
    merged into the top level.

    Parameters:
        org_arr (ak.Array): The input awkward array containing the `TRawData` subbranch.

    Returns:
        A new awkward array with the fields of `TRawData` merged into the top level.

    Raises:
        AssertionError: If `TRawData` is not found in the input array fields.
    """
    if not org_arr.fields:
        assert ak.count(org_arr) == 0, "Input array is empty but has no fields"
        return org_arr

    assert "TRawData" in org_arr.fields, "TRawData not found in the input array"

    fields = {}
    for field_name in org_arr.fields:
        if field_name == "TRawData":
            for raw_field_name in org_arr[field_name].fields:
                fields[raw_field_name] = org_arr[field_name][raw_field_name]
        else:
            fields[field_name] = org_arr[field_name]

    return ak.zip(fields)


#############################################
# Main function
#############################################
def preprocess_subbranch(full_branch_path: str, org_arr: ak.Array) -> ak.Array:
    full_branch_path = full_branch_path.replace("/Event:", "")
    evt_name, subbranch_name = full_branch_path.split("/")

    if evt_name == "TDigiEvent" and subbranch_name != "m_fromMc":
        return process_digi_subbranch(org_arr)

    # Default return
    return org_arr


class Bes3Interpretation(AsCustom):
    """
    Custom interpretation for Bes3 data.
    """

    target_branches: set[str] = set(bes3_branch2types.keys())

    def __init__(self, branch, context, simplify):
        super().__init__(branch, context, simplify)
        self._typename = bes3_branch2types[regularize_object_path(branch.object_path)]
        self.is_bes3 = self._typename is not None

        if self.is_bes3:
            self._typename = f"TObjArray<{self._typename}>"

    def final_array(
        self,
        basket_arrays,
        entry_start,
        entry_stop,
        entry_offsets,
        library,
        branch,
        options,
    ):
        arr = super().final_array(
            basket_arrays,
            entry_start,
            entry_stop,
            entry_offsets,
            library,
            branch,
            options,
        )

        # preprocess awkward array and return
        full_branch_path = regularize_object_path(branch.object_path)
        return preprocess_subbranch(full_branch_path, arr)

    def __repr__(self) -> str:
        """
        The string representation of the interpretation.
        """
        if self.is_bes3:
            return f"AsBes3({self._typename})"
        return super().__repr__()


uproot.register_interpretation(Bes3Interpretation)
