#!/bin/sh
rm -rf out
mkdir -p out
ffmpeg -i src/badapple.mp4 -filter:v "scale=$(jq .width options.json):$(jq .height options.json)" -r "$(jq .fps options.json)" out/%04d.png
date >out/build.txt
