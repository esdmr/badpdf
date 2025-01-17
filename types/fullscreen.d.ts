export class FullScreen extends PDFObject {
    constructor(data: any);
    _backgroundColor: any[];
    _clickAdvances: boolean;
    _cursor: 1;
    _defaultTransition: string;
    _escapeExits: boolean;
    _isFullScreen: boolean;
    _loop: boolean;
    _timeDelay: number;
    _usePageTiming: boolean;
    _useTimer: boolean;
    set backgroundColor(_: any[]);
    get backgroundColor(): any[];
    set clickAdvances(_: boolean);
    get clickAdvances(): boolean;
    set cursor(_: 1);
    get cursor(): 1;
    set defaultTransition(_: string);
    get defaultTransition(): string;
    set escapeExits(_: boolean);
    get escapeExits(): boolean;
    set isFullScreen(_: boolean);
    get isFullScreen(): boolean;
    set loop(_: boolean);
    get loop(): boolean;
    set timeDelay(_: number);
    get timeDelay(): number;
    set transitions(_: string[]);
    get transitions(): string[];
    set usePageTiming(_: boolean);
    get usePageTiming(): boolean;
    set useTimer(_: boolean);
    get useTimer(): boolean;
}
import { PDFObject } from "./pdf_object.js";