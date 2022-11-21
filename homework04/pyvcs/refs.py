import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    path = gitdir / pathlib.Path(ref)
    with open(path, "w") as file:
        file.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    if ref_resolve(gitdir, ref):
        path = gitdir / name
        with open(path, "w") as file:
            file.write(f"ref: {ref}")


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == "HEAD":
        refname = get_ref(gitdir)
    path = gitdir / refname
    if path.exists():
        with open(path, "r") as f:
            return f.read()
    else:
        return refname


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    path = gitdir / get_ref(gitdir)
    if path.exists():
        return ref_resolve(gitdir, "HEAD")
    else:
        return None


def is_detached(gitdir: pathlib.Path) -> bool:
    path = gitdir / "HEAD"
    with open(path, "r") as f:
        data = str(f.read())
    if "ref" not in data:
        return True
    else:
        return False


def get_ref(gitdir: pathlib.Path) -> str:
    path = gitdir / "HEAD"
    with open(path, "r") as f:
        return f.read()[f.read().find(" ") + 1 :]
