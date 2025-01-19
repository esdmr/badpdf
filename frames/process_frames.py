import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import deque
from itertools import groupby, islice
from pathlib import Path
from typing import Iterable
from PIL import Image
from json import load
from gilbert.gilbert2d import gilbert2d


def window[T](seq: Iterable[T], n=2):
    it = iter(seq)
    window = deque(islice(it, n), maxlen=n)
    yield window

    for e in it:
        window.append(e)
        yield window

    while window:
        window.popleft()

        if window:
            yield window


def gilbert(data: list[int], width: int, height: int):
    assert len(data) == width * height

    for x, y in gilbert2d(width, height):
        yield data[x + y * width]


def get_rle(data: Iterable[int], values=2, max=255):
    next = 0

    for curr, it in groupby(data):
        for _ in range((curr - next) % values):
            yield 0

        n = sum(1 for _ in it)

        for _ in range(n // max):
            yield max

            for _ in range(values - 1):
                yield 0

        yield n % max

        next = (curr + 1) % values


def apply_rle_bleed0(rle: Iterable[int], max=255, max_bleed=255):
    skip = 0

    for i in window(rle, 3):
        if skip:
            skip -= 1
        elif len(i) < 3 or i[0] != 0 or max < i[1] + i[2] or max_bleed < i[1]:
            yield i[0]
        else:
            yield i[1] + i[2]
            skip = 2


def apply_rle_ridge(rle: Iterable[int], max=255, max_ridge=1):
    skip = 0

    for i in window(rle, 3):
        if skip:
            skip -= 1
        elif len(i) < 3 or max < i[0] + i[1] + i[2] or max_ridge < i[1]:
            yield i[0]
        else:
            yield i[0] + i[1] + i[2]
            skip = 2


with open("options.json", "r") as f:
    options = load(f)

frame_data = bytearray()

for file in sorted(Path("out").glob("*.png")):
    with Image.open(file, "r") as f:
        data = [int(i // 128) for i in f.convert("L").getdata()]

        if options["gilbert"]:
            data = gilbert(data, f.width, f.height)

        data = get_rle(data)

        if not options["gilbert"]:
            data = apply_rle_bleed0(data)

        for _ in range(2):
            data = apply_rle_ridge(data)

        data = list(data)
        n = len(data)

        frame_data.append(n % 256)
        frame_data.append(n // 256)
        frame_data.extend(data)

with open("out/frames.bin", "wb") as f:
    f.write(frame_data)
