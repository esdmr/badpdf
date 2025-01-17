declare type Doc = import('./types/doc.js').Doc;
declare type Field = import('./types/field.js').Field;
declare type App = import('./types/app.js').App;

declare var app: App;
declare var delay: boolean;
declare function getField(cName: string): Field;
