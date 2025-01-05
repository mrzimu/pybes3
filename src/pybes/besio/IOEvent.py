import awkward as ak
import numpy as np
from typing import Union, Literal
from collections import UserDict
from abc import ABC, abstractmethod


def get_sim_matrix_idx(i: Union[int, ak.Array, np.ndarray],
                       j: Union[int, ak.Array, np.ndarray],
                       ndim: int) -> int:
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
    return_type: Literal['ak', 'np'] = 'ak'
    if type(i) != type(j):
        if isinstance(i, int):
            return_type = 'np' if isinstance(j, np.ndarray) else 'ak'
            i = ak.ones_like(j) * i
        elif isinstance(j, int):
            return_type = 'np' if isinstance(i, np.ndarray) else 'ak'
            j = ak.ones_like(i) * j
        else:
            raise ValueError("i and j should be the same type, or one of them should be an integer.")
    else:
        return_type = 'np' if isinstance(i, np.ndarray) else 'ak'

    i, j = ak.sort([i, j], axis=0)
    res = j * (j + 1) // 2 + i

    # Check dimension
    if ak.any([i >= ndim, j >= ndim]):
        raise ValueError("Indices i and j should be less than the dimension of the similarity matrix.")
    if ak.any([i < 0, j < 0]):
        raise ValueError("Indices i and j should be non-negative.")

    if return_type == 'np' and isinstance(res, ak.Array):
        res = res.to_numpy()

    return res


