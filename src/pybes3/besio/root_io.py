import re
from enum import Enum
from typing import Literal, Union

import awkward as ak
import awkward.contents
import awkward.index
import numpy as np
import uproot
import uproot.behaviors.TBranch
import uproot.extras
import uproot.interpretation

from .._utils import _extract_index, _flat_to_numpy, _recover_shape
from . import besio_cpp as bcpp

type_np2array = {
    "u1": "B",
    "u2": "H",
    "u4": "I",
    "u8": "Q",
    "i1": "b",
    "i2": "h",
    "i4": "i",
    "i8": "q",
    "f": "f",
    "d": "d",
}

num_typenames = {
    "bool": "i1",
    "char": "i1",
    "short": "i2",
    "int": "i4",
    "long": "i8",
    "unsigned char": "u1",
    "unsigned short": "u2",
    "unsigned int": "u4",
    "unsigned long": "u8",
    "float": "f",
    "double": "d",
    # cstdint
    "int8_t": "i1",
    "int16_t": "i2",
    "int32_t": "i4",
    "int64_t": "i8",
    "uint8_t": "u1",
    "uint16_t": "u2",
    "uint32_t": "u4",
    "uint64_t": "u8",
    # ROOT types
    "Bool_t": "i1",
    "Char_t": "i1",
    "Short_t": "i2",
    "Int_t": "i4",
    "Long_t": "i8",
    "UChar_t": "u1",
    "UShort_t": "u2",
    "UInt_t": "u4",
    "ULong_t": "u8",
    "Float_t": "f",
    "Double_t": "d",
}

stl_typenames = {
    "vector",
    "array",
    "map",
    "unordered_map",
    "string",
    "multimap",
}


tarray_typenames = {
    "TArrayC": "i1",
    "TArrayS": "i2",
    "TArrayI": "i4",
    "TArrayL": "i8",
    "TArrayF": "f",
    "TArrayD": "d",
}

readers: set["BaseReader"] = set()


ctype_hints = Literal["bool", "i1", "i2", "i4", "i8", "u1", "u2", "u4", "u8", "f", "d"]


class ReaderType(Enum):
    CType = "CType"
    STLSequence = "STLSequence"
    STLMap = "STLMap"
    STLString = "STLString"
    TArray = "TArray"
    TString = "TString"
    TObject = "TObject"
    CArray = "CArray"
    BaseObject = "BaseObject"
    ObjectHeader = "ObjectHeader"
    Empty = "Empty"


def get_top_type_name(type_name: str) -> str:
    if type_name.endswith("*"):
        type_name = type_name[:-1].strip()
    type_name = type_name.replace("std::", "").strip()
    return type_name.split("<")[0]


def gen_tree_config(
    cls_streamer_info: dict,
    all_streamer_info: dict,
    item_path: str = "",
) -> dict:
    """
    Generate reader configuration for a class streamer information.

    The content it returns should be:

    ```python
    {
        "reader": ReaderType,
        "name": str,
        "ctype": str, # for CTypeReader, TArrayReader
        "element_reader": dict, # reader config of the element, for STLVectorReader, SimpleCArrayReader, TObjectCArrayReader
        "flat_size": int, # for SimpleCArrayReader, TObjectCArrayReader
        "fMaxIndex": list[int], # for SimpleCArrayReader, TObjectCArrayReader
        "fArrayDim": int, # for SimpleCArrayReader, TObjectCArrayReader
        "key_reader": dict, # reader config of the key, for STLMapReader
        "val_reader": dict, # reader config of the value, for STLMapReader
        "sub_readers": list[dict], # for BaseObjectReader, ObjectHeaderReader
        "is_top_level": bool, # for STLVectorReader, STLMapReader, STLStringReader
    }
    ```

    Args:
        cls_streamer_info (dict): Class streamer information.
        all_streamer_info (dict): All streamer information.
        item_path (str): Path to the item.

    Returns:
        dict: Reader configuration.
    """
    fName = cls_streamer_info["fName"]
    item_path = fName if item_path == "" else f"{item_path}.{fName}"

    for reader in sorted(readers, key=lambda x: x.priority(), reverse=True):
        top_type_name = get_top_type_name(cls_streamer_info["fTypeName"])
        tree_config = reader.gen_tree_config(
            top_type_name,
            cls_streamer_info,
            all_streamer_info,
            item_path,
        )
        if tree_config is not None:
            return tree_config

    raise ValueError(f"Unknown type: {cls_streamer_info['fTypeName']} for {item_path}")


def get_reader_instance(tree_config: dict):
    for cls_reader in sorted(readers, key=lambda x: x.priority(), reverse=True):
        reader = cls_reader.get_reader_instance(tree_config)
        if reader is not None:
            return reader

    raise ValueError(f"Unknown reader type: {tree_config['reader']} for {tree_config['name']}")


def reconstruct_array(
    raw_data: Union[np.ndarray, tuple, list, None],
    tree_config: dict,
) -> Union[ak.Array, None]:
    for reader in sorted(readers, key=lambda x: x.priority(), reverse=True):
        data = reader.reconstruct_array(raw_data, tree_config)
        if data is not None:
            return data

    raise ValueError(f"Unknown reader type: {tree_config['reader']} for {tree_config['name']}")


