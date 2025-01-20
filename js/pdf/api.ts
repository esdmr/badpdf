import {gilbert, rows, char0, char1} from '../../frames/options.json';
import {width, height, fps} from '../../frames/ffmpeg.json';
import frames from '../../frames/out/frames.bin?uint8array&base64';
import {d2xy} from '#gilbert';

export const mspf = 1000 / fps;

let statusField = getField('T_stat');
const fields: Field[] = [];
const fieldValues: boolean[] = [];
const rowValues: string[][] = [];
const indexMap: {x: number, y: number, i: number}[] = [];
const length = width * height;

for (let i = 0; i < length; i++) {
	if (gilbert) {
		const result = d2xy(i, width, height);
		indexMap.push({...result, i: result.x + result.y * width});
	} else {
		indexMap.push({
			x: i % width,
			y: Math.trunc(i / width),
			i,
		});
	}
}

if (rows) {
	for (let y = 0; y < height; y++) {
		fields.push(getField(`R_${height - y - 1}`));
		rowValues.push(Array.from({length: width}, () => char0));
	}
} else {
	for (let i = 0; i < length; i++) {
		const {x, y} = indexMap[i];
		fields.push(getField(`P_${x}_${height - y - 1}`));
		fieldValues.push(false);
	}
}

try {
	app.execMenuItem('FitPage');
} catch {}

export {frames};

export function setInterval(fn: string, ms: number): unknown {
	return app.setInterval(fn, ms);
}

export function clearInterval(i: unknown) {
	app.clearInterval(i);
}

export function setPlayButtonVisibility(v: boolean) {
	getField('B_play').hidden = !v;
}

export function startFrame() {
	delay = true;
}

export function endFrame(index: number, frame: number, skippedFrames: number) {
	if (rows) {
		for (let y = 0; y < height; y++) {
			fields[y].value = rowValues[y].join('');
		}
	}

	delay = false;

	statusField.value = `${frame.toString().padStart(4, '0')}: ${index.toString().padStart(6, '0')}/${frames.length.toString().padStart(6, '0')} bytes (${((index / frames.length) * 100).toFixed(2).padStart(5, '0')}%), ${skippedFrames.toString().padStart(4, '0')} skipped (${((skippedFrames / frame) * 100).toFixed(2).padStart(5, '0')}%), ${width}*${height} pixels, ${fps} Hz = ${mspf} ms`;
}

export function setPixel(index: number, active: boolean) {
	const {x, y, i} = indexMap[index];

	if (rows) {
		rowValues[y][x] = active ? char1 : char0;
	} else if (fieldValues[i] !== active) {
		fields[i].hidden = active;
		fieldValues[i] = active;
	}
}
