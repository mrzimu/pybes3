import struct

from pybes3.io.raw_io import RawBinaryReader

reader = RawBinaryReader(
    "/besfs8/offline/data/merge/raw/round19/260409/run_0091668_All_merge0_file002_SFO-1.raw"
)

reader._reset_cursor()
block_data = reader._read_block(10)

fin = open(
    "/besfs8/offline/data/merge/raw/round19/260409/run_0091668_All_merge0_file002_SFO-1.raw",
    "rb",
)
fout = open("test_raw_data.raw", "wb")

file_header = fin.read(reader._data_start)
fout.write(file_header)

fout.write(block_data.tobytes())

fout.write(
    struct.pack(
        "10I",
        0x1234DDDD,  # marker
        10,  # block size
        8042026,  # date
        120631,  # time
        10,  # n-events
        int((fout.tell() + 40) / 1024 / 1024),  # file size in this file (MB)
        10,  # n-events in run
        int((fout.tell() + 40) / 1024 / 1024),  # file size in this run (MB)
        0,  # status
        0x1234EEEE,  # end-marker
    )
)


fin.close()
fout.close()