def gen_tree_config_from_type_name(
    type_name: str,
    all_streamer_info: dict,
    item_path: str = "",
):
    return gen_tree_config(
        {
            "fName": type_name,
            "fTypeName": type_name,
        },
        all_streamer_info,
        item_path,
    )


def regularize_object_path(object_path: str) -> str:
    return re.sub(r";[0-9]+", r"", object_path)


class BaseReader:
    """
    Base class for all readers.
    """

    @classmethod
    def priority(cls) -> int:
        """
        The priority of the reader. Higher priority means the reader will be
        used first.
        """
        return 20

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name: str,
        cls_streamer_info: dict,
        all_streamer_info: dict,
        item_path: str = "",
    ) -> dict:
        raise NotImplementedError("This method should be implemented in subclasses.")

    @classmethod
    def get_reader_instance(cls, tree_config: dict) -> bcpp.BaseReader:
        """
        Args:
            tree_config (dict): The configuration dictionary for the reader.

        Returns:
            An instance of the appropriate reader class.
        """
        raise NotImplementedError("This method should be implemented in subclasses.")

    @classmethod
    def reconstruct_array(
        cls,
        raw_data: Union[np.ndarray, tuple, list, None],
        tree_config: dict,
    ) -> Union[ak.Array, None]:
        """
        Args:
            raw_data (Union[np.ndarray, tuple, list, None]): The raw data to be
                recovered.
            tree_config (dict): The configuration dictionary for the reader.

        Returns:
            awkward.Array: The recovered data as an awkward array.
        """
        raise NotImplementedError("This method should be implemented in subclasses.")


class CTypeReader(BaseReader):
    """
    This class reads C++ primitive types from a binary parser.
    """

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name,
        cls_streamer_info,
        all_streamer_info,
        item_path,
    ):
        if top_type_name in num_typenames:
            ctype = num_typenames[top_type_name]
            return {
                "reader": ReaderType.CType,
                "name": cls_streamer_info["fName"],
                "ctype": ctype,
            }
        else:
            return None

    @classmethod
    def get_reader_instance(cls, tree_config: dict):
        if tree_config["reader"] != ReaderType.CType:
            return None

        ctype = tree_config["ctype"]
        return {
            "i1": bcpp.Int8Reader,
            "i2": bcpp.Int16Reader,
            "i4": bcpp.Int32Reader,
            "i8": bcpp.Int64Reader,
            "u1": bcpp.UInt8Reader,
            "u2": bcpp.UInt16Reader,
            "u4": bcpp.UInt32Reader,
            "u8": bcpp.UInt64Reader,
            "f": bcpp.FloatReader,
            "d": bcpp.DoubleReader,
        }[ctype](tree_config["name"])

    @classmethod
    def reconstruct_array(cls, raw_data, tree_config):
        if tree_config["reader"] != ReaderType.CType:
            return None
        return awkward.contents.NumpyArray(raw_data)


class STLSequenceReader(BaseReader):
    """
    This class reads STL sequence (vector, array) from a binary parser.
    """

    @staticmethod
    def get_sequence_element_typename(type_name: str) -> str:
        """
        Get the element type name of a vector type.

        e.g. vector<vector<int>> -> vector<int>
        """
        type_name = (
            type_name.replace("std::", "").replace("< ", "<").replace(" >", ">").strip()
        )
        return re.match(r"^(vector|array)<(.*)>$", type_name).group(2)

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name,
        cls_streamer_info,
        all_streamer_info,
        item_path,
    ):
        if top_type_name not in ["vector", "array"]:
            return None

        fName = cls_streamer_info["fName"]
        fTypeName = cls_streamer_info["fTypeName"]
        element_type = cls.get_sequence_element_typename(fTypeName)
        element_info = {
            "fName": fName,
            "fTypeName": element_type,
        }

        element_tree_config = gen_tree_config(
            element_info,
            all_streamer_info,
            item_path,
        )

        top_element_type = get_top_type_name(element_type)
        if top_element_type in stl_typenames:
            element_tree_config["is_top"] = False

        return {
            "reader": ReaderType.STLSequence,
            "name": fName,
            "element_reader": element_tree_config,
        }

    @classmethod
    def get_reader_instance(cls, tree_config: dict):
        if tree_config["reader"] != ReaderType.STLSequence:
            return None

        element_reader = get_reader_instance(tree_config["element_reader"])
        is_top = tree_config.get("is_top", True)
        return bcpp.STLSeqReader(tree_config["name"], is_top, element_reader)

    @classmethod
    def reconstruct_array(cls, raw_data, tree_config):
        if tree_config["reader"] != ReaderType.STLSequence:
            return None

        offsets, element_raw_data = raw_data
        element_data = reconstruct_array(
            element_raw_data,
            tree_config["element_reader"],
        )

        return awkward.contents.ListOffsetArray(
            awkward.index.Index64(offsets),
            element_data,
        )


