import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        values = [
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            self.name.encode(),
        ]
        return struct.pack(
            f"!4L6i20sh{len(self.name)}s3x",
            *values,
        )

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        f = "!4L6i20sh" + str(len(data) - 62) + "s"
        unpacked = list(struct.unpack(f, data))
        unpacked[-1] = unpacked[-1][: len(unpacked[12]) - 3].decode()
        return GitIndexEntry(*unpacked)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    if not (gitdir / "index").exists():
        return []
    with open(gitdir / "index", "rb") as file:
        data = file.read()
    answer = []
    len_data = int.from_bytes(data[8:12], "big")
    j = 0
    data = data[12:-20]
    for i in range(len_data):
        need = b"\x00\x00\x00"
        end = data[j + 62 :].find(need) + j + 62 + 3
        answer.append(GitIndexEntry.unpack(data[j:end]))
        j = end
    return answer


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    with open(gitdir / "index", "wb") as f:
        values = (b"DIRC", 2, len(entries))
        hash1 = struct.pack("!4s2i", *values)
        f.write(hash1)
        for element in entries:
            hash1 += element.pack()
            f.write(element.pack())
        hash2 = hashlib.sha1(hash1).hexdigest()
        res = bytes.fromhex(hash2)
        f.write(struct.pack("!" + str(len(res)) + "s", res))


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    for element in read_index(gitdir):
        if not details:
            print(element.name)
        else:
            print(str(oct(element.mode))[2:] + " " + str(element.sha1.hex()) + " 0	" + element.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    if (gitdir / "index").exists():
        res = read_index(gitdir)
    else:
        res = []
    for path in paths:
        f = open(path, "rb")
        str_f = f.read()
        sha = hash_object(str_f, "blob", True)
        stat = os.stat(path)
        res.append(
            GitIndexEntry(
                ctime_s=int(stat.st_ctime),
                ctime_n=0,
                mtime_s=int(stat.st_mtime),
                mtime_n=0,
                dev=stat.st_dev,
                ino=stat.st_ino,
                mode=stat.st_mode,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                sha1=bytes.fromhex(sha),
                flags=7,
                name=str(path).replace("\\", "/"),
            )
        )
        res = sorted(res, key=lambda x: x.name)
        write_index(gitdir, res)
