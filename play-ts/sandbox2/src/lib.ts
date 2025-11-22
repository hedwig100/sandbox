
const add = (a: number, b: number): number => {
    return a + b;
};

const subtract = (a: number, b: any): number => { // anyはこの設定だと防げない
    return a - b;
}

const exportAdd = add;
const exportSubtract = subtract;

export { exportAdd, exportSubtract };