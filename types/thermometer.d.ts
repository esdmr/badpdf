export class Thermometer extends PDFObject {
    constructor(data: any);
    _cancelled: boolean;
    _duration: number;
    _text: string;
    _value: number;
    set cancelled(_: boolean);
    get cancelled(): boolean;
    set duration(val: number);
    get duration(): number;
    set text(val: string);
    get text(): string;
    set value(val: number);
    get value(): number;
    begin(): void;
    end(): void;
}
import { PDFObject } from "./pdf_object.js";
