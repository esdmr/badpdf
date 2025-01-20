import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import deque
from itertools import groupby
from pathlib import Path
from typing import Iterable
from PIL import Image
from json import load
from gilbert.gilbert2d import gilbert2d


def window[T](seq: Iterable[T], n=2):
    window = deque[T](maxlen=n)

    for e in seq:
        window.append(e)

        if len(window) >= n:
            yield window

    while window:
        yield window


def deque_set[T](i: deque[T], *values: T):
    i.clear()
    i.extend(values)


def gilbert(data: list[int], width: int, height: int):
    assert len(data) == width * height

    for x, y in gilbert2d(width, height):
        yield data[int(x + y * width)]


def apply_rle(data: Iterable[int]):
    for curr, it in groupby(data):
        yield (curr, sum(1 for _ in it))


def apply_rle_u8(data: Iterable[tuple[int, int]]):
    for i, n in data:
        for _ in range(n // 0xFF):
            yield (i, 0xFF)

        yield (i, n % 0xFF)


def apply_rle_ord(data: Iterable[tuple[int, int]], *values: int):
    assert values
    queue = deque(values, maxlen=len(values))

    for i, n in data:
        assert i in values

        while queue[0] != i:
            yield 0
            queue.append(queue[0])

        yield n
        queue.append(i)


def apply_rle_bleed(rle: Iterable[int], max=255, max_bleed=8):
    for i in window(rle, 3):
        if len(i) != 3 or i[0] != 0 or max < i[1] + i[2] or max_bleed < i[1]:
            yield i.popleft()
        else:
            deque_set(i, sum(i))


def apply_rle_ridge(rle: Iterable[int], max=255, max_ridge=1):
    for i in window(rle, 3):
        if len(i) != 3 or max < i[0] + i[1] + i[2] or max_ridge < i[1]:
            yield i.popleft()
        else:
            deque_set(i, sum(i))


with open("options.json", "r") as f:
    options = load(f)
    GILBERT = bool(options["gilbert"])

frame_data = bytearray()

for file in sorted(Path("out").glob("*.png")):
    with Image.open(file, "r") as f:
        data = [int(i) // 128 for i in f.convert("L").getdata()]

        if GILBERT:
            data = gilbert(data, f.width, f.height)

        data = apply_rle(data)
        data = apply_rle_u8(data)
        data = apply_rle_ord(data, 0, 1)

        if not GILBERT:
            data = apply_rle_bleed(data)

        data = apply_rle_ridge(data)
        data = list(data)
        assert sum(data) == f.width * f.height
        n = len(data)

        frame_data.append(n % 256)
        frame_data.append(n // 256)
        frame_data.extend(data)

with open("out/frames.bin", "wb") as f:
    f.write(frame_data)
