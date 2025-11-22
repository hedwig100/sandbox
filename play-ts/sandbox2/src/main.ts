import { exportAdd } from "@/lib.js";
import dotenv from "dotenv";

dotenv.config();

const main = (): void => {
    console.log("This is sandbox2 main.ts");
    const result = exportAdd(5, 7);
    console.log(`5 + 7 = ${result}`);
    console.log(`Your secret from .env is: ${process.env.YOUR_SECRET}`);
};

main();