class STLMapReader(BaseReader):
    """
    This class reads std::map from a binary parser.
    """

    @staticmethod
    def get_map_key_val_typenames(type_name: str) -> tuple[str, str]:
        """
        Get the key and value type names of a map type.

        e.g. map<int, vector<int>> -> (int, vector<int>)
        """
        type_name = (
            type_name.replace("std::", "").replace("< ", "<").replace(" >", ">").strip()
        )
        return re.match(r"^(map|unordered_map|multimap)<(.*),(.*)>$", type_name).groups()[1:3]

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name,
        cls_streamer_info,
        all_streamer_info,
        item_path,
    ):
        if top_type_name not in ["map", "unordered_map", "multimap"]:
            return None

        fTypeName = cls_streamer_info["fTypeName"]
        key_type_name, val_type_name = cls.get_map_key_val_typenames(fTypeName)

        fName = cls_streamer_info["fName"]
        key_info = {
            "fName": "key",
            "fTypeName": key_type_name,
        }

        val_info = {
            "fName": "val",
            "fTypeName": val_type_name,
        }

        key_tree_config = gen_tree_config(key_info, all_streamer_info, item_path)
        if get_top_type_name(key_type_name) in stl_typenames:
            key_tree_config["is_top"] = False

        val_tree_config = gen_tree_config(val_info, all_streamer_info, item_path)
        if get_top_type_name(val_type_name) in stl_typenames:
            val_tree_config["is_top"] = False

        return {
            "reader": ReaderType.STLMap,
            "name": fName,
            "key_reader": key_tree_config,
            "val_reader": val_tree_config,
        }

    @classmethod
    def get_reader_instance(cls, tree_config: dict):
        if tree_config["reader"] != ReaderType.STLMap:
            return None

        key_cpp_reader = get_reader_instance(tree_config["key_reader"])
        val_cpp_reader = get_reader_instance(tree_config["val_reader"])
        is_top = tree_config.get("is_top", True)
        return bcpp.STLMapReader(
            tree_config["name"],
            is_top,
            key_cpp_reader,
            val_cpp_reader,
        )

    @classmethod
    def reconstruct_array(cls, raw_data, tree_config):
        if tree_config["reader"] != ReaderType.STLMap:
            return None

        key_tree_config = tree_config["key_reader"]
        val_tree_config = tree_config["val_reader"]
        offsets, key_raw_data, val_raw_data = raw_data
        key_data = reconstruct_array(key_raw_data, key_tree_config)
        val_data = reconstruct_array(val_raw_data, val_tree_config)

        return awkward.contents.ListOffsetArray(
            awkward.index.Index64(offsets),
            awkward.contents.RecordArray(
                [key_data, val_data],
                [key_tree_config["name"], val_tree_config["name"]],
            ),
        )


class STLStringReader(BaseReader):
    """
    This class reads std::string from a binary parser.
    """

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name,
        cls_streamer_info,
        all_streamer_info,
        item_path,
    ):
        if top_type_name != "string":
            return None

        return {
            "reader": ReaderType.STLString,
            "name": cls_streamer_info["fName"],
        }

    @classmethod
    def get_reader_instance(cls, tree_config: dict):
        if tree_config["reader"] != ReaderType.STLString:
            return None

        return bcpp.STLStringReader(
            tree_config["name"],
            tree_config.get("is_top", True),
        )

    @classmethod
    def reconstruct_array(cls, raw_data, tree_config):
        if tree_config["reader"] != ReaderType.STLString:
            return None

        offsets, data = raw_data
        return awkward.contents.ListOffsetArray(
            awkward.index.Index64(offsets),
            awkward.contents.NumpyArray(data, parameters={"__array__": "char"}),
            parameters={"__array__": "string"},
        )


class TArrayReader(BaseReader):
    """
    This class reads TArray from a binary paerser.

    TArray includes TArrayC, TArrayS, TArrayI, TArrayL, TArrayF, and TArrayD.
    Corresponding ctype is u1, u2, i4, i8, f, and d.
    """

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name,
        cls_streamer_info,
        all_streamer_info,
        item_path,
    ):
        if top_type_name not in tarray_typenames:
            return None

        ctype = tarray_typenames[top_type_name]
        return {
            "reader": ReaderType.TArray,
            "name": cls_streamer_info["fName"],
            "ctype": ctype,
        }

    @classmethod
    def get_reader_instance(cls, tree_config: dict):
        if tree_config["reader"] != ReaderType.TArray:
            return None

        ctype = tree_config["ctype"]

        return {
            "i1": bcpp.TArrayCReader,
            "i2": bcpp.TArraySReader,
            "i4": bcpp.TArrayIReader,
            "i8": bcpp.TArrayLReader,
            "f": bcpp.TArrayFReader,
            "d": bcpp.TArrayDReader,
        }[ctype](tree_config["name"])

    @classmethod
    def reconstruct_array(cls, raw_data, tree_config):
        if tree_config["reader"] != ReaderType.TArray:
            return None

        offsets, data = raw_data
        return awkward.contents.ListOffsetArray(
            awkward.index.Index64(offsets),
            awkward.contents.NumpyArray(data),
        )


