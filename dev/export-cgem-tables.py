import pandas as pd
import numpy as np
import pybes3.digi_id as digi

# The path of 'mapping.txt' file is in BOSS_Source/Cgem/CgemInfoLuSvc/share/mapping.txt.
raw_map = pd.read_csv(
    "mapping.txt",
    sep=" ",
    dtype={
        "constant": np.float32,
        "slope": np.float32,
    },
)

tiger_sheet1 = (
    list(range(48, 62)) + list(range(80, 94)) + list(range(114, 132)) + list(range(154, 172))
)


# There are total 22 GEMROC, while 21 of them are fully used (8 TIGERs each)
# and the last one is only used for 4 TIGERs.

# On each TIGER, there are 64 channels, so we create arrays of shape (21*8+4, 64)
# to store the mapping information.

N_ELEC_STRIPS = 21 * 8 + 4
N_CHANNELS = 64

raw_gemroc = np.ones((N_ELEC_STRIPS, N_CHANNELS), dtype=np.uint8) * 255
raw_tiger = np.ones((N_ELEC_STRIPS, N_CHANNELS), dtype=np.uint8) * 255
raw_channel = np.ones((N_ELEC_STRIPS, N_CHANNELS), dtype=np.uint8) * 255

raw_layer = np.ones((N_ELEC_STRIPS, N_CHANNELS), dtype=np.uint8) * 255
raw_sheet = np.ones((N_ELEC_STRIPS, N_CHANNELS), dtype=np.uint8) * 255
raw_view = np.ones((N_ELEC_STRIPS, N_CHANNELS), dtype=np.uint8) * 255
raw_strip = np.ones((N_ELEC_STRIPS, N_CHANNELS), dtype=np.uint16) * 65535
raw_constant = np.ones((N_ELEC_STRIPS, N_CHANNELS), dtype=np.float64) * np.nan
raw_slope = np.ones((N_ELEC_STRIPS, N_CHANNELS), dtype=np.float64) * np.nan

raw_digi_id = np.ones((N_ELEC_STRIPS, N_CHANNELS), dtype=np.uint32) * 4294967295


for i, row in raw_map.iterrows():
    if row["strip"] == "-1":  # This channel is not used
        continue
    assert row["strip"][0] in ["X", "V"], f"Invalid strip name: {row['strip']}"

    strip_type = 0 if row["strip"][0] == "X" else 1 if row["strip"][0] == "V" else -1
    strip = int(row["strip"][1:])

    # refer to BOSS: CgemInfoLuSvc::Readmapping()
    if strip_type == 0:
        if row.layer_ID == 1 and strip >= 630:
            strip -= 630
        if row.layer_ID == 2 and strip >= 832:
            strip -= 832
    elif strip_type == 1:
        if row.layer_ID == 1 and strip >= 1077:
            strip -= 1077
        if row.layer_ID == 2 and strip >= 1395:
            strip -= 1395

    tiger = 8 * row["gemroc_ID"] + row["SW_FEB_ID"]
    sheet = 0 if tiger not in tiger_sheet1 else 1
    channel = row["channel_ID"]

    raw_gemroc[tiger, channel] = row["gemroc_ID"]
    raw_tiger[tiger, channel] = row["SW_FEB_ID"]
    raw_channel[tiger, channel] = channel
    raw_layer[tiger, channel] = row["layer_ID"]
    raw_sheet[tiger, channel] = sheet
    raw_view[tiger, channel] = strip_type
    raw_strip[tiger, channel] = strip

    raw_digi_id[tiger, channel] = digi.get_cgem_digi_id(
        row["layer_ID"], sheet, strip_type, strip
    )

    raw_constant[tiger, channel] = row["constant"]
    raw_slope[tiger, channel] = row["slope"]

new_map = {
    "tiger": raw_tiger.flatten(),
    "channel": raw_channel.flatten(),
    "gemroc": raw_gemroc.flatten(),
    "layer": raw_layer.flatten(),
    "sheet": raw_sheet.flatten(),
    "strip_type": raw_view.flatten(),
    "strip": raw_strip.flatten(),
    "digi_id": raw_digi_id.flatten(),
    "constant": raw_constant.flatten(),
    "slope": raw_slope.flatten(),
}

np.savez_compressed("cgem_elec_table.npz", **new_map)
