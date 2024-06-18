import Didact from "didact";

const element = Didact.createElement(
    "div",
    {id: "foo"},
    Didact.createElement("a", null, "bar"),
    Didact.createElement("b")
)