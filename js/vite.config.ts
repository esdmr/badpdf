import {defineConfig} from 'vite';
import arraybuffer from 'vite-plugin-arraybuffer';

export default defineConfig(({mode}) => ({
	base: './',
	resolve: {
		conditions: mode === "pdf" ? ['pdf'] : [],
	},
	build: {
		rollupOptions: mode === 'pdf' ? {
			input: 'index.ts',
			output: {
				format: 'iife',
				entryFileNames: 'bad.js',
			},
		} : {
			input: 'bad.html',
		},
		target: ['es2022'],
		outDir: 'out',
		modulePreload: false,
	},
	plugins: [
		arraybuffer(),
	],
}));
