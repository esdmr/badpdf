/// <reference no-default-lib="true" />
/// <reference lib="es2020" />
/// <reference path="./pdf.d.ts" />
'use strict';

// #region Interface Init

const frames = b64_to_uint8array('###FRAME_DATA###');
const width = Number('###GRID_WIDTH###');
const height = Number('###GRID_HEIGHT###');
const fps = Number('###FPS###');

/** @type {Field} */
let statusField = getField('T_stat');
/** @type {Field[]} */
const fields = [];
/** @type {boolean[]} */
const fieldValues = [];

for (let y = height - 1; y >= 0; y--) {
	for (let x = 0; x < width; x++) {
		fields.push(getField(`P_${x}_${y}`));
		fieldValues.push(false);
	}
}

app.execMenuItem('FitPage');
// #endregion
// #region Generic Init
let index = 0;
let frame = 0;
let skippedFrames = 0;
let lastTime = 0;

const mspf = 1000 / fps;
let interval = 0;

globalThis.onFrame = onFrame;
globalThis.onInit = onInit;

// #endregion
// #region Interface Methods

/**
 * @see https://stackoverflow.com/a/62364519
 * @see https://github.com/ading2210/doompdf/blob/b38e0d7d346d1cc1101eb35d3d66ff32eee1efeb/file_template.js
 *
 * @param {string} str
 */
function b64_to_uint8array(str) {
	const abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
	const result = [];

	for(let i = 0; i < str.length / 4; i++) {
		const bin = str
			.slice(4 * i, 4 * i + 4)
			.split('')
			.map((x) => abc.indexOf(x).toString(2).padStart(6, '0'))
			.join('');

		const bytes = bin
			.match(/.{1,8}/g)
			?.map((x) => parseInt(x, 2)) ?? [];

		result.push(...bytes.slice(0, 3 - +(str[4*i+2]=='=') - +(str[4*i+3]=='=')));
	}

	return new Uint8Array(result);
}

/**
 * @param {string} fn
 * @param {number} ms
 * @returns {number}
 */
function setInterval(fn, ms) {
	return app.setInterval(fn, ms);
}

/** @param {number} i */
function clearInterval(i) {
	app.clearInterval(i);
}

/**
 * @param {boolean} v
 */
function setPlayButtonVisibility(v) {
	getField('B_play').hidden = !v;
}

function startFrame() {
	delay = true;
}

function endFrame() {
	delay = false;

	statusField.value = `${frame.toString().padStart(4, '0')}: ${index.toString().padStart(6, '0')}/${frames.length.toString().padStart(6, '0')} bytes (${(index / frames.length * 100).toFixed(2).padStart(5, '0')}%), ${skippedFrames.toString().padStart(4, '0')} skipped (${(skippedFrames / frame * 100).toFixed(2).padStart(5, '0')}%), ${width}*${height} pixels, ${fps} Hz = ${mspf} ms`;
}

/**
 * @param {number} index
 * @param {boolean} active
 */
function setPixel(index, active) {
	if (fieldValues[index] !== active) {
		fields[index].hidden = active;
		fieldValues[index] = active;
	}
}

// #endregion
// #region Generic Methods

function readFrameLength() {
	return frames[index++] + frames[index++] * 256;
}

function onFrame() {
	if (index >= frames.length) {
		setPlayButtonVisibility(true);
		app.clearInterval(interval);
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
	endFrame();
}

function onInit() {
	setPlayButtonVisibility(false);
	index = 0;
	frame = 0;
	skippedFrames = 0;
	lastTime = Date.now();
	interval = setInterval('onFrame();', mspf);
}

//#endregion
