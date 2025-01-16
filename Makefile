bad.pdf: frames/out/frames.bin frames/options.txt generate.py index.js
	uv run generate.py

preview: bad.html
	uv run python -m http.server

bad.html: frames/out/frames.bin frames/options.txt

frames/out/frames.bin: frames/out/build.txt frames/out/*.png frames/process_frames.py
	cd frames; uv run process_frames.py

frames/out/*.png:

frames/out/build.txt: frames/src/badapple.mp4 frames/options.txt frames/create-frames.sh
	cd frames; sh create-frames.sh
