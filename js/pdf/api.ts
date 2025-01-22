import {gilbert, rows, char0BWFont, char1BWFont, char0NoFont, char1NoFont} from '../../frames/options.json';
import {width, height, fps} from '../../frames/ffmpeg.json';
import frames from '../../frames/out/frames.bin?uint8array&base64';
import {d2xy} from '#gilbert';

export const mspf = 1000 / fps;

const statusField = getField('T_stat');
const fields: Field[][] = [];
const fieldValues: string[][] = [];
const fontFallback = app.viewerType === 'PDF.js';
const char0 = fontFallback ? char0NoFont : char0BWFont;
const char1 = fontFallback ? char1NoFont : char1BWFont;

const indexMap = Array.from(
	{length: width * height},
	(_, i) => gilbert ? d2xy(i, width, height) : {
		x: i % width,
		y: Math.trunc(i / width),
	},
);

if (rows) {
	for (let y = 0; y < height; y++) {
		fields.push([getField(`R_${height - y - 1}`)]);
		fieldValues.push(Array.from({length: width}, () => char0));
	}
} else {
	for (let y = 0; y < height; y++) {
		const row: Field[] = [];
		fields.push(row);
		fieldValues.push(Array.from({length: width}, () => char0));

		for (let x = 0; x < width; x++) {
			row.push(getField(`P_${x}_${height - y - 1}`));
		}
	}
}

try {
	app.execMenuItem('FitPage');
} catch {}

statusField.value = `Ready. ${app.viewerType} ${app.viewerVariation} v${app.viewerVersion}, AcroForm v${app.formsVersion}.`;

if (rows) {
	statusField.value += ` Embedded font is ${fontFallback ? 'not ' : ''}supported, probably.`;
}

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
			fields[y][0].value = fieldValues[y].join('');
		}
	}

	delay = false;

	statusField.value = `${frame.toString().padStart(4, '0')}: ${index.toString().padStart(6, '0')}/${frames.length.toString().padStart(6, '0')} bytes (${((index / frames.length) * 100).toFixed(2).padStart(5, '0')}%), ${skippedFrames.toString().padStart(4, '0')} skipped (${((skippedFrames / frame) * 100).toFixed(2).padStart(5, '0')}%), ${width}*${height} pixels, ${fps} Hz = ${mspf} ms`;
}

export function setPixel(index: number, active: boolean) {
	const {x, y} = indexMap[index];
	const char = active ? char1 : char0;

	if (!rows && fieldValues[y][x] !== char) {
		fields[y][x].hidden = active;
	}

	fieldValues[y][x] = char;
}
