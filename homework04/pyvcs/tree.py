import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree = b""
    for element in index:
        files = oct(element.mode)[2:].encode()
        if "/" in element.name:
            tree += b"40000 "
            pos = element.name.find("/")
            dirname = element.name[:pos]
            temp = files + b" " + element.name[pos + 1 :].encode() + b"\0" + element.sha1
            hash = bytes.fromhex(hash_object(temp, fmt="tree", write=True))
            tree += dirname.encode() + b"\0" + hash
        else:
            tree += files + b" " + element.name.encode() + b"\0" + element.sha1
    return hash_object(tree, fmt="tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    if time.timezone > 0:
        timezone = "-"
    else:
        timezone = "+"
    timezone += (
            "0" + str(abs(time.timezone) // 60 // 60) + "0" + str((abs(time.timezone) // 60 % 60))
    )
    data = ["tree " + str(tree)]
    if parent is not None:
        data.append("parent " + str(parent))
    print(
        ("author " + author + " " + str(int(time.mktime(time.localtime()))) + " " + str(timezone))
    )
    data.append(
        "author " + author + " " + str(int(time.mktime(time.localtime()))) + " " + str(timezone)
    )
    data.append(
        "committer " + author + " " + str(int(time.mktime(time.localtime()))) + " " + str(timezone)
    )
    data.append("\n" + message + "\n")
    return hash_object("\n".join(data).encode(), "commit", write=True)
