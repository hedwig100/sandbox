export const Didact = {
    createElement,
    render,
}

function createElement(type, props, ...children) {
    return {
        type,
        props: {
            ...props,
            children: children.map(
                child => typeof child === "object" 
                ? child : 
                createTextElement(child)
            )
        }
    }
}

function createTextElement(text) {
    return {
        type: "TEXT_ELEMENT",
        props: {
            nodeValue: text,
            children: [],
        }
    }
}

function render(element, container) {
    const dom = 
      element.type === "TEXT_ELEMENT" 
      ? document.createTextNode("") 
      : document.createElement(element.type)
    
    // Set property
    const isProperty = key => key !== "children"
    Object.keys(element.props)
      .filter(isProperty)
      .forEach(name => {
        dom[name] = element.props[name]
      })

    element.props.children.forEach(child => 
        render(child, dom)
    )

    container.appendChild(dom)
}

// For concurrent execution,

let nextUnitOfWork = null

function workLoop(deadline) {
    let shouldYield = false
    while (nextUnitOfWork && !shouldYield) {
        nextUnitOfWork = performUnitOfWork(nextUnitOfWork)
        shouldYield = deadline.timeRemaining() < 1
    }
    requestIdleCallback(workLoop)
}

function performUnitOfWork(nextUnitOfWork) {
    // TODO
}