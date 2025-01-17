export class PrintParams {
    constructor(data: any);
    binaryOk: boolean;
    bitmapDPI: number;
    booklet: {
        binding: number;
        duplexMode: number;
        subsetFrom: number;
        subsetTo: number;
    };
    colorOverride: number;
    colorProfile: string;
    constants: Readonly<{
        bookletBindings: Readonly<{
            Left: 0;
            Right: 1;
            LeftTall: 2;
            RightTall: 3;
        }>;
        bookletDuplexMode: Readonly<{
            BothSides: 0;
            FrontSideOnly: 1;
            BasicSideOnly: 2;
        }>;
        colorOverrides: Readonly<{
            auto: 0;
            gray: 1;
            mono: 2;
        }>;
        fontPolicies: Readonly<{
            everyPage: 0;
            jobStart: 1;
            pageRange: 2;
        }>;
        handling: Readonly<{
            none: 0;
            fit: 1;
            shrink: 2;
            tileAll: 3;
            tileLarge: 4;
            nUp: 5;
            booklet: 6;
        }>;
        interactionLevel: Readonly<{
            automatic: 0;
            full: 1;
            silent: 2;
        }>;
        nUpPageOrders: Readonly<{
            Horizontal: 0;
            HorizontalReversed: 1;
            Vertical: 2;
        }>;
        printContents: Readonly<{
            doc: 0;
            docAndComments: 1;
            formFieldsOnly: 2;
        }>;
        flagValues: Readonly<{
            applyOverPrint: 1;
            applySoftProofSettings: number;
            applyWorkingColorSpaces: number;
            emitHalftones: number;
            emitPostScriptXObjects: number;
            emitFormsAsPSForms: number;
            maxJP2KRes: number;
            setPageSize: number;
            suppressBG: number;
            suppressCenter: number;
            suppressCJKFontSubst: number;
            suppressCropClip: number;
            suppressRotate: number;
            suppressTransfer: number;
            suppressUCR: number;
            useTrapAnnots: number;
            usePrintersMarks: number;
        }>;
        rasterFlagValues: Readonly<{
            textToOutline: 1;
            strokesToOutline: number;
            allowComplexClip: number;
            preserveOverprint: number;
        }>;
        subsets: Readonly<{
            all: 0;
            even: 1;
            odd: 2;
        }>;
        tileMarks: Readonly<{
            none: 0;
            west: 1;
            east: 2;
        }>;
        usages: Readonly<{
            auto: 0;
            use: 1;
            noUse: 2;
        }>;
    }>;
    downloadFarEastFonts: boolean;
    fileName: string;
    firstPage: number;
    flags: number;
    fontPolicy: number;
    gradientDPI: number;
    interactive: number;
    lastPage: any;
    npUpAutoRotate: boolean;
    npUpNumPagesH: number;
    npUpNumPagesV: number;
    npUpPageBorder: boolean;
    npUpPageOrder: number;
    pageHandling: number;
    pageSubset: number;
    printAsImage: boolean;
    printContent: number;
    printerName: string;
    psLevel: number;
    rasterFlags: number;
    reversePages: boolean;
    tileLabel: boolean;
    tileMark: number;
    tileOverlap: number;
    tileScale: number;
    transparencyLevel: number;
    usePrinterCRD: number;
    useT1Conversion: number;
}
