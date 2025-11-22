import { exportAdd } from "../lib.js";

const main = (): void => {
    console.log("This is route A");
    const result = exportAdd(10, 15);
    console.log(`10 + 15 = ${result}`);
};

main();