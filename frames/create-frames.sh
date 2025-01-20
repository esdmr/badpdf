#!/bin/sh
rm -rf out
mkdir -p out
ffmpeg -i src/badapple.mp4 -filter:v "scale=$(jq .width ffmpeg.json):$(jq .height ffmpeg.json)" -r "$(jq .fps ffmpeg.json)" out/%04d.png
date >out/build.txt
