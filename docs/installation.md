# Installation

!!! info
    `pybes3` requires Python 3.9 or higher.

## Install `pybes3` using pip

```bash
pip install pybes3
```

## Users on lxlogin server

"lxlogin server" refers to the login server of IHEP computation clusters. If you are not using the lxlogin server, you can skip this section.

Since there is a quota limitation on the user's home directory (`~/`), you need to create symbolic links for `~/.local` and `~/.cache`, which contain pip packages and caches installed in "user mode":

```bash
# Check whether `.local` and `.cache` directories already exist.
# If so, move them to somewhere outside ~/
ls -a ~
mv ~/.local /path/to/somewhere/
mv ~/.cache /path/to/somewhere/

# If no `.local` or `.cache` exists, create them
mkdir /path/to/somewhere/.local
mkdir /path/to/somewhere/.cache

# After moving or creating them, link them back to ~
ln -s /path/to/somewhere/.local ~/.local
ln -s /path/to/somewhere/.cache ~/.cache
```

## Using `pybes3` under `BOSS8` environment

If you are using `pybes3` under a `BOSS8` environment, you **must** run the following commands after setting up the `BOSS8` environment:

```bash
export PYTHONPATH=`python -m site --user-site`:$PYTHONPATH
export PATH=`python -m site --user-base`/bin:$PATH
```

!!! warning
    Do **not** add these commands to your shell configuration file (e.g., `~/.bashrc`), since they will conflict with the default Python environment (without `BOSS8`).
