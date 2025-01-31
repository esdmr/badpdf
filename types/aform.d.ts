export class AForm {
    constructor(document: any, app: any, util: any, color: any);
    _document: any;
    _app: any;
    _util: any;
    _color: any;
    _dateFormats: string[];
    _timeFormats: string[];
    _emailRegex: RegExp;
    _mkTargetName(event: any): string;
    _parseDate(cFormat: any, cDate: any, strict?: boolean): any;
    AFMergeChange(event?: Event): any;
    AFParseDateEx(cString: any, cOrder: any): any;
    AFExtractNums(str: any): any;
    AFMakeNumber(str: any): number;
    AFMakeArrayFromList(string: any): any;
    AFNumber_Format(nDec: any, sepStyle: any, negStyle: any, currStyle: any, strCurrency: any, bCurrencyPrepend: any): void;
    AFNumber_Keystroke(nDec: any, sepStyle: any, negStyle: any, currStyle: any, strCurrency: any, bCurrencyPrepend: any): void;
    AFPercent_Format(nDec: any, sepStyle: any, percentPrepend?: boolean): void;
    AFPercent_Keystroke(nDec: any, sepStyle: any): void;
    AFDate_FormatEx(cFormat: any): void;
    AFDate_Format(pdf: any): void;
    AFDate_KeystrokeEx(cFormat: any): void;
    AFDate_Keystroke(pdf: any): void;
    AFRange_Validate(bGreaterThan: any, nGreaterThan: any, bLessThan: any, nLessThan: any): void;
    AFSimple(cFunction: any, nValue1: any, nValue2: any): number;
    AFSimple_Calculate(cFunction: any, cFields: any): void;
    AFSpecial_Format(psf: any): void;
    AFSpecial_KeystrokeEx(cMask: any): void;
    AFSpecial_Keystroke(psf: any): void;
    AFTime_FormatEx(cFormat: any): void;
    AFTime_Format(pdf: any): void;
    AFTime_KeystrokeEx(cFormat: any): void;
    AFTime_Keystroke(pdf: any): void;
    eMailValidate(str: any): boolean;
    AFExactMatch(rePatterns: any, str: any): any;
    #private;
}
