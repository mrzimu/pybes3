import argparse
from pathlib import Path

sh_template = """if [[ -n "$@VAR@" ]]; then
    if [[ ! "$@VAR@" =~ "@VALUE@" ]]; then
        export @VAR@="@VALUE@:$@VAR@"
    else
        _newpath="@VALUE@"
        for dir in `echo $@VAR@ | tr ':' ' '`; do
            if [[ "$dir" != "@VALUE@" ]]; then
                _newpath="${_newpath}:${dir}"
            fi
        done
        export @VAR@="$_newpath"
    fi
else
    export @VAR@="@VALUE@"
fi
"""

csh_template = """if ( $?@VAR@ ) then
    if (`echo $@VAR@ | grep -q "@VALUE@"; echo $?`) == 1 then
        setenv @VAR@ "@VALUE@:$@VAR@"
    else
        set _newpath = "@VALUE@"
        foreach dir (`echo $@VAR@ | tr ':' ' '`)
            echo dir: $dir
            if ("$dir" != "@VALUE@") then
                set _newpath = "${_newpath}:${dir}"
            endif
        end
        setenv @VAR@ "$_newpath"
    endif
else
    setenv @VAR@ "@VALUE@"
endif
"""


def add_envvar(vars: dict[str, str], template: str) -> str:
    res = ''
    for var, value in vars.items():
        res += template.replace('@VAR@', var).replace('@VALUE@', value)
    return res


parser = argparse.ArgumentParser(description='Generate shell scripts to add environment variables.')

parser.add_argument('--shell', type=str, default='sh', choices=['sh', 'csh'],
                    help='Shell type')

args = parser.parse_args()

base_path = Path(__file__).parent.parent

if (base_path / 'lib').exists():
    lib_path = str(base_path / 'lib')
elif (base_path / 'lib64').exists():
    lib_path = str(base_path / 'lib64')
else:
    raise FileNotFoundError('No lib or lib64 directory found.')

if (base_path / 'python').exists():
    python_path = str(base_path / 'python')
else:
    raise FileNotFoundError('No python directory found.')

vars = {
    'LD_LIBRARY_PATH': lib_path,
    'PYTHONPATH': python_path
}

if args.shell == 'sh':
    res = add_envvar(vars, sh_template)
elif args.shell == 'csh':
    res = add_envvar(vars, csh_template)
else:
    raise ValueError('Invalid shell type.')

with open(base_path / f'setup.{args.shell}', 'w') as f:
    f.write(res)
