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
    
    updateDom(dom, {}, fiber.props)
    return dom
}

function updateDom(dom, prevProps, nextProps) {
    const isEvent = key => key.startsWith("on")
    const isProperty = key => key !== "children" && !isEvent(key)
    const isNew = (prev, next) => key => prev[key] !== next[key]
    const isGone = (prev, next) => key => !(key in next)

    // Remove old or changed event listeners
    Object.keys(prevProps)
        .filter(isEvent)
        .filter(key => !(key in nextProps) || isNew(prevProps, nextProps)(key))
        .forEach(name => {
            const eventType = name.toLowerCase().substring(2)
            dom.removeEventListener(eventType, prevProps[name])
        })

    // Remove old properties
    Object.keys(prevProps)
        .filter(isProperty)
        .filter(isGone(prevProps, nextProps))
        .forEach(name => {
            dom[name] = ""
        })
    
    // Update with new properties
    Object.keys(nextProps)
        .filter(isProperty)
        .filter(isNew(prevProps, nextProps))
        .forEach(name => {
            dom[name] = nextProps[name]
        })
    
    // Add event listeners
    Object.keys(nextProps)
        .filter(isEvent)
        .filter(isNew(prevProps, nextProps))
        .forEach(name => {
            const eventType = name.toLowerCase().substring(2)
            dom.addEventListener(eventType, nextProps[name])
        })
}

function commitRoot() {
    deletions.forEach(commitWork)
    commitWork(wipRoot.child)
    currentRoot = wipRoot
    wipRoot = null
}

function commitWork(fiber) {
    if (!fiber) {
        return
    }

    // Find parent with a DOM node (functional components don't have DOM nodes)
    let domParentFiber = fiber.parent
    while (!domParentFiber.dom) {
        domParentFiber = domParentFiber.parent
    }
    const domParent = domParentFiber.dom

    if (fiber.effectTag === "PLACEMENT" && fiber.dom != null) {
        domParent.appendChild(fiber.dom)
    } else if (fiber.effectTag === "UPDATE" && fiber.dom != null){
        updateDom(
            fiber.dom, 
            fiber.alternate.props,
            fiber.props,
        )
    } else if (fiber.effectTag === "DELETION") {
        commitDeletion(fiber, domParent)
    } 

    commitWork(fiber.child)
    commitWork(fiber.sibling)
}

// Find a descendant of a fiber with a DOM node
// , which is a child of a DOM node of `domParent`
function commitDeletion(fiber, domParent) {
    if (fiber.dom) {
        domParent.removeChild(fiber.dom)
    } else {
        commitDeletion(fiber.child, domParent)
    }
}

function render(element, container) {
    wipRoot = {
        dom: container,
        props: {
            children: [element],
        },
        // Reference to the last rendered fiber node
        alternate: currentRoot,
    }
    deletions = []
    nextUnitOfWork = wipRoot
}


let nextUnitOfWork = null

let currentRoot = null

// The root of the DOM tree working in progress
let wipRoot = null

// To keep track of delted old fiber nodes
let deletions = []

// eslint-disable-next-line
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

requestIdleCallback(workLoop)

function performUnitOfWork(fiber) {

    const isFunctionComponent = fiber.type instanceof Function
    if (isFunctionComponent) {
        updateFunctionComponent(fiber)
    } else {
        updateHostComponent(fiber)
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

function updateFunctionComponent(fiber) {
    const children = [fiber.type(fiber.props)]
    reconcileChildren(fiber, children)
}

function updateHostComponent(fiber) {
    // Construct DOM of the fiber node.
    if (!fiber.dom) {
        fiber.dom = createDom(fiber)
    }

    // If the fiber node has children, reconcile fiber node 
    // corresponding to children.
    const elements = fiber.props.children
    reconcileChildren(fiber, elements)
}

function reconcileChildren(wipFiber, elements) {
    let index = 0
    let oldFiber = wipFiber.alternate && wipFiber.alternate.child
    let prevSibling = null
    
    while (index < elements.length || oldFiber != null) {
        const element = elements[index]
        let newFiber = null

        const sameType = oldFiber && element && element.type === oldFiber.type

        if (sameType) {
            // Same type and different props -> Update
            newFiber = {
                type: oldFiber.type,
                props: element.props,
                dom: oldFiber.dom,
                parent: wipFiber,
                alternate: oldFiber,
                effectTag: "UPDATE",
            }
        }
        if (element && !sameType) {
            // Different type and different props -> Replace
            newFiber = {
                type: element.type,
                props: element.props,
                dom: null,
                parent: wipFiber,
                alternate: null,
                effectTag: "PLACEMENT",
            }
        }
        if (oldFiber && !sameType) {
            // No corresponding fiber in the current tree -> Delete
            oldFiber.effectTag = "DELETION"
            deletions.push(oldFiber)
        }

        if (oldFiber) {
            oldFiber = oldFiber.sibling
        }

        if (index === 0) {
            wipFiber.child = newFiber
        } else {
            prevSibling.sibling = newFiber
        }

        prevSibling = newFiber
        index++
    }

}