class TStringReader(BaseReader):
    """
    This class reads TString from a binary parser.
    """

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name,
        cls_streamer_info,
        all_streamer_info,
        item_path,
    ):
        if top_type_name != "TString":
            return None

        return {
            "reader": ReaderType.TString,
            "name": cls_streamer_info["fName"],
        }

    @classmethod
    def get_reader_instance(cls, tree_config: dict):
        if tree_config["reader"] != ReaderType.TString:
            return None

        return bcpp.TStringReader(tree_config["name"])

    @classmethod
    def reconstruct_array(cls, raw_data, tree_config):
        if tree_config["reader"] != ReaderType.TString:
            return None

        offsets, data = raw_data
        return awkward.contents.ListOffsetArray(
            awkward.index.Index64(offsets),
            awkward.contents.NumpyArray(data, parameters={"__array__": "char"}),
            parameters={"__array__": "string"},
        )


class TObjectReader(BaseReader):
    """
    This class reads TObject from a binary parser.

    It will not record any data.
    """

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name,
        cls_streamer_info,
        all_streamer_info,
        item_path,
    ):
        if top_type_name != "BASE":
            return None

        fType = cls_streamer_info["fType"]
        if fType != 66:
            return None

        return {
            "reader": ReaderType.TObject,
            "name": cls_streamer_info["fName"],
        }

    @classmethod
    def get_reader_instance(cls, tree_config: dict):
        if tree_config["reader"] != ReaderType.TObject:
            return None

        return bcpp.TObjectReader(tree_config["name"])

    @classmethod
    def reconstruct_array(cls, raw_data, tree_config):
        return None


class CArrayReader(BaseReader):
    """
    This class reads a C-array from a binary parser.
    """

    @classmethod
    def priority(cls):
        return 100  # This reader should be called first

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name,
        cls_streamer_info,
        all_streamer_info,
        item_path,
    ):
        if cls_streamer_info.get("fArrayDim", 0) == 0:
            return None

        fName = cls_streamer_info["fName"]
        fTypeName = cls_streamer_info["fTypeName"]
        fArrayDim = cls_streamer_info["fArrayDim"]
        fMaxIndex = cls_streamer_info["fMaxIndex"]

        element_streamer_info = cls_streamer_info.copy()
        element_streamer_info["fArrayDim"] = 0

        element_tree_config = gen_tree_config(
            element_streamer_info,
            all_streamer_info,
        )

        flat_size = np.prod(fMaxIndex[:fArrayDim])
        assert flat_size > 0, f"flatten_size should be greater than 0, but got {flat_size}"

        # c-type number or TArray
        if top_type_name in num_typenames or top_type_name in tarray_typenames:
            return {
                "reader": ReaderType.CArray,
                "name": fName,
                "is_obj": False,
                "element_reader": element_tree_config,
                "flat_size": flat_size,
                "fMaxIndex": fMaxIndex,
                "fArrayDim": fArrayDim,
            }

        # TSTring
        elif top_type_name == "TString":
            return {
                "reader": ReaderType.CArray,
                "name": fName,
                "is_obj": True,
                "element_reader": element_tree_config,
                "flat_size": flat_size,
                "fMaxIndex": fMaxIndex,
                "fArrayDim": fArrayDim,
            }

        # STL
        elif top_type_name in stl_typenames:
            element_tree_config["is_top"] = False
            return {
                "reader": ReaderType.CArray,
                "name": fName,
                "is_obj": True,
                "flat_size": flat_size,
                "element_reader": element_tree_config,
                "fMaxIndex": fMaxIndex,
                "fArrayDim": fArrayDim,
            }

        else:
            raise ValueError(f"Unknown type: {top_type_name} for C-array: {fTypeName}")

    @classmethod
    def get_reader_instance(cls, tree_config: dict):
        reader_type = tree_config["reader"]
        if reader_type != ReaderType.CArray:
            return None

        element_reader = get_reader_instance(tree_config["element_reader"])

        return bcpp.CArrayReader(
            tree_config["name"],
            tree_config["is_obj"],
            tree_config["flat_size"],
            element_reader,
        )

    @classmethod
    def reconstruct_array(cls, raw_data, tree_config):
        if tree_config["reader"] != ReaderType.CArray:
            return None

        element_tree_config = tree_config["element_reader"]
        fMaxIndex = tree_config["fMaxIndex"]
        fArrayDim = tree_config["fArrayDim"]
        shape = [fMaxIndex[i] for i in range(fArrayDim)]

        element_data = reconstruct_array(
            raw_data,
            element_tree_config,
        )

        for s in shape[::-1]:
            element_data = awkward.contents.RegularArray(element_data, int(s))

        return element_data


