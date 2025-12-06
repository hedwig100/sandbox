var s = "hello";
var n = 3;
var b = true;
var v = undefined;
var nums = [1, 2, 3];
var strs = ["a", "b", "c"];
var tup = ["age", 30];
var user = { name: "Alice", age: 25 };
var a = { name: "Bob" };
var fn = function (args) {
    return args.name;
};
console.log(fn(a));
var getUser = function (user) {
    return "Name: ".concat(user.name, ", Age: ").concat(user.age);
};
var user1 = { name: "Charlie", age: 28 };
console.log(getUser(user1));
