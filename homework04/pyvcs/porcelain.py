import os
import pathlib
import shutil
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    ind = read_index(gitdir)
    return commit_tree(gitdir, write_tree(gitdir, ind), message, author)


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    file = gitdir / "refs" / "heads" / obj_name
    if file.exists():
        with open(file, "r") as f:
            obj_name = f.read()
    ind = read_index(gitdir)
    for element in ind:
        if pathlib.Path(element.name).is_file():
            if "/" in element.name:
                pos = element.name.find("/")
                shutil.rmtree(element.name[:pos])
            else:
                os.chmod(element.name, 0o777)
                os.remove(element.name)
    path = gitdir / "objects" / obj_name[:2] / obj_name[2:]
    f.close()
    with open(path, "rb") as f1:
        tree = commit_parse(f1.read()).decode()
    f1.close()
    for el in find_tree_files(tree, gitdir):
        if "/" in el[0]:
            pos = el[0].find("/")
            dir_name = el[0][:pos]
            os.mkdir(dir_name)
        with open(el[0], "w") as f:
            _, content = read_object(el[1], gitdir)
            f.write(content.decode())
