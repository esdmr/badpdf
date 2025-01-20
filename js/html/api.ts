import {gilbert} from '../../frames/options.json';
import {width, height, fps} from '../../frames/ffmpeg.json';
import frames from '../../frames/out/frames.bin?uint8array&base64';
import { d2xy } from '#gilbert';

export const mspf = 1000 / fps;

const canvas = document.querySelector('canvas')!;
canvas.width = width;
canvas.height = height;

const ctx = canvas.getContext('2d')!;
const img = ctx.getImageData(0, 0, width, height);
const status = document.querySelector('p')!;
const play = document.querySelector('button')!;

const indexMap = Array.from({length: width * height}, (_, i) => {
	if (!gilbert) return i;
	const {x, y} = d2xy(i, width, height)
	return x + y * width;
});

console.log(indexMap);

export {frames};
export const setInterval = globalThis.setInterval;
export const clearInterval = globalThis.clearInterval;

export function setPlayButtonVisibility(v: boolean) {
	play.hidden = !v;
}

export function startFrame() {
	// Do nothing
}

export function endFrame(index: number, frame: number, skippedFrames: number) {
	ctx.putImageData(img, 0, 0);

	status.innerText = `${frame.toString().padStart(4, '0')}: ${index.toString().padStart(6, '0')}/${frames.length.toString().padStart(6, '0')} bytes (${((index / frames.length) * 100).toFixed(2).padStart(5, '0')}%), ${skippedFrames.toString().padStart(4, '0')} skipped (${((skippedFrames / frame) * 100).toFixed(2).padStart(5, '0')}%), ${width}*${height} pixels, ${fps} Hz = ${mspf} ms`;
}

export function setPixel(index: number, active: boolean) {
	img.data[indexMap[index] * 4 + 0] = active ? 255 : 0;
	img.data[indexMap[index] * 4 + 1] = active ? 255 : 0;
	img.data[indexMap[index] * 4 + 2] = active ? 255 : 0;
	img.data[indexMap[index] * 4 + 3] = 255;
}
