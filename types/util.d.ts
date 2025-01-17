export class Util extends PDFObject {
    constructor(data: any);
    _scandCache: Map<any, any>;
    _months: string[];
    _days: string[];
    MILLISECONDS_IN_DAY: number;
    MILLISECONDS_IN_WEEK: number;
    _externalCall: any;
    printf(...args: any[]): string;
    iconStreamFromIcon(): void;
    printd(cFormat: any, oDate: any): any;
    printx(cFormat: any, cSource: any): string;
    scand(cFormat: any, cDate: any): any;
    _scand(cFormat: any, cDate: any, strict?: boolean): any;
    spansToXML(): void;
    stringFromStream(): void;
    xmlToSpans(): void;
    #private;
}
import { PDFObject } from "./pdf_object.js";
