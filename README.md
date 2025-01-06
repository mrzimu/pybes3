# pybes3

## Overview

`pybes3` is an **unofficial** python module that aims to make BES3 user easier to work with Python. It includes:

* [besio](./doc/besio.md): An I/O submodule that can directly read BES3 `rtraw`, `dst`, `rec` files, and transfer their data to `awkward` array.



## Installation

### On lxlogin

Since there is a quota limitation on user's home path (`~/`), you may also need to create a symbolink for `~/.local`, which will contain pip packages that installed in "user mode":

```bash
# Check whether a `.local` directory already exists. If so, move it to somewhere else
ls -a ~
mv ~/.local /path/to/somewhere/

# If no `.local` exists, create one
mkdir /path/to/somewhere/.local

# Link it back to `~`
ln -s /path/to/somewhere/.local ~/.local
```

Then install `pybes3` in user mode:

```bash
pip install --user pybes3
```

### On PC

For PC users, it is sufficient to directly execute:

```bash
pip install pybes3
```



## Usage

See links below for usage information:

* [besio](./doc/besio.md)