class BaseObjectReader(BaseReader):
    """
    Base class is what a custom class inherits from.
    It has fNBytes(uint32), fVersion(uint16) at the beginning.
    """

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name,
        cls_streamer_info,
        all_streamer_info,
        item_path,
    ):
        if top_type_name != "BASE":
            return None

        fType = cls_streamer_info["fType"]
        if fType != 0:
            return None

        fName = cls_streamer_info["fName"]
        sub_streamers: list = all_streamer_info[fName]

        sub_tree_configs = [
            gen_tree_config(s, all_streamer_info, item_path) for s in sub_streamers
        ]

        return {
            "reader": ReaderType.BaseObject,
            "name": fName,
            "sub_readers": sub_tree_configs,
        }

    @classmethod
    def get_reader_instance(cls, tree_config: dict):
        if tree_config["reader"] != ReaderType.BaseObject:
            return None

        sub_readers = [get_reader_instance(s) for s in tree_config["sub_readers"]]
        return bcpp.BaseObjectReader(tree_config["name"], sub_readers)

    @classmethod
    def reconstruct_array(cls, raw_data, tree_config):
        if tree_config["reader"] != ReaderType.BaseObject:
            return None

        sub_tree_configs = tree_config["sub_readers"]

        arr_dict = {}
        for s_cfg, s_data in zip(sub_tree_configs, raw_data):
            s_name = s_cfg["name"]
            s_reader_type = s_cfg["reader"]

            if s_reader_type == ReaderType.TObject:
                continue

            arr_dict[s_name] = reconstruct_array(s_data, s_cfg)

        return awkward.contents.RecordArray(
            [arr_dict[k] for k in arr_dict],
            [k for k in arr_dict],
        )


class ObjectHeaderReader(BaseReader):
    """
    This class read an object starting with an object header.
    """

    @classmethod
    def priority(cls):
        return 0  # should be called last

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name,
        cls_streamer_info,
        all_streamer_info,
        item_path,
    ):
        sub_streamers: list = all_streamer_info[top_type_name]
        sub_tree_configs = [
            gen_tree_config(s, all_streamer_info, item_path) for s in sub_streamers
        ]
        return {
            "reader": ReaderType.ObjectHeader,
            "name": top_type_name,
            "sub_readers": sub_tree_configs,
        }

    @classmethod
    def get_reader_instance(cls, tree_config: dict):
        if tree_config["reader"] != ReaderType.ObjectHeader:
            return None

        sub_readers = [get_reader_instance(s) for s in tree_config["sub_readers"]]
        return bcpp.ObjectHeaderReader(tree_config["name"], sub_readers)

    @classmethod
    def reconstruct_array(cls, raw_data, tree_config):
        if tree_config["reader"] != ReaderType.ObjectHeader:
            return None

        sub_tree_configs = tree_config["sub_readers"]

        arr_dict = {}
        for s_cfg, s_data in zip(sub_tree_configs, raw_data):
            s_name = s_cfg["name"]
            s_reader_type = s_cfg["reader"]

            if s_reader_type == ReaderType.TObject:
                continue

            arr_dict[s_name] = reconstruct_array(s_data, s_cfg)

        return awkward.contents.RecordArray(
            [arr_dict[k] for k in arr_dict],
            [k for k in arr_dict],
        )


class EmptyReader(BaseReader):
    """
    This class does nothing.
    """

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name,
        cls_streamer_info,
        all_streamer_info,
        item_path,
    ):
        return None

    @classmethod
    def get_reader_instance(cls, tree_config: dict):
        if tree_config["reader"] != ReaderType.Empty:
            return None

        return bcpp.EmptyReader(tree_config["name"])

    @classmethod
    def reconstruct_array(cls, raw_data, tree_config):
        if tree_config["reader"] != ReaderType.Empty:
            return None

        return awkward.contents.EmptyArray()


class Bes3TObjArrayReader(BaseReader):
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

    @classmethod
    def gen_tree_config(
        cls,
        top_type_name: str,
        cls_streamer_info: dict,
        all_streamer_info: dict,
        item_path: str = "",
    ):
        if top_type_name != "TObjArray":
            return None

        obj_typename = Bes3TObjArrayReader.bes3_branch2types.get(
            item_path.replace(".TObjArray*", "")
        )
        if obj_typename is None:
            return None

        if obj_typename not in all_streamer_info:
            return {
                "reader": "MyTObjArrayReader",
                "name": cls_streamer_info["fName"],
                "element_reader": {
                    "reader": ReaderType.Empty,
                    "name": obj_typename,
                },
            }

        sub_reader_config = []
        for s in all_streamer_info[obj_typename]:
            sub_reader_config.append(
                gen_tree_config(s, all_streamer_info, item_path + f".{obj_typename}")
            )

        return {
            "reader": "MyTObjArrayReader",
            "name": cls_streamer_info["fName"],
            "element_reader": {
                "reader": ReaderType.ObjectHeader,
                "name": obj_typename,
                "sub_readers": sub_reader_config,
            },
        }

    @staticmethod
    def get_reader_instance(reader_config: dict):
        if reader_config["reader"] != "MyTObjArrayReader":
            return None

        element_reader_config = reader_config["element_reader"]
        element_reader = get_reader_instance(element_reader_config)

        return bcpp.Bes3TObjArrayReader(reader_config["name"], element_reader)

    @staticmethod
    def reconstruct_array(raw_data, reader_config: dict):
        if reader_config["reader"] != "MyTObjArrayReader":
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


