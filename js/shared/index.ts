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

function readNextInt() {
	let value = 0;
	let more: number;

	do {
		if (index >= frames.length) {
			throw new RangeError('Incomplete VLQ found');
		}

		const byte = frames[index++];
		value = ((value << 7) | (byte & 0x7F));
		more = (byte >> 7);
	} while (more);

	return value;
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
		index = readNextInt() + index;
		frame++;
		skippedFrames++;
	}

	lastTime += deltaFrames * mspf;
	onNextFrame();
}

function onNextFrame() {
	if (index >= frames.length) return;

	const end = readNextInt() + index;
	startFrame();
	let active = false;
	let pixelIndex = 0;

	while (index < end) {
		const length = readNextInt();

		for (let i = 0; i < length; i++) {
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
	interval = setInterval('onFrame();', mspf);
}