def reshape_symmetric_matrix(arr: Union[ak.Array, np.ndarray]) -> Union[ak.Array, np.ndarray]:
    """
    EvtRecover a flattened simplified symmetric matrix represented as a 1D array back to a 2D matrix.
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
        type_strs = [i.strip() for i in arr.typestr.split('*')[:-1]]
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
            tmp_idx = tuple([slice(None)] * (ndim_data - 1) +
                            [get_sim_matrix_idx(i, j, ndim_err), np.newaxis, np.newaxis])
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


class IOField(UserDict[str, ak.Array], ABC):
    def __init__(self, arr: ak.Array) -> None:
        UserDict.__init__(self)
        ABC.__init__(self)

        err_fields = self._err_fields()

        for f in arr.fields:
            if f in err_fields:
                self[f] = reshape_symmetric_matrix(arr[f])
            else:
                self[f] = arr[f]

        for k, v in self.items():
            assert not hasattr(self, k)
            setattr(self, k, v)

    @abstractmethod
    def _err_fields(self) -> list[str]:
        """
        Returns a list of error-matrix fields for the event. Subclasses should implement this method.

        Returns:
            list[str]: A list of names of error-matrix fields.
        """
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __repr__(self) -> str:
        res = f"{self.__class__.__name__} with attributions: "
        res += ', '.join([f"{k}" for k, v in self.items()])
        return res


class EventHeader(IOField):
    def _err_fields(self) -> list[str]:
        return []


class EvtRecEvent(IOField):
    def _err_fields(self) -> list[str]:
        return []


class EvtRecTracks(IOField):
    def _err_fields(self) -> list[str]:
        return []


class EvtRecPrimaryVertex(IOField):
    def _err_fields(self) -> list[str]:
        return ['errVtx']


class EvtRecVeeVertex(IOField):
    def _err_fields(self) -> list[str]:
        return ['err']


class EvtRecPi0(IOField):
    def _err_fields(self) -> list[str]:
        return []


class EvtRecDTag(IOField):
    def _err_fields(self) -> list[str]:
        return []


class EvtRecEtaToGG(IOField):
    def _err_fields(self) -> list[str]:
        return []


class McMdcTrk(IOField):
    def _err_fields(self) -> list[str]:
        return []


class McEmcTrk(IOField):
    def _err_fields(self) -> list[str]:
        return []


class McTofTrk(IOField):
    def _err_fields(self) -> list[str]:
        return []


class McMucTrk(IOField):
    def _err_fields(self) -> list[str]:
        return []


class McParticle(IOField):
    def _err_fields(self) -> list[str]:
        return []


class DigiMdc(IOField):
    def _err_fields(self) -> list[str]:
        return []


class DigiEmc(IOField):
    def _err_fields(self) -> list[str]:
        return []


class DigiTof(IOField):
    def _err_fields(self) -> list[str]:
        return []


class DigiMuc(IOField):
    def _err_fields(self) -> list[str]:
        return []


class DigiLumi(IOField):
    def _err_fields(self) -> list[str]:
        return []


class DigiFromMc(IOField):
    def _err_fields(self) -> list[str]:
        return []


class DstMdc(IOField):
    def _err_fields(self) -> list[str]:
        return ['helixErr']


class DstEmc(IOField):
    def _err_fields(self) -> list[str]:
        return ['err']


class DstTof(IOField):
    def _err_fields(self) -> list[str]:
        return []


class DstMuc(IOField):
    def _err_fields(self) -> list[str]:
        return []


class DstDedx(IOField):
    def _err_fields(self) -> list[str]:
        return []


class DstExt(IOField):
    def _err_fields(self) -> list[str]:
        return ['Tof1ErrorMatrix',
                'Tof2ErrorMatrix',
                'EmcErrorMatrix',
                'MucErrorMatrix']


class RecMdcTrack(IOField):
    def _err_fields(self) -> list[str]:
        return ['err']


class RecMdcHit(IOField):
    def _err_fields(self) -> list[str]:
        return []


class RecTofTrack(IOField):
    def _err_fields(self) -> list[str]:
        return []


class RecEmcHit(IOField):
    def _err_fields(self) -> list[str]:
        return []


class RecEmcCluster(IOField):
    def _err_fields(self) -> list[str]:
        return []


class RecEmcShower(IOField):
    def _err_fields(self) -> list[str]:
        return ['err']


class RecMucTrack(IOField):
    def _err_fields(self) -> list[str]:
        return []


class RecMdcDedx(IOField):
    def _err_fields(self) -> list[str]:
        return []


class RecMdcDedxHit(IOField):
    def _err_fields(self) -> list[str]:
        return []


class RecExtTrack(IOField):
    def _err_fields(self) -> list[str]:
        return []


class RecMdcKalTrack(IOField):
    def _err_fields(self) -> list[str]:
        return ['terror']


class RecMdcKalHelixSeg(IOField):
    def _err_fields(self) -> list[str]:
        return []


class RecEvTime(IOField):
    def _err_fields(self) -> list[str]:
        return []


class RecZdd(IOField):
    def _err_fields(self) -> list[str]:
        return []


class HltRaw(IOField):
    def _err_fields(self) -> list[str]:
        return []


class HltInf(IOField):
    def _err_fields(self) -> list[str]:
        return []


class HltDstInf(IOField):
    def _err_fields(self) -> list[str]:
        return []


class TrigData(IOField):
    def _err_fields(self) -> list[str]:
        return []


class IOSubEvent(ABC):
    @property
    @abstractmethod
    def available_fields(self) -> list[str]:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} with available fields: {self.available_fields}"


class IOMcEvent(IOSubEvent):
    def __init__(self, data_dict: dict[str, ak.Array]) -> None:
        super().__init__()

        self.mdc: McMdcTrk
        self.emc: McEmcTrk
        self.tof: McTofTrk
        self.muc: McMucTrk
        self.particle: McParticle

        for k, v in data_dict.items():
            if not k.startswith('/Event/Mc'):
                continue

            field = k.split('/')[-1]

            if field == 'Mdc':
                self.mdc = McMdcTrk(v)
            if field == 'Emc':
                self.emc = McEmcTrk(v)
            if field == 'Tof':
                self.tof = McTofTrk(v)
            if field == 'Muc':
                self.muc = McMucTrk(v)
            if field == 'McParticle':
                self.particle = McParticle(v)

    @property
    def available_fields(self) -> list[str]:
        attr_names = ['mdc', 'emc', 'tof', 'muc', 'particle']
        return [i for i in attr_names if hasattr(self, i)]


class IODigiEvent(IOSubEvent):
    def __init__(self, data_dict: dict[str, ak.Array]) -> None:
        super().__init__()

        self.mdc: DigiMdc
        self.emc: DigiEmc
        self.tof: DigiTof
        self.muc: DigiMuc
        self.lumi: DigiLumi
        self.from_mc: DigiFromMc

        for k, v in data_dict.items():
            if not k.startswith('/Event/Digi'):
                continue

            field = k.split('/')[-1]

            if field == 'Mdc':
                self.mdc = DigiMdc(v)
            if field == 'Emc':
                self.emc = DigiEmc(v)
            if field == 'Tof':
                self.tof = DigiTof(v)
            if field == 'Muc':
                self.muc = DigiMuc(v)
            if field == 'Lumi':
                self.lumi = DigiLumi(v)
            if field == 'FromMc':
                self.from_mc = DigiFromMc(v)

    @property
    def available_fields(self) -> list[str]:
        attr_names = ['mdc', 'emc', 'tof', 'muc', 'lumi', 'from_mc']
        return [i for i in attr_names if hasattr(self, i)]


class IODstEvent(IOSubEvent):
    def __init__(self, data_dict: dict[str, ak.Array]) -> None:
        super().__init__()

        self.mdc: DstMdc
        self.emc: DstEmc
        self.tof: DstTof
        self.muc: DstMuc
        self.dedx: DstDedx
        self.ext: DstExt

        for k, v in data_dict.items():
            if not k.startswith('/Event/Dst'):
                continue

            field = k.split('/')[-1]

            if field == 'Mdc':
                self.mdc = DstMdc(v)
            if field == 'Emc':
                self.emc = DstEmc(v)
            if field == 'Tof':
                self.tof = DstTof(v)
            if field == 'Muc':
                self.muc = DstMuc(v)
            if field == 'Dedx':
                self.dedx = DstDedx(v)
            if field == 'Ext':
                self.ext = DstExt(v)

    @property
    def available_fields(self) -> list[str]:
        attr_names = ['mdc', 'emc', 'tof', 'muc', 'dedx', 'ext']
        return [i for i in attr_names if hasattr(self, i)]


class IOEvtRecEvent(IOSubEvent):
    def __init__(self, data_dict: dict[str, ak.Array]) -> None:
        super().__init__()

        self.evt: EvtRecEvent
        self.tracks: EvtRecTracks
        self.prim_vtx: EvtRecPrimaryVertex
        self.vee_vtx: EvtRecVeeVertex
        self.pi0: EvtRecPi0
        self.dtag: EvtRecDTag
        self.eta2gg: EvtRecEtaToGG

        for k, v in data_dict.items():
            if not k.startswith('/Event/EvtRec'):
                continue

            field = k.split('/')[-1]

            if field == 'Evt':
                self.evt = EvtRecEvent(v)

            if field == 'Tracks':
                self.tracks = EvtRecTracks(v)

            if field == 'PrimaryVertex':
                self.prim_vtx = EvtRecPrimaryVertex(v)

            if field == 'VeeVertex':
                self.vee_vtx = EvtRecVeeVertex(v)

            if field == 'Pi0':
                self.pi0 = EvtRecPi0(v)

            if field == 'DTag':
                self.dtag = EvtRecDTag(v)

            if field == 'EtaToGG':
                self.eta2gg = EvtRecEtaToGG(v)

    @property
    def available_fields(self) -> list[str]:
        attr_names = ['evt', 'tracks', 'prim_vtx', 'vee_vtx', 'pi0', 'dtag', 'eta2gg']
        return [i for i in attr_names if hasattr(self, i)]


class IORecEvent(IOSubEvent):
    def __init__(self, data_dict: dict[str, ak.Array]) -> None:
        super().__init__()

        self.mdc_track: RecMdcTrack
        self.mdc_hit: RecMdcHit
        self.tof_track: RecTofTrack
        self.emc_hit: RecEmcHit
        self.emc_cluster: RecEmcCluster
        self.emc_shower: RecEmcShower
        self.muc_track: RecMucTrack
        self.mdc_dedx: RecMdcDedx
        self.mdc_dedx_hit: RecMdcDedxHit
        self.ext_track: RecExtTrack
        self.mdc_kal_track: RecMdcKalTrack
        self.mdc_kal_helix_seg: RecMdcKalHelixSeg
        self.ev_time: RecEvTime
        self.zdd: RecZdd

        for k, v in data_dict.items():
            if not k.startswith('/Event/Rec'):
                continue

            field = k.split('/')[-1]

            if field == 'MdcTrack':
                self.mdc_track = RecMdcTrack(v)

            if field == 'MdcHit':
                self.mdc_hit = RecMdcHit(v)

            if field == 'TofTrack':
                self.tof_track = RecTofTrack(v)

            if field == 'EmcHit':
                self.emc_hit = RecEmcHit(v)

            if field == 'EmcCluster':
                self.emc_cluster = RecEmcCluster(v)

            if field == 'EmcShower':
                self.emc_shower = RecEmcShower(v)

            if field == 'MucTrack':
                self.muc_track = RecMucTrack(v)

            if field == 'MdcDedx':
                self.mdc_dedx = RecMdcDedx(v)

            if field == 'MdcDedxHit':
                self.mdc_dedx_hit = RecMdcDedxHit(v)

            if field == 'ExtTrack':
                self.ext_track = RecExtTrack(v)

            if field == 'MdcKalTrack':
                self.mdc_kal_track = RecMdcKalTrack(v)

            if field == 'MdcKalHelixSeg':
                self.mdc_kal_helix_seg = RecMdcKalHelixSeg(v)

            if field == 'EvTime':
                self.ev_time = RecEvTime(v)

            if field == 'Zdd':
                self.zdd = RecZdd(v)

    @property
    def available_fields(self) -> list[str]:
        attr_names = ['mdc_track', 'mdc_hit', 'tof_track', 'emc_hit', 'emc_cluster', 'emc_shower',
                      'muc_track', 'mdc_dedx', 'mdc_dedx_hit', 'ext_track', 'mdc_kal_track', 'mdc_kal_helix_seg',
                      'ev_time', 'zdd']
        return [i for i in attr_names if hasattr(self, i)]


class IOHltEvent(IOSubEvent):
    def __init__(self, data_dict: dict[str, ak.Array]) -> None:
        super().__init__()

        self.raw: HltRaw
        self.inf: HltInf
        self.dst_inf: HltDstInf

        for k, v in data_dict.items():
            if not k.startswith('/Event/Hlt'):
                continue

            field = k.split('/')[-1]

            if field == 'Raw':
                self.raw = HltRaw(v)

            if field == 'Inf':
                self.inf = HltInf(v)

            if field == 'DstInf':
                self.dst_inf = HltDstInf(v)

    @property
    def available_fields(self) -> list[str]:
        attr_names = ['raw', 'inf', 'dst_inf']
        return [i for i in attr_names if hasattr(self, i)]


class IOEvent:
    def __init__(self,
                 files: list[str],
                 entries: int,
                 data_dict: dict[str, ak.Array]) -> None:
        self.files = files
        self.entries = entries
        self.data = {k: v for k, v in data_dict.items() if v is not None}

        self.header: EventHeader
        self.tigger: TrigData

        self.evt_rec: IOEvtRecEvent
        self.mc: IOMcEvent
        self.digi: IODigiEvent
        self.dst: IODstEvent
        self.rec: IORecEvent

        # Get available sub-events items
        for k in self.data.keys():
            k_split = [i.strip() for i in k.split('/') if i.strip() != '']
            if k_split[0] != 'Event':
                continue

            subevt_name = k_split[1]

            if subevt_name == 'Header':
                self.header = EventHeader(self.data[k])

            if subevt_name == 'Trig':
                self.tigger = TrigData(self.data[k])

            if subevt_name == 'EvtRec':
                self.evt_rec = IOEvtRecEvent(self.data)

            if subevt_name == 'Mc':
                self.mc = IOMcEvent(self.data)

            if subevt_name == 'Digi':
                self.digi = IODigiEvent(self.data)

            if subevt_name == 'Dst':
                self.dst = IODstEvent(self.data)

            if subevt_name == 'Rec':
                self.rec = IORecEvent(self.data)

            if subevt_name == 'Hlt':
                self.hlt = IOHltEvent(self.data)

    @property
    def available_subevents(self) -> list[str]:
        attr_names = ['header', 'evt_rec', 'mc', 'digi', 'dst', 'rec', 'trigger', 'hlt']
        return [i for i in attr_names if hasattr(self, i)]

    def __repr__(self) -> str:
        subevts = []
        for subevt_attr_name in ['header', 'evt_rec', 'mc', 'digi', 'dst', 'rec', 'trigger', 'hlt']:
            if hasattr(self, subevt_attr_name):
                subevts.append(subevt_attr_name)

        return f"Bes3Event with {self.entries} entries, sub-events: {subevts}"