readers |= {
    CTypeReader,
    STLSequenceReader,
    STLMapReader,
    STLStringReader,
    TArrayReader,
    TStringReader,
    TObjectReader,
    CArrayReader,
    BaseObjectReader,
    ObjectHeaderReader,
    EmptyReader,
    Bes3TObjArrayReader,
}


##########################################################################################
#                                     Array Preprocess
##########################################################################################
def get_symetric_matrix_idx(
    i: Union[int, ak.Array, np.ndarray], j: Union[int, ak.Array, np.ndarray], ndim: int
) -> int:
    """
    Returns the index of the similarity matrix given the row and column indices.

    The matrix is assumed to be symmetric-like. (i, j) -> index relationship is:

    |     | i=0 | i=1 | i=2 |
    | :-: | :-: | :-: | :-: |
    | j=0 |  0  |     |     |
    | j=1 |  1  |  2  |     |
    | j=2 |  3  |  4  |  5  |

    Parameters:
        i (Union[int, ak.Array, np.ndarray]): The row index or array of row indices.
        j (Union[int, ak.Array, np.ndarray]): The column index or array of column indices.
        ndim (int): The dimension of the similarity matrix.

    Returns:
        The index or array of indices corresponding to the given row and column indices.

    Raises:
        ValueError: If the row and column indices are not of the same type, or if one of them is not an integer.
        ValueError: If the row or column indices are greater than or equal to the dimension of the similarity matrix.
        ValueError: If the row or column indices are negative.
    """
    # Check type
    return_type: Literal["ak", "np"] = "ak"
    if type(i) != type(j):
        if isinstance(i, int):
            return_type = "np" if isinstance(j, np.ndarray) else "ak"
            i = ak.ones_like(j) * i
        elif isinstance(j, int):
            return_type = "np" if isinstance(i, np.ndarray) else "ak"
            j = ak.ones_like(i) * j
        else:
            raise ValueError(
                "i and j should be the same type, or one of them should be an integer."
            )
    else:
        return_type = "np" if isinstance(i, np.ndarray) else "ak"

    i, j = ak.sort([i, j], axis=0)
    res = j * (j + 1) // 2 + i

    # Check dimension
    if ak.any([i >= ndim, j >= ndim]):
        raise ValueError(
            "Indices i and j should be less than the dimension of the similarity matrix."
        )
    if ak.any([i < 0, j < 0]):
        raise ValueError("Indices i and j should be non-negative.")

    if return_type == "np" and isinstance(res, ak.Array):
        res = res.to_numpy()

    return res


def expand_zipped_symetric_matrix(
    arr: Union[ak.Array, np.ndarray],
) -> Union[ak.Array, np.ndarray]:
    """
    Recover a flattened simplified symmetric matrix represented as a 1D array back to a 2D matrix.
    This function assumes the last dimension of the input array is the flattened symmetric matrix,
    and will transform array

    ```
    [[a11, a12, a22, a13, a23, a33],
     [b11, b12, b22, b13, b23, b33]]
    ```

    to

    ```
    [[[a11, a12, a13],
      [a12, a22, a23],
      [a13, a23, a33]],

     [[b11, b12, b13],
      [b12, b22, b23],
      [b13, b23, b33]]]
    ```

    Parameters:
        arr (Union[ak.Array, np.ndarray]): The input array representing the flattened simplified symmetric matrix.

    Returns:
        The reshaped symmetric matrix as a 2D array.

    Raises:
        ValueError: If the input array does not have a symmetric shape.
    """

    # Get the number of elements in the symmetric matrix
    if isinstance(arr, ak.Array):
        type_strs = [i.strip() for i in arr.typestr.split("*")[:-1]]
        n_err_elements = int(type_strs[-1])
        raw_shape = _extract_index(arr.layout)[:-1]
        flat_arr = _flat_to_numpy(arr).flatten().reshape(-1, n_err_elements)
    else:
        n_err_elements = arr.shape[-1]
        raw_shape = arr.shape[:-1]
        flat_arr = arr.reshape(-1, n_err_elements)

    ndim_err = (np.sqrt(1 + 8 * n_err_elements) - 1) / 2
    if not ndim_err.is_integer():
        raise ValueError("The array does not have a symmetric shape.")
    ndim_err = int(ndim_err)

    # Preapre output array
    n_raw_len = len(flat_arr.flatten())
    n_out_len = n_raw_len // n_err_elements * (ndim_err**2)
    raw_out = np.zeros(n_out_len, dtype=flat_arr.dtype).reshape(-1, ndim_err, ndim_err)

    # Fill error matrix
    for i in range(ndim_err):
        for j in range(ndim_err):
            idx = get_symetric_matrix_idx(i, j, ndim_err)
            raw_out[:, i, j] = flat_arr[:, idx]

    # Reshape the output array to match the original shape
    if isinstance(arr, ak.Array):
        res = _recover_shape(ak.Array(raw_out), raw_shape)
    else:
        res = raw_out.reshape(*raw_shape, ndim_err, ndim_err)

    return res


