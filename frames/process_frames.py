import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import deque
from itertools import groupby
from pathlib import Path
from typing import Iterable
from PIL import Image
from json import load
from gilbert.gilbert2d import gilbert2d
from pyvlq import encode


def window[T](seq: Iterable[T], n=2):
    window = deque[T]()

    for e in seq:
        window.append(e)

        while len(window) >= n:
            yield window

    while window:
        yield window


def deque_set[T](i: deque[T], *values: T):
    i.clear()
    i.extend(values)


def gilbert(
    data: list[int],
    width: int,
    height: int,
    cache: Iterable[tuple[int, int]] | None = None,
):
    assert len(data) == width * height

    for x, y in cache or gilbert2d(width, height):
        yield data[int(x + y * width)]


def apply_rle(data: Iterable[int]):
    for curr, it in groupby(data):
        yield (curr, sum(1 for _ in it))


def apply_rle_ord(data: Iterable[tuple[int, int]], *values: int):
    assert values
    queue = deque(values)

    for i, n in data:
        assert i in values

        while queue[0] != i:
            yield 0
            queue.rotate(-1)

        yield n
        queue.rotate(-1)


def apply_rle_ridge(rle: Iterable[int], max=1):
    for i in window(rle, 3):
        if len(i) != 3 or max < i[1]:
            yield i.popleft()
        else:
            deque_set(i, sum(i))


def apply_rle_plain(rle: Iterable[int], max=4):
    in_plain = False

    for i in window(rle, 3):
        if in_plain:
            if len(i) != 3 or max < i[1] or max < i[2]:
                in_plain = False
            else:
                deque_set(i, sum(i))
        else:
            if len(i) != 3 or max < i[0] or max < i[1] or max < i[2]:
                yield i.popleft()
            else:
                in_plain = True


def apply_rle_vlq(data: Iterable[int]):
    for i in data:
        yield from encode(i)


with open("options.json", "r") as f:
    options = load(f)
    GILBERT = bool(options["gilbert"])

with open("ffmpeg.json", "r") as f:
    ffmpeg_options = load(f)
    WIDTH = int(ffmpeg_options["width"])
    HEIGHT = int(ffmpeg_options["height"])

frame_data = bytearray()
gilbert_cache = list(gilbert2d(WIDTH, HEIGHT)) if GILBERT else None

for file in sorted(Path("out").glob("*.png")):
    with Image.open(file, "r") as f:
        assert f.width == WIDTH
        assert f.height == HEIGHT

        data = [int(i) >> 7 for i in f.convert("L").getdata()]

        if GILBERT:
            data = gilbert(data, f.width, f.height, gilbert_cache)

        data = apply_rle(data)
        data = apply_rle_ord(data, 0, 1)
        data = apply_rle_ridge(data)
        data = apply_rle_plain(data)
        data = apply_rle_vlq(data)

        data = list(data)
        frame_data.extend(encode(len(data)))
        frame_data.extend(data)

with open("out/frames.bin", "wb") as f:
    f.write(frame_data)
