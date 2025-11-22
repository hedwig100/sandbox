import { exportAdd } from "./lib.js";

const main = (): void => {
    console.log("This is sandbox2 main.ts");
    const result = exportAdd(5, 7);
    console.log(`5 + 7 = ${result}`);
};

main();