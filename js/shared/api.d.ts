export const mspf: number;
export const frames: Uint8Array;
export function setInterval(fn: string, ms: number): number;
export function clearInterval(i: number): void;
export function setPlayButtonVisibility(v: boolean): void;
export function startFrame(): void;
export function endFrame(index: number, frame: number, skippedFrames: number): void;
export function setPixel(index: number, active: boolean): void;
