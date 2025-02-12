### on lxlogin server

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

Then install `pybes3` in user mode:

```bash
pip install --user pybes3
```

!!! note
    If you are using different python version, you need to install `pybes3` for each of major version.

### on PC

For PC users, it is sufficient to directly execute:

```bash
pip install pybes3
```
