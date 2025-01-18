/// <reference no-default-lib="true" />
/// <reference lib="es2020" />

import {
	mspf,
	frames,
	setInterval,
	clearInterval,
	endFrame,
	setPixel,
	setPlayButtonVisibility,
	startFrame,
} from '#api';

declare global {
	var onFrame: () => void;
	var onInit: () => void;
}

let index = 0;
let frame = 0;
let skippedFrames = 0;
let lastTime = 0;
let interval = 0;

globalThis.onFrame = onFrame;
globalThis.onInit = onInit;

function readFrameLength() {
	return frames[index++] + frames[index++] * 256;
}

function onFrame() {
	if (index >= frames.length) {
		setPlayButtonVisibility(true);
		clearInterval(interval);
		return;
	}

	const time = Date.now();
	const deltaFrames = Math.trunc((time - lastTime) / mspf);

	if (deltaFrames < 1) return;

	for (let i = 1; i < deltaFrames && index < frames.length; i++) {
		index = readFrameLength() + index;
	}

	const end = readFrameLength() + index;
	startFrame();

	let active = false;
	let pixelIndex = 0;

	for (; index < end; index++) {
		for (let i = frames[index]; i > 0; i--) {
			setPixel(pixelIndex++, active);
		}

		active = !active;
	}

	frame += deltaFrames;
	skippedFrames += deltaFrames - 1;
	lastTime += deltaFrames * mspf;
	endFrame(index, frame, skippedFrames);
}

function onInit() {
	setPlayButtonVisibility(false);
	index = 0;
	frame = 0;
	skippedFrames = 0;
	lastTime = Date.now();
	interval = setInterval('onFrame();', mspf);
}
