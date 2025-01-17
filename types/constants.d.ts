export const Border: Readonly<{
    s: "solid";
    d: "dashed";
    b: "beveled";
    i: "inset";
    u: "underline";
}>;
export const Cursor: Readonly<{
    visible: 0;
    hidden: 1;
    delay: 2;
}>;
export const Display: Readonly<{
    visible: 0;
    hidden: 1;
    noPrint: 2;
    noView: 3;
}>;
export const Font: Readonly<{
    Times: "Times-Roman";
    TimesB: "Times-Bold";
    TimesI: "Times-Italic";
    TimesBI: "Times-BoldItalic";
    Helv: "Helvetica";
    HelvB: "Helvetica-Bold";
    HelvI: "Helvetica-Oblique";
    HelvBI: "Helvetica-BoldOblique";
    Cour: "Courier";
    CourB: "Courier-Bold";
    CourI: "Courier-Oblique";
    CourBI: "Courier-BoldOblique";
    Symbol: "Symbol";
    ZapfD: "ZapfDingbats";
    KaGo: "HeiseiKakuGo-W5-UniJIS-UCS2-H";
    KaMi: "HeiseiMin-W3-UniJIS-UCS2-H";
}>;
export const GlobalConstants: Readonly<{
    IDS_GREATER_THAN: "Invalid value: must be greater than or equal to % s.";
    IDS_GT_AND_LT: string;
    IDS_LESS_THAN: "Invalid value: must be less than or equal to % s.";
    IDS_INVALID_MONTH: "** Invalid **";
    IDS_INVALID_DATE: "Invalid date / time: please ensure that the date / time exists. Field";
    IDS_INVALID_DATE2: " should match format ";
    IDS_INVALID_VALUE: "The value entered does not match the format of the field";
    IDS_AM: "am";
    IDS_PM: "pm";
    IDS_MONTH_INFO: string;
    IDS_STARTUP_CONSOLE_MSG: "** ^ _ ^ **";
    RE_NUMBER_ENTRY_DOT_SEP: string[];
    RE_NUMBER_COMMIT_DOT_SEP: string[];
    RE_NUMBER_ENTRY_COMMA_SEP: string[];
    RE_NUMBER_COMMIT_COMMA_SEP: string[];
    RE_ZIP_ENTRY: string[];
    RE_ZIP_COMMIT: string[];
    RE_ZIP4_ENTRY: string[];
    RE_ZIP4_COMMIT: string[];
    RE_PHONE_ENTRY: string[];
    RE_PHONE_COMMIT: string[];
    RE_SSN_ENTRY: string[];
    RE_SSN_COMMIT: string[];
}>;
export const Highlight: Readonly<{
    n: "none";
    i: "invert";
    p: "push";
    o: "outline";
}>;
export const Position: Readonly<{
    textOnly: 0;
    iconOnly: 1;
    iconTextV: 2;
    textIconV: 3;
    iconTextH: 4;
    textIconH: 5;
    overlay: 6;
}>;
export const ScaleHow: Readonly<{
    proportional: 0;
    anamorphic: 1;
}>;
export const ScaleWhen: Readonly<{
    always: 0;
    never: 1;
    tooBig: 2;
    tooSmall: 3;
}>;
export const Style: Readonly<{
    ch: "check";
    cr: "cross";
    di: "diamond";
    ci: "circle";
    st: "star";
    sq: "square";
}>;
export const Trans: Readonly<{
    blindsH: "BlindsHorizontal";
    blindsV: "BlindsVertical";
    boxI: "BoxIn";
    boxO: "BoxOut";
    dissolve: "Dissolve";
    glitterD: "GlitterDown";
    glitterR: "GlitterRight";
    glitterRD: "GlitterRightDown";
    random: "Random";
    replace: "Replace";
    splitHI: "SplitHorizontalIn";
    splitHO: "SplitHorizontalOut";
    splitVI: "SplitVerticalIn";
    splitVO: "SplitVerticalOut";
    wipeD: "WipeDown";
    wipeL: "WipeLeft";
    wipeR: "WipeRight";
    wipeU: "WipeUp";
}>;
export const ZoomType: Readonly<{
    none: "NoVary";
    fitP: "FitPage";
    fitW: "FitWidth";
    fitH: "FitHeight";
    fitV: "FitVisibleWidth";
    pref: "Preferred";
    refW: "ReflowWidth";
}>;
