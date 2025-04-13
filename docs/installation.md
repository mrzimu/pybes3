!!! info
    `pybes3` requires Python 3.9 or higher.

## Users on lxlogin server

"lxlogin server" means the login server of computation clusters of IHEP. Since there is a quota limitation on user's home path (`~/`), you may also need to create symbolinks for `~/.local` and `~/.cache`, which contains pip caches and packages that installed in "user mode":

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

## Install `pybes3` using pip

```bash
pip install pybes3
```