def expand_subbranch_symetric_matrix(
    sub_br_arr: ak.Array, matrix_fields: Union[str, set[str]]
) -> ak.Array:
    """
    Recover simplified symmetric matrix back to 2D matrix from specified fields of a branch array.

    Parameters:
        sub_br_arr: Subbranch array that need to be recovered.
        matrix_fields: Name of list of names of fields to be recovered.

    Returns:
        An array with recovered fields.
    """
    if isinstance(matrix_fields, str):
        matrix_fields = {matrix_fields}
    matrix_fields = set(matrix_fields)

    raw_shape = _extract_index(sub_br_arr.layout)

    res_dict = {}
    for field_name in sub_br_arr.fields:
        flat_sub_arr = sub_br_arr[field_name]
        for _ in range(len(raw_shape)):
            flat_sub_arr = ak.flatten(flat_sub_arr)

        if field_name in matrix_fields:
            res_dict[field_name] = expand_zipped_symetric_matrix(flat_sub_arr)
        else:
            res_dict[field_name] = flat_sub_arr

    res_arr = _recover_shape(ak.Array(res_dict), raw_shape)
    return res_arr


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
    assert "TRawData" in org_arr.fields, "TRawData not found in the input array"

    fields = {}
    for field_name in org_arr.fields:
        if field_name == "TRawData":
            for raw_field_name in org_arr[field_name].fields:
                fields[raw_field_name] = org_arr[field_name][raw_field_name]
        else:
            fields[field_name] = org_arr[field_name]

    return ak.Array(fields)


#############################################
# TEvtRecObject
#############################################
def process_evtrec_m_Evtx(org_arr: ak.Array) -> ak.Array:
    return expand_subbranch_symetric_matrix(org_arr, "m_Evtx")


def process_evtrec_m_evtRecVeeVertexCol(org_arr: ak.Array) -> ak.Array:
    return expand_subbranch_symetric_matrix(org_arr, "m_Ew")


#############################################
# TDstEvent
#############################################
def process_dst_m_mdcTrackCol(org_arr: ak.Array) -> ak.Array:
    return expand_subbranch_symetric_matrix(org_arr, "m_err")


def process_dst_m_emcTrackCol(org_arr: ak.Array) -> ak.Array:
    return expand_subbranch_symetric_matrix(org_arr, "m_err")


def process_dst_m_extTrackCol(org_arr: ak.Array) -> ak.Array:
    return expand_subbranch_symetric_matrix(
        org_arr,
        {
            "myEmcErrorMatrix",
            "myMucErrorMatrix",
            "myTof1ErrorMatrix",
            "myTof2ErrorMatrix",
        },
    )


def process_dst_m_mdcKalTrackCol(org_arr: ak.Array) -> ak.Array:
    return expand_subbranch_symetric_matrix(
        org_arr,
        {
            "m_zerror",
            "m_zerror_e",
            "m_zerror_mu",
            "m_zerror_k",
            "m_zerror_p",
            "m_ferror",
            "m_ferror_e",
            "m_ferror_mu",
            "m_ferror_k",
            "m_ferror_p",
        },
    )


#############################################
# TRecEvent
#############################################
def process_rec_m_recMdcTrackCol(org_arr: ak.Array) -> ak.Array:
    return expand_subbranch_symetric_matrix(org_arr, "m_err")


def process_rec_m_recEmcShowerCol(org_arr: ak.Array) -> ak.Array:
    return expand_subbranch_symetric_matrix(org_arr, "m_err")


def process_rec_m_recMdcKalTrackCol(org_arr: ak.Array) -> ak.Array:
    return expand_subbranch_symetric_matrix(org_arr, "m_terror")


#############################################
# Main function
#############################################
def preprocess_subbranch(full_branch_path: str, org_arr: ak.Array) -> ak.Array:
    full_branch_path = full_branch_path.replace("/Event:", "")
    evt_name, subbranch_name = full_branch_path.split("/")

    if evt_name == "TDigiEvent" and subbranch_name != "m_fromMc":
        return process_digi_subbranch(org_arr)

    if evt_name == "TEvtRecObject":
        if subbranch_name == "m_Evtx":
            return process_evtrec_m_Evtx(org_arr)
        if subbranch_name == "m_evtRecVeeVertexCol":
            return process_evtrec_m_evtRecVeeVertexCol(org_arr)

    if evt_name == "TDstEvent":
        if subbranch_name == "m_mdcTrackCol":
            return process_dst_m_mdcTrackCol(org_arr)
        if subbranch_name == "m_emcTrackCol":
            return process_dst_m_emcTrackCol(org_arr)
        if subbranch_name == "m_extTrackCol":
            return process_dst_m_extTrackCol(org_arr)
        if subbranch_name == "m_mdcKalTrackCol":
            return process_dst_m_mdcKalTrackCol(org_arr)

    if evt_name == "TRecEvent":
        if subbranch_name == "m_recMdcTrackCol":
            return process_rec_m_recMdcTrackCol(org_arr)
        if subbranch_name == "m_recEmcShowerCol":
            return process_rec_m_recEmcShowerCol(org_arr)
        if subbranch_name == "m_recMdcKalTrackCol":
            return process_rec_m_recMdcKalTrackCol(org_arr)

    # Default return
    return org_arr


