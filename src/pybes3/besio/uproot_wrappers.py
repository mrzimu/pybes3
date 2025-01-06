from collections import deque

import awkward as ak
import awkward.contents
import awkward.index
import numpy as np
import uproot
import uproot.behaviors
import uproot.behaviors.TBranch
import uproot.interpretation
import uproot.interpretation.identify
import uproot.interpretation.library
from uproot.models.TBranch import Model_TBranchElement

from .besio_cpp import read_bes_stl, read_bes_tobjarray, read_bes_tobject

##########################################################################################
#                                       Constants
##########################################################################################
kBASE = "BASE"
kCtype = "ctype"
kTString = "TString"
kVector = "vector"
kList = "list"
kDeque = "deque"
kMap = "map"
kSet = "set"
kMultiMap = "multimap"
kMultiSet = "multiset"

kTArrayC = "TArrayC"
kTArrayS = "TArrayS"
kTArrayI = "TArrayI"
kTArrayL = "TArrayL"
kTArrayF = "TArrayF"
kTArrayD = "TArrayD"

CTYPE_NAMES = {
    "bool",
    "char",
    "short",
    "int",
    "long",
    "float",
    "double",
    "unsigned char",
    "unsigned short",
    "unsigned int",
    "unsigned long",
}

STL_NAMES = {kVector, kList, kDeque, kMap, kSet, kMultiMap, kMultiSet}

TARRAY_NAMES = {kTArrayC, kTArrayS, kTArrayI, kTArrayL, kTArrayF, kTArrayD}

BES_BRANCH_NAMES = {
    "TEvtHeader",
    "TMcEvent",
    "TDigiEvent",
    "TDstEvent",
    "TRecEvent",
    "TEvtRecObject",
    "THltEvent",
}

