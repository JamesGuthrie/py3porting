# Copyright (c) James Guthrie <james@prodigi.ch>, 2015 under the terms
# and conditions of the GPLv3+

import pickle
import argparse 

from typing import Iterator, List, Dict, Set, Any
from debian.deb822 import Packages

def get_args() -> Any:
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--package-list', required=True, help='Path to the debian package list')
    parser.add_argument('-c', '--cache',        default="",    help='File in which to cache intermediate results')
    return parser.parse_args()

def read_cache(cache: str) -> Set[str]:
    with open(cache, 'rb') as pickled_repo:
        return pickle.load(pickled_repo)


def write_cache(cache: str, repo: Set[str]) -> None:
    with open(cache, 'wb') as pickled_repo:
        pickle.dump(repo, pickled_repo)


def read_packages(file_path:str) -> Set[str]:
    with open(file_path, 'r') as fd:
        repo = {pkg['package'] for pkg in Packages.iter_paragraphs(fd)}
        return repo

def prepare_repo(file_path: str, cache: str="") -> Set[str]:
    if (len(cache) > 0):
        try:
            return read_cache(cache)
        except:
            repo = read_packages(file_path)
            write_cache(cache, repo)
            return repo
    else:
        repo = read_packages(file_path)
        return repo


def python_packages(repo: Set[str]) -> Iterator[str]:
    for pkg in repo:
        if pkg.startswith("python-"):
            yield pkg

def main():
    args = get_args()
    repo = prepare_repo(args.package_list, cache=args.cache)
    for pkg in python_packages(repo):
        py3_pkg = pkg.replace("python-", "python3-")
        if not py3_pkg in repo:
            print(pkg)

if __name__ == "__main__":
    main()
