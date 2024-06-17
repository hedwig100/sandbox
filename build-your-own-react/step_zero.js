
// Original React code
// const element = (
// <div id="foo">
//     <a>bar</a>
//     <b />
// </div>
// )
// const container = document.getElementById("root")
// ReactDOM.render(element, container)

const element = {
    type: "h1",
    props: {
        title: "foo",
        children: "Hello",
    },
}

const container = document.getElementById("root")

const node = document.createElement(element.type)
node["title"] = element.props.title
const text = document.createTextNode("")
text["nodeValue"] = element.props.children
node.appendChild(text)
container.appendChild(node)