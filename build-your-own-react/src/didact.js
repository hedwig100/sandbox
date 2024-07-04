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

function createDom(fiber) {
    const dom = 
      fiber.type === "TEXT_ELEMENT" 
      ? document.createTextNode("") 
      : document.createElement(fiber.type)
    
    // Set property
    const isProperty = key => key !== "children"
    Object.keys(fiber.props)
      .filter(isProperty)
      .forEach(name => {
        dom[name] = fiber.props[name]
      })
    
    return dom
}

function commitRoot() {
    commitWork(wipRoot.child)
    wipRoot = null
}

function commitWork(fiber) {
    if (!fiber) {
        return
    }
    const domParent = fiber.parent.dom
    domParent.appendChild(fiber.dom)
    commitWork(fiber.child)
    commitWork(fiber.sibling)
}

function render(element, container) {
    wipRoot = {
        dom: container,
        props: {
            children: [element],
        },
    }
    nextUnitOfWork = wipRoot
}

// For concurrent execution,

let nextUnitOfWork = null

// The root of the DOM tree working in progress
let wipRoot = null

function workLoop(deadline) {
    let shouldYield = false
    while (nextUnitOfWork && !shouldYield) {
        nextUnitOfWork = performUnitOfWork(nextUnitOfWork)
        shouldYield = deadline.timeRemaining() < 1
    }

    if (!nextUnitOfWork && wipRoot) {
        commitRoot()
    }

    requestIdleCallback(workLoop)
}

function performUnitOfWork(fiber) {

    // Construct DOM of the fiber node.
    if (!fiber.dom) {
        fiber.dom = createDom(fiber)
    }

    // If the fiber node has children, create fiber node 
    // corresponding to children.
    const elements = fiber.props.children
    let index = 0
    let prevSibling = null
    
    while (index < elements.length) {
        const element = elements[index]

        const newFiber = {
            type: element.type,
            props: element.props,
            pareent: fiber,
            dom: null,
        }

        if (index === 0) {
            fiber.child = newFiber
        } else {
            prevSibling.sibling = newFiber
        }

        prevSibling = newFiber
        index++
    }

    // Returns nextUnitOfWork
    if (fiber.child) {
        return fiber.child
    }
    let nextFiber = fiber
    while (nextFiber) {
        if (nextFiber.sibling) {
            return nextFiber.sibling
        }
        nextFiber = nextFiber.parent
    }
}