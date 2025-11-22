const s: string = "hello";
const n: number = 3;
const b: boolean = true;
const v: void = undefined;

const nums: number[] = [1, 2, 3];
const strs: Array<string> = ["a", "b", "c"];

const tup: [string, number] = ["age", 30];

const user: { name: string; age: number } = { name: "Alice", age: 25 };

type A = {name: string};
const a: A = {name: "Bob"};
const fn = (args: A): string => {
  return args.name;
};
console.log(fn(a));

type User = {
    name: string;
    age: number;
};

interface IUser {
    name: string;
    age: number;
}

const getUser = (user: IUser): string => {
    return `Name: ${user.name}, Age: ${user.age}`;
};

const user1: IUser = { name: "Charlie", age: 28 };
console.log(getUser(user1));