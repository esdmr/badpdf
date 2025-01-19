declare function gilbert_d2xy(idx: number, w: number, h: number): {
    x: number;
    y: number;
};
declare function gilbert_xy2d(x: number, y: number, w: number, h: number): number;
declare function gilbert_d2xyz(idx: number, w: number, h: number, d: number): {
    x: number;
    y: number;
    z: number;
};
declare function gilbert_xyz2d(x: number, y: number, z: number, w: number, h: number, d: number): number;
export { gilbert_d2xy as d2xy, gilbert_xy2d as xy2d, gilbert_d2xyz as d2xyz, gilbert_xyz2d as xyz2d };