kFallBack = "fallback"
kTObjArray = "TObjArray"
kTObject = "TObject"
kSTL = "STL"
branchname_to_element_type = {
    "TEvtHeader/m_eventId": (kFallBack, None),
    "TEvtHeader/m_runId": (kFallBack, None),
    "TEvtHeader/m_time": (kFallBack, None),
    "TEvtHeader/m_eventTag": (kFallBack, None),
    "TEvtHeader/m_flag1": (kFallBack, None),
    "TEvtHeader/m_flag2": (kFallBack, None),
    "TEvtHeader/m_etsT1": (kFallBack, None),
    "TEvtHeader/m_etsT2": (kFallBack, None),
    # multimap and map are the same
    "EventNavigator/m_mcMdcMcHits": (kSTL, "map<int,int>"),
    "EventNavigator/m_mcMdcTracks": (kSTL, "map<int,int>"),
    "EventNavigator/m_mcEmcMcHits": (kSTL, "map<int,int>"),
    "EventNavigator/m_mcEmcRecShowers": (kSTL, "map<int,int>"),
    "TMcEvent/m_mdcMcHitCol": (kTObjArray, "TMdcMc"),
    "TMcEvent/m_cgemMcHitCol": (kTObjArray, "TCgemMc"),
    "TMcEvent/m_emcMcHitCol": (kTObjArray, "TEmcMc"),
    "TMcEvent/m_tofMcHitCol": (kTObjArray, "TTofMc"),
    "TMcEvent/m_mucMcHitCol": (kTObjArray, "TMucMc"),
    "TMcEvent/m_mcParticleCol": (kTObjArray, "TMcParticle"),
    "TDigiEvent/m_fromMc": (kFallBack, None),
    "TDigiEvent/m_mdcDigiCol": (kTObjArray, "TMdcDigi"),
    "TDigiEvent/m_cgemDigiCol": (kTObjArray, "TCgemDigi"),
    "TDigiEvent/m_emcDigiCol": (kTObjArray, "TEmcDigi"),
    "TDigiEvent/m_tofDigiCol": (kTObjArray, "TTofDigi"),
    "TDigiEvent/m_mucDigiCol": (kTObjArray, "TMucDigi"),
    "TDigiEvent/m_lumiDigiCol": (kTObjArray, "TLumiDigi"),
    "TDstEvent/m_emcTrackCol": (kTObjArray, "TEmcTrack"),
    "TDstEvent/m_mdcTrackCol": (kTObjArray, "TMdcTrack"),
    "TDstEvent/m_tofTrackCol": (kTObjArray, "TTofTrack"),
    "TDstEvent/m_mucTrackCol": (kTObjArray, "TMucTrack"),
    "TDstEvent/m_mdcDedxCol": (kTObjArray, "TMdcDedx"),
    "TDstEvent/m_extTrackCol": (kTObjArray, "TExtTrack"),
    "TDstEvent/m_mdcKalTrackCol": (kTObjArray, "TMdcKalTrack"),
    "TRecEvent/m_recMdcTrackCol": (kTObjArray, "TRecMdcTrack"),
    "TRecEvent/m_recMdcHitCol": (kTObjArray, "TRecMdcHit"),
    "TRecEvent/m_recEmcHitCol": (kTObjArray, "TRecEmcHit"),
    "TRecEvent/m_recEmcClusterCol": (kTObjArray, "TRecEmcCluster"),
    "TRecEvent/m_recEmcShowerCol": (kTObjArray, "TRecEmcShower"),
    "TRecEvent/m_recTofTrackCol": (kTObjArray, "TRecTofTrack"),
    "TRecEvent/m_recMucTrackCol": (kTObjArray, "TRecMucTrack"),
    "TRecEvent/m_recMdcDedxCol": (kTObjArray, "TRecMdcDedx"),
    "TRecEvent/m_recMdcDedxHitCol": (kTObjArray, "TRecMdcDedxHit"),
    "TRecEvent/m_recExtTrackCol": (kTObjArray, "TRecExtTrack"),
    "TRecEvent/m_recMdcKalTrackCol": (kTObjArray, "TRecMdcKalTrack"),
    "TRecEvent/m_recMdcKalHelixSegCol": (kTObjArray, "TRecMdcKalHelixSeg"),
    "TRecEvent/m_recEvTimeCol": (kTObjArray, "TRecEvTime"),
    "TRecEvent/m_recZddChannelCol": (kTObjArray, "TRecZddChannel"),
    # This is an TObject, not a TObjArray
    "TEvtRecObject/m_evtRecEvent": (kTObject, "TEvtRecEvent"),
    "TEvtRecObject/m_evtRecTrackCol": (kTObjArray, "TEvtRecDTag"),
    # This is an TObject, not a TObjArray
    "TEvtRecObject/m_evtRecPrimaryVertex": (kTObject, "TEvtRecPrimaryVertex"),
    "TEvtRecObject/m_evtRecVeeVertexCol": (kTObjArray, "TEvtRecDTag"),
    "TEvtRecObject/m_evtRecPi0Col": (kTObjArray, "TEvtRecDTag"),
    "TEvtRecObject/m_evtRecEtaToGGCol": (kTObjArray, "TEvtRecDTag"),
    "TEvtRecObject/m_evtRecDTagCol": (kTObjArray, "TEvtRecDTag"),
    "THltEvent/m_hltRawCol": (kTObjArray, "THltRaw"),
    # This is an TObject, not a TObjArray
    "THltEvent/m_hltInf": (kTObject, "THltInf"),
    # This is an TObject, not a TObjArray
    "THltEvent/m_dstHltInf": (kTObject, "TDstHltInf"),
}


##########################################################################################
#                                 C++ output to awkward
##########################################################################################


def get_top_type_name(type_name: str) -> str:
    if type_name in CTYPE_NAMES:
        return kCtype

    elif "<" in type_name:
        top_type_name = type_name.split("<")[0]
        if top_type_name in STL_NAMES:
            return top_type_name
        else:
            raise NotImplementedError(f"Unsupported type_name: {type_name}")

    elif type_name == kTString:
        return kTString

    else:
        return type_name


def get_vector_subtype(type_name: str) -> str:
    assert type_name.startswith("vector<") and type_name.endswith(
        ">"
    ), f"Unsupported type_name: {type_name}"
    return type_name[7:-1].strip()


def get_map_subtypes(type_name: str) -> tuple[str, str]:
    assert type_name.startswith("map<") and type_name.endswith(
        ">"
    ), f"Unsupported type_name: {type_name}"

    pos_split = 0
    n_level = 0
    for i, c in enumerate(type_name):
        if c == "<":
            n_level += 1
        elif c == ">":
            n_level -= 1
        if n_level == 1 and c == ",":
            pos_split = i
            break

    assert pos_split != 0, f"Unsupported type_name: {type_name}"
    return type_name[4:pos_split].strip(), type_name[pos_split + 1: -1].strip()


