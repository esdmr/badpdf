import {width, height, fps} from '../../frames/options.json';
import frames from '../frames/out/frames.bin?uint8array&base64';
import {d2xy} from '#gilbert';

export const mspf = 1000 / fps;

let statusField = getField('T_stat');
const fields: Field[] = [];
const fieldValues: boolean[] = [];

for (let d = 0; d < width * height; d++) {
	const {x, y} = d2xy(d, width, height);
	fields.push(getField(`P_${x}_${height - y - 1}`));
	fieldValues.push(false);
}

const {rect} = statusField;
statusField.rect = [rect[0] + Math.trunc(Math.random() * 200 - 100), rect[0] + Math.trunc(Math.random() * 200 - 100), rect[0] + Math.trunc(Math.random() * 200 - 100), rect[0] + Math.trunc(Math.random() * 200 - 100)];
statusField.rotation = Math.trunc(Math.random() * 4) * 90;

try {
	app.execMenuItem('FitPage');
} catch {}

export {frames};

export function setInterval(fn: string, ms: number) {
	return app.setInterval(fn, ms);
}

export function clearInterval(i: number) {
	app.clearInterval(i);
}

export function setPlayButtonVisibility(v: boolean) {
	getField('B_play').hidden = !v;
}

export function startFrame() {
	delay = true;
}

export function endFrame(index: number, frame: number, skippedFrames: number) {
	delay = false;

	statusField.value = `${frame.toString().padStart(4, '0')}: ${index.toString().padStart(6, '0')}/${frames.length.toString().padStart(6, '0')} bytes (${((index / frames.length) * 100).toFixed(2).padStart(5, '0')}%), ${skippedFrames.toString().padStart(4, '0')} skipped (${((skippedFrames / frame) * 100).toFixed(2).padStart(5, '0')}%), ${width}*${height} pixels, ${fps} Hz = ${mspf} ms`;
}

export function setPixel(index: number, active: boolean) {
	if (fieldValues[index] !== active) {
		fields[index].hidden = active;
		fieldValues[index] = active;
	}
}
