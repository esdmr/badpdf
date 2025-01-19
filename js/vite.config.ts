import {defineConfig} from 'vite';
import arraybuffer from 'vite-plugin-arraybuffer';
import {readFile} from 'node:fs/promises';

export default defineConfig(({mode}) => ({
	base: './',
	resolve: {
		conditions: mode === "pdf" ? ['pdf'] : [],
	},
	build: {
		rollupOptions: mode === 'pdf' ? {
			input: 'shared/index.ts',
			output: {
				format: 'iife' as const,
				entryFileNames: 'bad.js',
			},
		} : {
			input: 'html/index.html',
		},
		target: ['es2022'],
		outDir: 'out',
		modulePreload: false,
	},
	plugins: [
		arraybuffer(),
		{
			name: 'gilbert',
			enforce: 'pre' as const,
			resolveId (source, importer, options) {
				if (source === '#gilbert') return '\0gilbert';
			},
			async load (id, options) {
				if (id !== '\0gilbert') return;

				const code = await readFile(new URL('../gilbert/ports/gilbert.js', import.meta.url), 'utf8');

				return `${code.replace('typeof module !== "undefined"', 'false')}; export {gilbert_d2xy as d2xy, gilbert_xy2d as xy2d, gilbert_d2xyz as d2xyz, gilbert_xyz2d as xyz2d};`;
			},
		}
	],
}));
