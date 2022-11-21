import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    gitdir = os.getenv("GIT_DIR", ".git")
    cur = pathlib.Path(workdir)
    path = cur / gitdir
    if path.exists():
        return path
    for directory in path.parents:
        if directory.name == gitdir:
            return directory
    raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    workdir = pathlib.Path(workdir)
    if not workdir.is_dir():
        raise Exception(f"{workdir.name} is not a directory")
    gitdir = os.getenv("GIT_DIR", ".git")
    os.makedirs(workdir / gitdir / "refs" / "tags")
    os.makedirs(workdir / gitdir / "objects")
    os.makedirs(workdir / gitdir / "refs" / "heads")

    (workdir / gitdir / "HEAD").write_text("ref: refs/heads/master\n")
    (workdir / gitdir / "config").write_text(
        "[core]\n\trepositoryformatversion = 0\n\tfilemode = true"
        "\n\tbare = false\n\tlogallrefupdates = false\n"
    )
    (workdir / gitdir / "description").write_text("Unnamed pyvcs repository.\n")
    return workdir / gitdir