def recover_basic_element(
    streamer_info: dict, org_data: tuple, all_streamer_info: dict
) -> awkward.contents.Content:
    fTypeName = streamer_info["fTypeName"]
    fName = streamer_info["fName"]
    top_type_name = get_top_type_name(fTypeName)

    if "fArrayDim" in streamer_info and streamer_info["fArrayDim"] > 0:
        fMaxIndex = streamer_info["fMaxIndex"]

        new_info = streamer_info.copy()
        new_info["fArrayDim"] = 0

        flat_content = recover_basic_element(new_info, org_data, all_streamer_info)
        shape = deque(fMaxIndex[fMaxIndex > 0].tolist())
        return recover_array_shape(flat_content, shape)

    if top_type_name == kCtype:
        return awkward.contents.NumpyArray(org_data[0])

    elif top_type_name == kTString:
        offset, data = org_data
        return awkward.contents.ListOffsetArray(
            awkward.index.Index(offset),
            awkward.contents.NumpyArray(data.view(np.uint8), parameters={"__array__": "char"}),
            parameters={"__array__": "string"},
        )

    elif top_type_name in STL_NAMES:
        if top_type_name == kVector:
            element_type = get_vector_subtype(fTypeName)
            element_info = {
                "fName": fName + "_element",
                "fTypeName": element_type,
                "fType": -1,
            }

            offsets, sub_org_data = org_data
            sub_content = recover_basic_element(element_info, sub_org_data, all_streamer_info)

            return awkward.contents.ListOffsetArray(awkward.index.Index(offsets), sub_content)

        elif top_type_name == kMap or top_type_name == kMultiMap:
            key_type, val_type = get_map_subtypes(fTypeName)

            key_info = {"fName": fName + "_key", "fTypeName": key_type, "fType": -1}
            val_info = {"fName": fName + "_val", "fTypeName": val_type, "fType": -1}

            offset, key_org_data, val_org_data = org_data

            key_content = recover_basic_element(key_info, key_org_data, all_streamer_info)
            val_content = recover_basic_element(val_info, val_org_data, all_streamer_info)

            return awkward.contents.ListOffsetArray(
                awkward.index.Index(offset),
                awkward.contents.RecordArray([key_content, val_content], ["key", "val"]),
            )
        else:
            raise NotImplementedError(f"Unsupported STL type: {top_type_name}")

    elif top_type_name == kBASE:
        fType = streamer_info["fType"]
        if fType == 66:
            return None

        elif fType == 0:
            sub_streamers = all_streamer_info[fName]
            sub_field_names = []
            sub_field_contents = []
            for s_info, s_data in zip(sub_streamers, org_data):
                sub_content = recover_basic_element(s_info, s_data, all_streamer_info)
                sub_name = s_info["fName"]

                # skip TObject result
                if sub_content is not None:
                    sub_field_contents.append(sub_content)
                    sub_field_names.append(sub_name)
            return awkward.contents.RecordArray(sub_field_contents, sub_field_names)

        else:
            raise NotImplementedError(f"Unsupported fType: {fType}")

    elif top_type_name in TARRAY_NAMES:
        offsets, sub_org_data = org_data
        return awkward.contents.ListOffsetArray(
            awkward.index.Index(offsets), awkward.contents.NumpyArray(sub_org_data)
        )

    else:
        sub_streamers = all_streamer_info[top_type_name]
        sub_field_names = []
        sub_field_contents = []
        for s_info, s_data in zip(sub_streamers, org_data):
            sub_content = recover_basic_element(s_info, s_data, all_streamer_info)
            sub_name = s_info["fName"]

            # skip TObject result
            if sub_content is not None:
                sub_field_contents.append(sub_content)
                sub_field_names.append(sub_name)

        return awkward.contents.RecordArray(sub_field_contents, sub_field_names)


def recover_array_shape(
    content: awkward.contents.Content, shape: deque[int]
) -> awkward.contents.Content:
    cur_shape = shape.popleft()
    if len(shape) > 0:
        content = recover_array_shape(content, shape)
    return awkward.contents.RegularArray(content, cur_shape)


