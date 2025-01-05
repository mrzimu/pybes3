#!/usr/bin/env python3

import sys
import subprocess
import argparse
import re
from pathlib import Path


cpp_suffix = {'c', 'cc', 'cxx', 'cpp', 'C', 'h', 'hh', 'hxx', 'hpp', 'icc', 'ihh'}

# =============================================================
#                     Predifined functions
# =============================================================


def pos_int(value: str) -> int:
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f'{value} is not a positive integer')

    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f'{value} is not a positive integer')
    return ivalue


def format_single_file(fpath: str, src_dir: Path, style_file: Path) -> bool:
    proc = subprocess.run(['clang-format',
                           '--fallback-style=Google',
                          f'--style=file:{style_file}',
                           '-i', fpath], cwd=src_dir)
    if proc.returncode != 0:
        print(f'Format failed: {fpath}')
    return proc.returncode == 0


def format_files(files: list, src_dir: Path, style_file: Path, njobs: int) -> None:
    with ProcessPoolExecutor(max_workers=njobs) as executor:
        executor.map(format_single_file, files, [src_dir] * len(files), [style_file] * len(files))


# =============================================================
#                        Parse arguments
# =============================================================
usage = """
    - Format all changed C++ files in the repository:
        ./format_code.py

    - Format all C++ files in the repository:
        ./format_code.py --all

    - Format a single C++ file:
        ./format_code.py -f <file>
"""

parser = argparse.ArgumentParser(
    description='Format C++ code using clang-format.',
    usage=usage)

parser.add_argument('--source-dir', type=str, default='.',
                    help='source directory, default is current directory')

parser.add_argument('-f', '--file', action='store',
                    help='Format a single C++ file')

parser.add_argument('--staged', action='store_true',
                    help='Format staged files and add them back to the staging area')

parser.add_argument('--all', action='store_true',
                    help='Format all C++ files in the repository')

parser.add_argument('-j', '--jobs', type=pos_int, default=16,
                    help='Number of jobs to run in parallel, only available when --all is set')

args = parser.parse_args()

# =============================================================
#                     Format all c++ files
# =============================================================
src_dir = Path(args.source_dir).resolve()

style_file = Path(__file__).parent.parent / '.clang-format'
if not style_file.exists():
    print(f'Error: style file {style_file} not found')
    sys.exit(1)

if args.all:
    import re
    from glob import glob
    from concurrent.futures import ProcessPoolExecutor

    # Find cpp files
    cpp_files = set(sum([
        glob(f'{src_dir}/**/*.{suffix}', recursive=True) for suffix in cpp_suffix
    ], []))

    # Find fortran header files
    fortran_src = glob(f'{src_dir}/**/*.f', recursive=True) + glob(f'{src_dir}/**/*.F', recursive=True)
    fortran_inc = set()
    for f in fortran_src:
        dir_name = Path(f).parent
        code = open(f, errors='replace').read()
        fortran_inc |= {
            dir_name / i for i in re.findall(r"INCLUDE\s*'(.*)'", code) + re.findall(r"include\s*'(.*)'", code) if i.endswith(".h")}

    common_files = cpp_files & fortran_inc
    if common_files:
        print("Some fortran header files with '.h' suffix are found, it is recommended to change the suffix to '.inc':")
        for f in common_files:
            print(f)

    cpp_files -= fortran_inc

    print(f'Formatting {len(cpp_files)} C++ files...')

    try:
        format_files(list(cpp_files), src_dir, style_file, args.jobs)
        sys.exit(0)
    except Exception as e:
        print(f'Error formatting files: {e}')
        sys.exit(1)

# =============================================================
#                    Format single c++ files
# =============================================================
if args.file:
    if not (src_dir / args.file).exists():
        print(f'Error: {args.file} not found')
        sys.exit(1)

    if not format_single_file(args.file, src_dir, style_file):
        sys.exit(1)

    print(f'Formatted: {args.file}')
    sys.exit(0)

# =============================================================
#                     Format diff files
# - if --staged is set:
#   Will format only staged files and add them back
#
# - if --staged is not set:
#   Will format all changed files
# =============================================================
if not (src_dir / '.git').exists():
    print(f'Error: {src_dir} is not a valid git repository')
    sys.exit(1)

diffs_staged = subprocess.run(['git', 'diff', '--cached', '--name-only', 'HEAD'],
                              stdout=subprocess.PIPE, cwd=src_dir, start_new_session=True)

if diffs_staged.returncode != 0:
    print('Error running git diff')
    sys.exit(1)

diffs_staged = diffs_staged.stdout.decode('utf-8').strip().split('\n')
cpp_staged = set([f for f in diffs_staged if ('.' in f and f.split('.')[-1] in cpp_suffix)])

for f in cpp_staged:
    if format_single_file(f, src_dir, style_file):
        proc = subprocess.run(['git', 'add', f], cwd=src_dir)
        if proc.returncode != 0:
            print(f'Error adding {f} back to the staging area')
            sys.exit(1)
        print(f'Formatted and added back: {f}')
    else:
        sys.exit(1)

if args.staged:  # if --staged, exit
    sys.exit(0)

# if not --staged, format all changed files
diffs_all = subprocess.run(['git', 'diff', '--name-only'],
                           stdout=subprocess.PIPE, cwd=src_dir, start_new_session=True)

if diffs_all.returncode != 0:
    print('Error running git diff')
    sys.exit(1)

diffs_all = diffs_all.stdout.decode('utf-8').strip().split('\n')
cpp_all = set([f for f in diffs_all if ('.' in f and f.split('.')[-1] in cpp_suffix)])
cpp_not_staged = cpp_all - cpp_staged

for f in cpp_not_staged:
    if format_single_file(f, src_dir, style_file):
        print(f'Formatted: {f}')
    else:
        print(f'Error formatting {f}')
        sys.exit(1)
