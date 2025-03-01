# pybes3

`pybes3` is an **unofficial** python module that aims to make BES3 users easier to work with Python.


It is highly recommended to take a look at [awkward](https://awkward-array.org/doc/stable/index.html) and [uproot](https://uproot.readthedocs.io/en/stable/) documentations before using `pybes3`.

## Documentation

Visit the [documentation](https://pybes3.readthedocs.io/en/stable/) for more information about installation, usage, and examples.

## Installation

### on lxlogin

Since there is a quota limitation on user's home path (`~/`), you may also need to create a symbolink for `~/.local`, which will contain pip packages that installed in "user mode":

```bash
# Check whether a `.local` directory and `.cache` already exists.
# If so, move it to somewhere else.
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

> If you are using different python version, you need to install `pybes3` for each of major version.

### on PC

For PC users, it is sufficient to directly execute:

```bash
pip install pybes3
```