def tobjarray_np2ak(
    element_type_name: str, org_array_dict: dict, all_streamer_info: dict
) -> awkward.Array:
    org_data_tuple: tuple = org_array_dict["data"]
    obj_offsets: np.ndarray = org_array_dict["obj_offsets"]
    element_streamer_info = all_streamer_info[element_type_name]

    field_names = []
    field_contents = []
    for s, org_data in zip(element_streamer_info, org_data_tuple):
        element_content = recover_basic_element(s, org_data, all_streamer_info)
        if element_content is None:
            continue

        # Make object-offsets, then it's event-by-event array
        evt_contents = awkward.contents.ListOffsetArray(
            awkward.index.Index(obj_offsets), element_content
        )

        field_names.append(s["fName"])
        field_contents.append(evt_contents)

    return awkward.Array(awkward.contents.RecordArray(field_contents, field_names))


def tobject_np2ak(
    org_data_list: tuple, streamer_members_info: list[dict], all_streamer_info: dict
) -> awkward.Array:
    field_names = []
    field_contents = []
    for s, org_data in zip(streamer_members_info, org_data_list):
        fTypeName = s["fTypeName"]
        fArrayDim = s["fArrayDim"]

        if fTypeName == kBASE:
            assert (
                s["fType"] == 65
            ), f'fTypeName is "BASE" but fType is not TString: {s}'  # TString's fType is 65
            continue

        # Recover pure c-types array to "element" array
        element_content = recover_basic_element(fTypeName, org_data)

        if fArrayDim > 0:
            fMaxIndex = s["fMaxIndex"]
            shape = deque(fMaxIndex[fMaxIndex > 0].tolist())
            element_content = recover_array_shape(element_content, shape)

        field_names.append(s["fName"])
        field_contents.append(element_content)

    return awkward.Array(awkward.contents.RecordArray(field_contents, field_names))


def stl_np2ak(org_data: tuple, type_name: str, all_streamer_info: dict) -> awkward.Array:
    tmp_info = {
        "fName": "tmp",
        "fTypeName": type_name,
        "fType": -1,
    }
    element_content = recover_basic_element(tmp_info, org_data, all_streamer_info)
    return awkward.Array(element_content)


##########################################################################################
#                                      Interpretation
##########################################################################################


