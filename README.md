# pybes3

## Overview

`pybes3` is an **unofficial** python module that aims to make BES3 user easier to work with Python. It includes:

* [besio](./doc/besio.md): An I/O submodule that can directly read BES3 `rtraw`, `dst`, `rec` files, and transfer their data to `awkward` array.



## Installation

### On lxlogin

Since there is a quota limitation on user's home path (`~/`), you may also need to create a symbolink for `~/.local`, which will contain pip packages that installed in "user mode":

```bash
# Check whether a `.local` directory and `.cache` already exists. If so, move it to somewhere else
ls -a ~
mv ~/.local /path/to/somewhere/
mv ~/.cache /path/to/somewhere

# If no `.local` or `.cache` exists, create them
mkdir /path/to/somewhere/.local
mkdir /path/to/somewhere/.cache

# After moving or creating them, link them back to `~`
ln -s /path/to/somewhere/.local ~/.local
ln -s /path/to/somewhere/.cache ~/.cache
```

Then install `pybes3` in user mode:

```bash
pip install --user pybes3
```

> If you are using different python version, you need to install `pybes3` for each of version.

### On PC

For PC users, it is sufficient to directly execute:

```bash
pip install pybes3
```



## Usage

See links below for usages:

* [besio](./doc/besio.md): Read `.raw`, `.rtraw`, `.dst`, `.rec` files and transfer their data to `awkward` array.

