from typing import Literal, Union

import awkward as ak
import numpy as np


def get_symetric_matrix_idx(
    i: Union[int, ak.Array, np.ndarray], j: Union[int, ak.Array, np.ndarray], ndim: int
) -> int:
    r"""
    Returns the index of the similarity matrix given the row and column indices.
    The matrix is assumed to be symmetric-like. (i, j) -> index relationship is:

     j\i | 0 1 2
    ------------
      0  | 0
      1  | 1 2
      2  | 3 4 5

    Parameters:
        i (Union[int, ak.Array, np.ndarray]): The row index or array of row indices.
        j (Union[int, ak.Array, np.ndarray]): The column index or array of column indices.
        ndim (int): The dimension of the similarity matrix.

    Returns:
        int: The index or array of indices corresponding to the given row and column indices.

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
    arr: Union[ak.Array, np.ndarray]
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

    Args:
        arr (Union[ak.Array, np.ndarray]): The input array representing the flattened simplified symmetric matrix.

    Returns:
        Union[ak.Array, np.ndarray]: The reshaped symmetric matrix as a 2D array.

    Raises:
        ValueError: If the input array does not have a symmetric shape.
    """
    ndim_data: int = arr.ndim

    # Get the number of elements in the symmetric matrix
    if isinstance(arr, ak.Array):
        type_strs = [i.strip() for i in arr.typestr.split("*")[:-1]]
        n_err_elements = int(type_strs[-1])

        ndim_err = (np.sqrt(1 + 8 * n_err_elements) - 1) / 2
        if not ndim_err.is_integer():
            raise ValueError("The array does not have a symmetric shape.")
        ndim_err = int(ndim_err)
    elif isinstance(arr, np.ndarray):
        n_err_elements = arr.shape[-1]

    # Reshape the array
    tmp_matrix = []
    for i in range(ndim_err):
        tmp_row = []
        for j in range(ndim_err):
            tmp_idx = tuple(
                [slice(None)] * (ndim_data - 1)
                + [get_symetric_matrix_idx(i, j, ndim_err), np.newaxis, np.newaxis]
            )
            tmp_row.append(arr[tmp_idx])

        if isinstance(arr, ak.Array):
            tmp_matrix.append(ak.concatenate(tmp_row, axis=-1))
        else:
            tmp_matrix.append(np.concatenate(tmp_row, axis=-1))

    if isinstance(arr, ak.Array):
        res = ak.concatenate(tmp_matrix, axis=-2)
    else:
        res = np.concatenate(tmp_matrix, axis=-2)

    return res


def expand_subbranch_symetric_matrix(
    sub_br_arr: ak.Array, matrix_fields: Union[str, list[str]]
) -> ak.Array:
    if isinstance(matrix_fields, str):
        matrix_fields = {matrix_fields}
    matrix_fields = set(matrix_fields)

    res_dict = {}
    for field_name in sub_br_arr.fields:
        if field_name in matrix_fields:
            res_dict[field_name] = expand_zipped_symetric_matrix(sub_br_arr[field_name])
        else:
            res_dict[field_name] = sub_br_arr[field_name]
    return ak.Array(res_dict)


#############################################
# TDigiEvent
#############################################
def process_digi_subbranch(org_arr: ak.Array) -> ak.Array:
    """
    Processes the 'TRawData' subbranch of the input awkward array and returns a new array with the subbranch fields
    merged into the top level.

    Args:
        org_arr (ak.Array): The input awkward array containing the 'TRawData' subbranch.

    Returns:
        ak.Array: A new awkward array with the fields of 'TRawData' merged into the top level.

    Raises:
        AssertionError: If 'TRawData' is not found in the input array fields.
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

    if evt_name == "TRecEvent":
        if subbranch_name == "m_recMdcTrackCol":
            return process_rec_m_recMdcTrackCol(org_arr)
        if subbranch_name == "m_recEmcShowerCol":
            return process_rec_m_recEmcShowerCol(org_arr)
        if subbranch_name == "m_recMdcKalTrackCol":
            return process_rec_m_recMdcKalTrackCol(org_arr)

    # Default return
    return org_arr