class BesInterpretation(uproot.interpretation.Interpretation):
    def __init__(self, full_branch_name: str) -> None:
        super().__init__()

        self.full_branch_name = full_branch_name
        self.parse_rule, self.element_type_name = branchname_to_element_type[full_branch_name]

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
        basket_entry_starts = np.array(entry_offsets[:-1])
        basket_entry_stops = np.array(entry_offsets[1:])

        basket_start_idx = np.where(basket_entry_starts <= entry_start)[0].max()
        basket_end_idx = np.where(basket_entry_stops >= entry_stop)[0].min()

        arr_to_concat = [basket_arrays[i] for i in range(basket_start_idx, basket_end_idx + 1)]
        tot_array = ak.concatenate(arr_to_concat)

        relative_entry_start = entry_start - basket_entry_starts[basket_start_idx]
        relative_entry_stop = entry_stop - basket_entry_starts[basket_start_idx]

        return tot_array[relative_entry_start:relative_entry_stop]

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return f"BES::As({self.typename})"

    @property
    def cache_key(self):
        return str(self.__class__)

    @property
    def typename(self):
        res = "BES::"
        if self.parse_rule == kTObjArray:
            res += f"TObjArray<{self.element_type_name}>"
        elif self.parse_rule == kTObject:
            res += self.element_type_name
        elif self.parse_rule == kSTL:
            res += self.element_type_name
        else:
            raise NotImplementedError(
                f"Unsupported parse_rule: {self.parse_rule}, {self.element_type_name}"
            )
        return res

    def basket_array(
        self,
        data: np.ndarray,
        byte_offsets: np.ndarray,
        basket,
        branch: Model_TBranchElement,
        context,
        cursor_offset,
        library,
        options,
    ):

        # For BES TObject and TObjArray, element class streamers are needed
        # Check streamers and versions
        if self.parse_rule == kTObjArray or self.parse_rule == kTObject:
            obj_streamer = branch.file.streamers.get(self.element_type_name)
            if obj_streamer is None:
                raise ValueError(
                    f"Streamer for {self.element_type_name} not found, maybe this branch is empty?"
                )

            obj_versions = list(obj_streamer.keys())
            assert (
                len(obj_versions) == 1
            ), "Only one version of streamer is supported. Maybe you mixed data from different versions?"

        def get_streamer_list(type_name: str) -> list[dict]:
            return [
                i.all_members
                for i in list(branch.file.streamers[type_name].values())[0].member("fElements")
            ]

        all_streamer_info = {k: get_streamer_list(k) for k in branch.file.streamers.keys()}

        if self.parse_rule == kTObjArray:
            org_data = read_bes_tobjarray(
                data, byte_offsets, self.element_type_name, all_streamer_info
            )
        elif self.parse_rule == kTObject:
            org_data = read_bes_tobject(
                data, byte_offsets, self.element_type_name, all_streamer_info
            )
        elif self.parse_rule == kSTL:
            org_data = read_bes_stl(
                data, byte_offsets, self.element_type_name, all_streamer_info
            )
        else:
            raise NotImplementedError(
                f"Unsupported parse_rule: {self.parse_rule}, {self.element_type_name}"
            )

        if isinstance(library, uproot.interpretation.library.NumPy):
            raise NotImplementedError("Numpy library is not supported")

        if isinstance(library, uproot.interpretation.library.Pandas):
            raise NotImplementedError("Pandas library is not supported")

        assert isinstance(library, uproot.interpretation.library.Awkward), (
            "Unknown library: %s" % library
        )

        if self.parse_rule == kTObjArray:
            return tobjarray_np2ak(self.element_type_name, org_data, all_streamer_info)
        elif self.parse_rule == kTObject:
            return tobject_np2ak(self.element_type_name, org_data, all_streamer_info)
        elif self.parse_rule == kSTL:
            return stl_np2ak(org_data, self.element_type_name, all_streamer_info)
        else:
            raise NotImplementedError(
                f"Unsupported parse_rule: {self.parse_rule}, {self.element_type_name}"
            )


##########################################################################################
#                                       Wrappers
##########################################################################################
_is_TBranchElement_branches_wrapped = False
_is_uproot_interpretation_of_wrapped = False

_uproot_interpretation_of = uproot.interpretation.identify.interpretation_of


def bes_interpretation_of(
    branch: uproot.behaviors.TBranch.TBranch, context: dict, simplify: bool = True
) -> uproot.interpretation.Interpretation:
    if not hasattr(branch, "parent"):
        return _uproot_interpretation_of(branch, context, simplify)

    parent_name = branch.parent.name
    full_branch_name = f"{parent_name}/{branch.name}"

    if full_branch_name not in branchname_to_element_type.keys():
        return _uproot_interpretation_of(branch, context, simplify)

    if branchname_to_element_type[full_branch_name][0] == kFallBack:
        return _uproot_interpretation_of(branch, context, simplify)

    return BesInterpretation(full_branch_name=full_branch_name)


def wrap_uproot_interpretation():
    global _is_uproot_interpretation_of_wrapped
    if not _is_uproot_interpretation_of_wrapped:
        _is_uproot_interpretation_of_wrapped = True
        uproot.interpretation.identify.interpretation_of = bes_interpretation_of


def wrap_uproot_TBranchElement_branches():
    def branches(self):
        if self.name not in BES_BRANCH_NAMES:
            return self.member("fBranches")
        else:
            res = []
            for br in self.member("fBranches"):
                if br.name == "TObject":
                    continue

                interpret_type, class_name = branchname_to_element_type[
                    f"{self.name}/{br.name}"
                ]
                if interpret_type == kFallBack or class_name in self.file.streamers:
                    res.append(br)
                else:
                    continue
            return res

    global _is_TBranchElement_branches_wrapped
    if not _is_TBranchElement_branches_wrapped:
        _is_TBranchElement_branches_wrapped = True
        uproot.models.TBranch.Model_TBranchElement.branches = property(branches)
        for v in uproot.models.TBranch.Model_TBranchElement.known_versions.values():
            v.branches = property(branches)


def wrap_uproot():
    wrap_uproot_interpretation()
    wrap_uproot_TBranchElement_branches()
