export class Event {
    constructor(data: any);
    change: any;
    changeEx: any;
    commitKey: any;
    fieldFull: any;
    keyDown: any;
    modifier: any;
    name: any;
    rc: boolean;
    richChange: any;
    richChangeEx: any;
    richValue: any;
    selEnd: any;
    selStart: any;
    shift: any;
    source: any;
    target: any;
    targetName: string;
    type: string;
    value: any;
    willCommit: any;
}
export class EventDispatcher {
    constructor(document: any, calculationOrder: any, objects: any, externalCall: any);
    _document: any;
    _calculationOrder: any;
    _objects: any;
    _externalCall: any;
    _isCalculating: boolean;
    mergeChange(event: any): string | any[];
    userActivation(): void;
    dispatch(baseEvent: any): void;
    formatAll(): void;
    runValidation(source: any, event: any): void;
    runActions(source: any, target: any, event: any, eventName: any): any;
    calculateNow(): void;
    runCalculate(source: any, event: any): void;
}
