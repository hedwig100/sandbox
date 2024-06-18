import { Didact } from "./didact.js";

/**@jsx Didact.createElement */
const element = (
    <div id="foo">
        <b>bar</b>
        <c />
    </div>
)

const container = document.getElementById("root")
Didact.render(element, container)