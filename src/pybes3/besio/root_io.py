import awkward as ak
import awkward.contents
import awkward.index
import numpy as np
import uproot
import uproot.behaviors.TBranch
import uproot.extras
import uproot.interpretation
import uproot_custom
from uproot_custom import (
    AsCustom,
    BaseReader,
    BasicTypeReader,
    EmptyReader,
    BaseObjectReader,
    gen_tree_config,
    get_cpp_reader,
    reconstruct_array,
    regularize_object_path,
)

from . import besio_cpp as bcpp


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
    "/Event:EventNavigator/m_mcMdcMcHits": "map<int,int>",
    "/Event:EventNavigator/m_mcMdcTracks": "map<int,int>",
    "/Event:EventNavigator/m_mcEmcMcHits": "map<int,int>",
    "/Event:EventNavigator/m_mcEmcRecShowers": "map<int,int>",
}


class Bes3TObjArrayReader(BaseReader):
    @classmethod
    def priority(cls):
        return 50

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name: str,
        cls_streamer_info: dict,
        all_streamer_info: dict,
        item_path: str,
        called_from_top: bool,
    ):
        if top_type_name != "TObjArray":
            return None

        item_path = item_path.replace(".TObjArray*", "")
        obj_typename = bes3_branch2types.get(item_path)
        if obj_typename is None:
            return None

        if obj_typename not in all_streamer_info:
            return {
                "reader": cls,
                "name": cls_streamer_info["fName"],
                "element_reader": {
                    "reader": EmptyReader,
                    "name": obj_typename,
                },
            }

        sub_reader_config = []
        for s in all_streamer_info[obj_typename]:
            sub_reader_config.append(
                gen_tree_config(
                    cls_streamer_info=s,
                    all_streamer_info=all_streamer_info,
                    item_path=f"{item_path}.{obj_typename}",
                )
            )

        return {
            "reader": cls,
            "name": cls_streamer_info["fName"],
            "element_reader": {
                "reader": BaseObjectReader,
                "name": obj_typename,
                "sub_readers": sub_reader_config,
            },
        }

    @classmethod
    def get_cpp_reader(cls, reader_config: dict):
        if reader_config["reader"] != cls:
            return None

        element_reader_config = reader_config["element_reader"]
        element_reader = get_cpp_reader(element_reader_config)

        return bcpp.Bes3TObjArrayReader(reader_config["name"], element_reader)

    @classmethod
    def reconstruct_array(cls, raw_data, reader_config: dict):
        if reader_config["reader"] != cls:
            return None

        offsets, element_raw_data = raw_data
        element_reader_config = reader_config["element_reader"]
        element_data = reconstruct_array(
            element_raw_data,
            element_reader_config,
        )

        return awkward.contents.ListOffsetArray(
            awkward.index.Index64(offsets),
            element_data,
        )


class Bes3CgemClusterColReader(BaseReader):
    @classmethod
    def priority(cls):
        return 55

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name,
        cls_streamer_info,
        all_streamer_info,
        item_path,
        called_from_top: bool,
    ):
        item_path = item_path.replace(".TObjArray*", "")
        if item_path != "/Event:TRecEvent/m_recCgemClusterCol":
            return None

        if all_streamer_info.get("TCgemCluster") is not None:
            return None  # Let Bes3TObjArrayReader handle it

        return {
            "reader": cls,
            "name": cls_streamer_info["fName"],
        }

    @classmethod
    def get_cpp_reader(cls, tree_config):
        if tree_config["reader"] != cls:
            return None

        return bcpp.Bes3CgemClusterColReader(tree_config["name"])

    @classmethod
    def reconstruct_array(cls, raw_data, tree_config):
        if tree_config["reader"] != cls:
            return None

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


class Bes3SymMatrixArrayReader(BaseReader):
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
    def gen_tree_config(
        cls,
        top_type_name,
        cls_streamer_info,
        all_streamer_info,
        item_path,
        called_from_top: bool,
    ):
        if item_path not in Bes3SymMatrixArrayReader.target_items:
            return None

        fArrayDim = cls_streamer_info["fArrayDim"]
        fMaxIndex = cls_streamer_info["fMaxIndex"]
        ctype = BasicTypeReader.typenames[top_type_name]

        flat_size = np.prod(fMaxIndex[:fArrayDim])
        assert flat_size > 0, f"flatten_size should be greater than 0, but got {flat_size}"

        full_dim = int((np.sqrt(1 + 8 * flat_size) - 1) / 2)
        return {
            "reader": cls,
            "name": cls_streamer_info["fName"],
            "ctype": ctype,
            "flat_size": flat_size,
            "full_dim": full_dim,
        }

    @classmethod
    def get_cpp_reader(cls, tree_config):
        if tree_config["reader"] != cls:
            return None

        ctype = tree_config["ctype"]
        assert ctype == "d", "Only double precision symmetric matrix is supported."

        return bcpp.Bes3SymMatrixArrayReader(
            tree_config["name"],
            tree_config["flat_size"],
            tree_config["full_dim"],
        )

    @classmethod
    def reconstruct_array(cls, raw_data, tree_config):
        if tree_config["reader"] != cls:
            return None

        full_dim = tree_config["full_dim"]
        return awkward.contents.NumpyArray(raw_data.reshape(-1, full_dim, full_dim))


uproot_custom.registered_readers |= {
    Bes3TObjArrayReader,
    Bes3SymMatrixArrayReader,
    Bes3CgemClusterColReader,
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

    def basket_array(
        self,
        data,
        byte_offsets,
        basket,
        branch,
        context,
        cursor_offset,
        library,
        interp_options,
    ):
        raw_ak_layout = super().basket_array(
            data,
            byte_offsets,
            basket,
            branch,
            context,
            cursor_offset,
            library,
            interp_options,
        )
        raw_ak_arr = ak.Array(raw_ak_layout)

        # preprocess awkward array and return
        full_branch_path = regularize_object_path(branch.object_path)
        return preprocess_subbranch(full_branch_path, raw_ak_arr)

    @property
    def typename(self) -> str:
        """
        The typename of the interpretation.
        """
        return self._typename

    def __repr__(self) -> str:
        """
        The string representation of the interpretation.
        """
        return f"AsBes3(TObjArray[{self.typename}])"


##########################################################################################
#                                       Wrappers
##########################################################################################
_is_uproot_interpretation_of_wrapped = False

_uproot_interpretation_of = uproot.interpretation.identify.interpretation_of


def bes_interpretation_of(
    branch: uproot.behaviors.TBranch.TBranch, context: dict, simplify: bool = True
) -> uproot.interpretation.Interpretation:
    if not hasattr(branch, "parent"):
        return _uproot_interpretation_of(branch, context, simplify)

    if Bes3Interpretation.match_branch(branch, context, simplify):
        return Bes3Interpretation(branch, context, simplify)

    return _uproot_interpretation_of(branch, context, simplify)


def wrap_uproot_interpretation():
    global _is_uproot_interpretation_of_wrapped
    if not _is_uproot_interpretation_of_wrapped:
        _is_uproot_interpretation_of_wrapped = True
        uproot.interpretation.identify.interpretation_of = bes_interpretation_of


def wrap_uproot():
    """
    Wraps the uproot functions to use the BES interpretation.
    """
    wrap_uproot_interpretation()
