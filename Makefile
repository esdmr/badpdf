build: bad.pdf

bad.pdf: frames/options.txt generate.py js/out/bad.js uv.lock
	uv run generate.py

frames/out/frames.bin: frames/out/build.txt frames/process_frames.py uv.lock
	cd frames; uv run process_frames.py

frames/out/build.txt: frames/src/badapple.mp4 frames/options.txt frames/create-frames.sh
	cd frames; sh create-frames.sh

uv.lock: pyproject.toml
	uv sync

preview: frames/out/frames.bin js/pnpm-lock.yaml
	cd js; corepack pnpm vite

js/out/bad.js: frames/out/frames.bin frames/options.txt js/index.ts js/pdf-api.ts js/pnpm-lock.yaml js/vite.config.ts
	cd js; corepack pnpm vite build -m pdf

js/pnpm-lock.yaml: js/package.json
	cd js; pnpm i

.PHONY: build preview
