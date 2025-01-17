#!/bin/sh
rm -rf out
mkdir -p out
ffmpeg -i src/badapple.mp4 -filter:v "scale=$(sed '1q;d' options.txt):$(sed '2q;d' options.txt)" -r "$(sed '3q;d' options.txt)" out/%04d.png
date >out/build.txt
