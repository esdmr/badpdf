export class Color extends PDFObject {
    static _isValidSpace(cColorSpace: any): cColorSpace is "G" | "CMYK" | "RGB" | "T";
    static _isValidColor(colorArray: any): boolean;
    static _getCorrectColor(colorArray: any): any;
    constructor();
    transparent: string[];
    black: (string | number)[];
    white: (string | number)[];
    red: (string | number)[];
    green: (string | number)[];
    blue: (string | number)[];
    cyan: (string | number)[];
    magenta: (string | number)[];
    yellow: (string | number)[];
    dkGray: (string | number)[];
    gray: (string | number)[];
    ltGray: (string | number)[];
    convert(colorArray: any, cColorSpace: any): any;
    equal(colorArray1: any, colorArray2: any): any;
}
import { PDFObject } from "./pdf_object.js";
