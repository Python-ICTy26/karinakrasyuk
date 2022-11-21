import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f"{fmt} {len(data)}\0"
    store = header.encode() + data
    res = hashlib.sha1(store).hexdigest()
    if write:
        path = repo_find() / "objects" / res[:2]
        if not path.exists():
            path.mkdir(parents=True)
        workdir = path / res[2:]
        with open(workdir, "wb") as f:
            f.write(zlib.compress(store))
    return res


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if len(obj_name) > 40 or len(obj_name) < 4:
        raise Exception(f"Not a valid object name {obj_name}")
    res = []
    paths = gitdir / "objects" / obj_name[:2]
    for path in paths.iterdir():
        if obj_name[2:] in str(path.parts[-1]):
            res.append(str(path.parts[-2]) + str(path.parts[-1]))
    if len(res) > 0:
        return res
    else:
        raise Exception(f"Not a valid object name {obj_name}")


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = gitdir / "objects" / sha[:2] / sha[2:]
    with open(path, "rb") as f:
        data = zlib.decompress(f.read())
        ind1 = data.find(b"\x00")
        head = data[:ind1]
        ind2 = head.find(b" ")
        head = head[:ind2]
        data = data[ind1 + 1 :]
        return head.decode(), data


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    res = []
    while len(data):
        mode = int(data[: data.find(b" ")].decode())
        data = data[data.find(b" ") + 1 :]
        name = data[: data.find(b"\x00")].decode()
        data = data[data.find(b"\x00") + 1 :]
        sha = bytes.hex(data[:20])
        data = data[20:]
        res += [(mode, name, sha)]
    return res


def cat_file(obj_name: str, pretty: bool = True) -> None:
    path = repo_find()
    for element in resolve_object(obj_name, path):
        header, data = read_object(element, path)
        if header == "tree":
            res = ""
            files = read_tree(data)
            for file in files:
                res += f"{str(file[0]).zfill(6)} {read_object(file[2], repo_find())[0]} {file[2]}\t{file[1]}\n"
            print(res)
        else:
            print(data.decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    res = []
    _, data = read_object(tree_sha, gitdir)
    for element in read_tree(data):
        if read_object(element[2], gitdir)[0] == "tree":
            tree = find_tree_files(element[2], gitdir)
            for el in tree:
                name = element[1] + "/" + el[0]
                res += [(name, el[1])]
        else:
            res += [(element[1], element[2])]
    return res


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    index = data.find(b"tree")
    return data[index + 5 : index + 45]
