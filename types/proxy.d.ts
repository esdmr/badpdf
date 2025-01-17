export class ProxyHandler {
    nosend: Set<string>;
    get(obj: any, prop: any): any;
    set(obj: any, prop: any, value: any): boolean;
    has(obj: any, prop: any): boolean;
    getPrototypeOf(obj: any): any;
    setPrototypeOf(obj: any, proto: any): boolean;
    isExtensible(obj: any): boolean;
    preventExtensions(obj: any): boolean;
    getOwnPropertyDescriptor(obj: any, prop: any): {
        configurable: boolean;
        enumerable: boolean;
        value: any;
    };
    defineProperty(obj: any, key: any, descriptor: any): boolean;
    deleteProperty(obj: any, prop: any): void;
    ownKeys(obj: any): (string | symbol)[];
}
