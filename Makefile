build: bad.pdf

bad.pdf: frames/options.json frames/ffmpeg.json generate.py js/out/bad.js uv.lock
	uv run generate.py

frames/out/frames.bin: frames/out/build.txt frames/options.json frames/process_frames.py uv.lock
	cd frames; uv run process_frames.py

frames/out/build.txt: frames/src/badapple.mp4 frames/ffmpeg.json frames/create-frames.sh
	cd frames; sh create-frames.sh

uv.lock: pyproject.toml
	uv sync
	touch uv.lock

dev: frames/out/frames.bin js/pnpm-lock.yaml
	cd js; corepack pnpm vite

preview: js/out/index.html js/pnpm-lock.yaml
	cd js; corepack pnpm vite preview

js/out/index.html: frames/out/frames.bin frames/options.json frames/ffmpeg.json js/html/index.html js/shared/index.ts js/html/api.ts js/pnpm-lock.yaml js/vite.config.ts
	cd js; corepack pnpm vite build -m html

js/out/bad.js: frames/out/frames.bin frames/options.json frames/ffmpeg.json js/shared/index.ts js/pdf/api.ts js/pnpm-lock.yaml js/vite.config.ts
	cd js; corepack pnpm vite build -m pdf

js/pnpm-lock.yaml: js/package.json
	cd js; pnpm i
	touch js/pnpm-lock.yaml

.PHONY: build preview dev
