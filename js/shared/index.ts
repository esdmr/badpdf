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
	var onNextFrame: () => void;
	var onPauseResume: () => void;
}

let index = 0;
let frame = 0;
let skippedFrames = 0;
let lastTime = -1;
let interval: unknown;

globalThis.onFrame = onFrame;
globalThis.onInit = onInit;
globalThis.onNextFrame = onNextFrame;
globalThis.onPauseResume = onPauseResume;

function readFrameLength() {
	return frames[index++] + frames[index++] * 256;
}

function onFrame() {
	if (index >= frames.length) {
		setPlayButtonVisibility(true);
		clearInterval(interval);
		lastTime = -1;
		interval = undefined;
		return;
	}

	const time = Date.now();
	const deltaFrames = Math.trunc((time - lastTime) / mspf);

	if (deltaFrames < 1) return;

	for (let i = 1; i < deltaFrames && index < frames.length; i++) {
		index = readFrameLength() + index;
	}

	frame += deltaFrames - 1;
	skippedFrames += deltaFrames - 1;
	lastTime += deltaFrames * mspf;
	onNextFrame();
}

function onNextFrame() {
	if (lastTime < 0) return;

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

	frame++;
	endFrame(index, frame, skippedFrames);
}

function onPauseResume() {
	if (lastTime < 0) {
		onInit();
		return;
	}

	if (interval === undefined) {
		lastTime = Date.now();
		interval = setInterval('onFrame();', mspf);
	} else {
		clearInterval(interval);
		interval = undefined;
	}
}

function onInit() {
	setPlayButtonVisibility(false);
	index = 0;
	frame = 0;
	skippedFrames = 0;
	lastTime = Date.now();
	interval = setInterval('try{onFrame();}catch(error){app.alert(String(error))}	', mspf);
}
