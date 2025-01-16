/**
 * @see https://stackoverflow.com/a/62364519
 * @see https://github.com/ading2210/doompdf/blob/b38e0d7d346d1cc1101eb35d3d66ff32eee1efeb/file_template.js
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
			.map((x) => parseInt(x, 2));

		result.push(...bytes.slice(0, 3 - +(str[4*i+2]=='=') - +(str[4*i+3]=='=')));
	}

	return new Uint8Array(result);
}

const frames = b64_to_uint8array('###FRAME_DATA###');
let index = 0;
let frame = 0;

const fps = Number('###FPS###');
const statField = getField('T_stat');
const fields = [];
const fieldValues = [];
let interval;

const width = Number('###GRID_WIDTH###');
const height = Number('###GRID_HEIGHT###');

for (let y = height - 1; y >= 0; y--) {
	for (let x = 0; x < width; x++) {
		fields.push(getField(`P_${x}_${y}`));
		fieldValues.push(false);
	}
}

app.execMenuItem('FitPage');
globalThis.onFrame = onFrame;
globalThis.onInit = onInit;

function setPixel(index, active) {
	if (fieldValues[index] !== active) {
		fields[index].hidden = active;
		fieldValues[index] = active;
	}
}

function onFrame() {
	if (index >= frames.length) {
		this.getField('B_play').hidden = false;
		app.clearInterval(interval);
		return;
	}

	const end = frames[index++] + frames[index++] * 256 + index;

	let active = false;
	let pixelIndex = 0;

	for (; index < end; index++) {
		for (let i = frames[index]; i > 0; i--) {
			setPixel(pixelIndex++, active);
		}

		active = !active;
	}

	frame++;
	statField.value = `${frame.toString().padStart(4, '0')}: ${index}/${frames.length} (${(index / frames.length * 100).toFixed(2)})%`;
}

function onInit() {
	this.getField('B_play').hidden = true;
	index = 0;
	frame = 0;
	interval = app.setInterval('onFrame();', 1000 / fps);
}
