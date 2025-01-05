# pybes3

## Overview

`pybes3` is an **unofficial** python module that aims to make BES3 user easier to work with Python. It includes:

* [besio](./doc/besio.md): An I/O submodule that can directly read BES3 `rtraw`, `dst`, `rec` files, and transfer their data to `awkward` array.



## Installation

### Preparation for users on lxlogin

If you are on `lxlogin` server, you need to firstly create a virtual environment for Python:

```bash
cd /path/to/install # somewhere you choose to install virtual environment

# create virtual environment
python3 -m venv myvenv

# activate the virtual environment
source myvenv/bin/activate

# update pip
python3 -m pip install --upgrade pip
```

**Every time you want to use `pybes3`, make sure you have activated this virtual environment with command `source /path/to/install/myvenv/bin/activate`.**



Since there is a quota limitation on user's home path (`~/`), you may also need to create a symbolink for `~/.cache`, which will contain pip caches when installing python module.

```bash
# check whether a `.cache` directory already exists. If so, move it to somewhere else
ls -a ~
mv ~/.cache /path/to/somewhere

# link it back to `~`
ln -s /path/to/somewhere/.cache ~/.cache
```

### Package install

To install `pybes3`, directly run:

```bash
pip install pybes3
```

By so far, `pybes3` requires a C++ compiler to build its C++ binding. Make sure your environment has one.



## Usage

See links below for usage information:

* [besio](./doc/besio.md)