class Bes3Interpretation(uproot.interpretation.Interpretation):
    """
    Custom interpretation for Bes3 data.
    """

    target_branches: set[str] = set(Bes3TObjArrayReader.bes3_branch2types.keys())

    def __init__(
        self,
        branch: uproot.behaviors.TBranch.TBranch,
        context: dict,
        simplify: bool,
    ):
        """
        Args:
            branch (:doc:`uproot.behaviors.TBranch.TBranch`): The ``TBranch`` to
                interpret as an array.
            context (dict): Auxiliary data used in deserialization.
            simplify (bool): If True, call
                :ref:`uproot.interpretation.objects.AsObjects.simplify` on any
                :doc:`uproot.interpretation.objects.AsObjects` to try to get a
                more efficient interpretation.

        Accept arguments from `uproot.interpretation.identify.interpretation_of`.
        """
        self._branch = branch
        self._context = context
        self._simplify = simplify

        # simplify streamer information
        self.all_streamer_info: dict[str, list[dict]] = {}
        for k, v in branch.file.streamers.items():
            cur_infos = [i.all_members for i in next(iter(v.values())).member("fElements")]
            self.all_streamer_info[k] = cur_infos

    @classmethod
    def match_branch(
        cls,
        branch: uproot.behaviors.TBranch.TBranch,
        context: dict,
        simplify: bool,
    ) -> bool:
        """
        Args:
            branch (:doc:`uproot.behaviors.TBranch.TBranch`): The ``TBranch`` to
                interpret as an array.
            context (dict): Auxiliary data used in deserialization.
            simplify (bool): If True, call
                :ref:`uproot.interpretation.objects.AsObjects.simplify` on any
                :doc:`uproot.interpretation.objects.AsObjects` to try to get a
                more efficient interpretation.

        Accept arguments from `uproot.interpretation.identify.interpretation_of`,
        determine whether this interpretation can be applied to the given branch.
        """
        full_path = regularize_object_path(branch.object_path)
        return full_path in cls.target_branches

    @property
    def typename(self) -> str:
        """
        The name of the type of the interpretation.
        """
        return self._branch.streamer.typename

    @property
    def cache_key(self) -> str:
        """
        The cache key of the interpretation.
        """
        return id(self)

    def __repr__(self) -> str:
        """
        The string representation of the interpretation.
        """
        return f"AsBes3Custom({self.typename})"

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
        """
        Concatenate the arrays from the baskets and return the final array.
        """

        awkward = uproot.extras.awkward()

        basket_entry_starts = np.array(entry_offsets[:-1])
        basket_entry_stops = np.array(entry_offsets[1:])

        basket_start_idx = np.where(basket_entry_starts <= entry_start)[0].max()
        basket_end_idx = np.where(basket_entry_stops >= entry_stop)[0].min()

        arr_to_concat = [basket_arrays[i] for i in range(basket_start_idx, basket_end_idx + 1)]
        tot_array = awkward.concatenate(arr_to_concat)

        relative_entry_start = entry_start - basket_entry_starts[basket_start_idx]
        relative_entry_stop = entry_stop - basket_entry_starts[basket_start_idx]

        return tot_array[relative_entry_start:relative_entry_stop]

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
        assert library.name == "ak", "Only awkward arrays are supported"

        full_branch_path = regularize_object_path(branch.object_path)

        # generate reader config
        tree_config = gen_tree_config_from_type_name(
            branch.streamer.typename, self.all_streamer_info, full_branch_path
        )

        # get reader
        reader = get_reader_instance(tree_config)

        # do read
        raw_data = bcpp.read_data(data, byte_offsets, reader)

        # recover raw data
        raw_ak_layout = reconstruct_array(raw_data, tree_config)
        raw_ak_arr = ak.Array(raw_ak_layout)

        # preprocess awkward array and return
        return preprocess_subbranch(full_branch_path, raw_ak_arr)


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

    if Bes3Interpretation.match_branch(branch, context, simplify):
        return Bes3Interpretation(branch, context, simplify)

    return _uproot_interpretation_of(branch, context, simplify)


def wrap_uproot_interpretation():
    global _is_uproot_interpretation_of_wrapped
    if not _is_uproot_interpretation_of_wrapped:
        _is_uproot_interpretation_of_wrapped = True
        uproot.interpretation.identify.interpretation_of = bes_interpretation_of


def wrap_uproot_TBranchElement_branches():
    def branches(self):

        if self.name not in {
            "TEvtHeader",
            "TMcEvent",
            "TDigiEvent",
            "TDstEvent",
            "TRecEvent",
            "TEvtRecObject",
            "THltEvent",
        }:
            return self.member("fBranches")
        else:

            res = []
            for br in self.member("fBranches"):
                if br.name == "TObject":
                    continue

                full_path = regularize_object_path(br.object_path)
                if full_path not in Bes3TObjArrayReader.bes3_branch2types:
                    res.append(br)
                    continue

                class_name = Bes3TObjArrayReader.bes3_branch2types[full_path]
                if class_name in self.file.streamers:
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
    """
    Wraps the uproot functions to use the BES interpretation.
    """
    wrap_uproot_interpretation()
    wrap_uproot_TBranchElement_branches()
