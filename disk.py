import os


def get_size(path):

    fs = os.statvfs(path)

    free = fs.f_bfree * fs.f_bsize
    total = fs.f_blocks * fs.f_bsize
    used = (fs.f_blocks - fs.f_bfree) * fs.f_bsize

    return free, total, used
