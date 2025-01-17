from dataclasses import dataclass


@dataclass
class MdcDigiConst:
    DIGI_FLAG = 0x10
    DIGI_OFFSET = 24
    DIGI_MASK = 0xFF000000

    WIRETYPE_OFFSET = 15
    WIRETYPE_MASK = 0x00008000

    LAYER_OFFSET = 9
    LAYER_MASK = 0x00007E00

    WIRE_OFFSET = 0
    WIRE_MASK = 0x000001FF


@dataclass
class TofDigiConst:
    DIGI_FLAG = 0x20
    DIGI_OFFSET = 24
    DIGI_MASK = 0xFF000000


@dataclass
class EmcDigiConst:
    DIGI_FLAG = 0x30
    DIGI_OFFSET = 24
    DIGI_MASK = 0xFF000000

    MODULE_OFFSET = 16
    MODULE_MASK = 0x000F0000

    THETA_OFFSET = 8
    THETA_MASK = 0x00003F00

    PHI_OFFSET = 0
    PHI_MASK = 0x000000FF


@dataclass
class MucDigiConst:
    DIGI_FLAG = 0x40
    DIGI_OFFSET = 24
    DIGI_MASK = 0xFF000000


@dataclass
class HltDigiConst:
    DIGI_FLAG = 0x50
    DIGI_OFFSET = 24
    DIGI_MASK = 0xFF000000


@dataclass
class MrpcDigiConst:
    DIGI_FLAG = 0x70
    DIGI_OFFSET = 24
    DIGI_MASK = 0xFF000000
