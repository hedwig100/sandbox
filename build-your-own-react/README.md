# Build-your-own-react

Reference: https://pomb.us/build-your-own-react/

## Run
```
export NODE_OPTIONS=--openssl-legacy-provider // To avoid error
npm start
```

## Architecture

### Data structure
- `Element`
    - React element corresponding to DOM. This class works as an interface to users
    - `type (string)` : HTML DOM type e.g. `h1`, `TEXT_ELEMENT`
    - `props (json)`: properties of DOM element
    - `children (Element[])`: children as a DOM element which is a list of `Element`

- `DOM`
    - a data structure inside html

- `Fiber`
    - a node of virtual DOM which Didact holds
    - `type (string)`: HTML DOM type e.g. `h1`, `TEXT_ELEMENT`
    - `child (Fiber)`: a reference to child fiber
    - `sibling (Fiber)`: a reference to next sibling
    - `parent (Fiber)`: a reference to parent node
    - `effectTag (string)`: specify how to process the corresponding DOM node when updating the DOM tree e.g. `REPLACE`, `UPDATE`, `DELETION`
    - `dom (DOM)`: the corresponding DOM element
    - `alternate (Fiber)`: a reference to the old fiber. This is used for detecting the change of virtual DOM tree so that we can avoid unnecesary re-rendering
    - `props (json)`: properties of DOM element
    - `hooks (Hook[])`: a reference to hooks with this fiber

- `Hook`
    - having the state of the hook, and functions that will be appiled to the state.
    - `state (any)`: a current state of the hook
    - `queue (Function[])`: functions that will be applied to the variables corresponding to the hook

### Global variables
- `wipRoot (Fiber)`: currently processed root of the virtual DOM tree
- `currentRoot (Fiber)`: current root of the virtal DOM tree
- `wipFIber (Fiber)`: currently processed fiber
- `nextUnitOfWork (Fiber)`: a fiber which should be processed next
- `deletions (Fiber[])`: fibers that should be removed in the next commit
- `hookIndex (integer)`: the number of hooks in `wipFiber`.

### Functions
- `createElement(type, props, ...children)`: returns an Element having the `type, props, children`
- `render(element, container)`: set the given element to `wipRoot`, and `nextUnitOfWork`
- `useState(initial)`: this function is used in a component. `wipFiber` 
in this function points to the component. This function creates `Hook`
and add it to `wipFiber.hooks`. Moreover, this function can be called 
more than twice (while re-rendering). In this case, retrieve the old hook from `wipFiber.alternate.hooks[hookIndex]` and update the state.
The `setState` function which `useState` returns adds the argument (function) to `hook.queeu` and set `currentRoot` to `wipRoot` and `nextUnitOfWork` (invokes re-rendering).
- `workLoop`
    - this function runs always when CPU is idle. When there is a `nextUnifOfWork`, execute `performUnitOfWork(nextUnitOfWork)`. 
    - When there is no `nextUnitOfWork` and there is `wipRoot`, execute `commitRoot()`.
    - `performUnitOfWork()` updates the fiber by comparing the current fiber and old fiber. This update varies for `FunctionComponent` (without DOM node) and normal components (having DOM node). 
    - `commitRoot()` commits the `wipRoot`. Until this function is called, the update is only executed on `Fiber` (in other words, the update is temporarily on virtual DOM tree). This prevents users see the DOM node under change.

## MEMO

**Step I. The `createElement` Function**
- propsを埋めたDOMを作るためのjson(これをReact Elementと呼ぶことにする)を返す. 
- ただのテキストの場合は `type` が特殊な `TEXT_ELEMENT` であるようなReact Elementを返す. 

**Step II. The `render` Function**
- `document` はトップレベルのDOMであり, グローバル変数?
- `document` に `createElement` でエレメントを作ることでDOMをReact Elementから作成する. 
- `props` をすべて指定して, `children` を再帰的にレンダリングする.

**Step III: Concurrent Mode**
- 今の実装ではDOMツリーを構築し終わるまで, DOMツリーの構築がメインスレッドをブロックし続ける. これによってより重要度の高いユーザのインプットなどが行えなくなるかもしれない. 
- そこでDOMツリーの構築をいくつかの部分に分けて、その各部分が終わった後にブラウザがほかにやるべきことがあればそれができるようにする. 
- そこで `requestIdelCallback` を使う. これは `setTimeout` と同様に使うが, `setTimeout` と異なる点はある時間があった後にcallbackが実行されるのではなく, メインスレッドがアイドル状態にあるときにcallbackが実行されることである.

**Step IV: Fibers**
- StepIIIで小さな単位にDOMツリーの構築を分解すると書いたが, それはfiber treeというものを使って行われる. 
- fiber treeは木構造のデータ構造で
    - 割り当てられた仕事を木のノード単位に分割し, 
    - 次にやるべき仕事を決める
　ためのデータ構造である. 調べたところこれは一般的な概念ではなく, React 特有の概念っぽいのでそれほど抽象的に理解する必要はないかも.
- treeを明示的に持っていないが, 走査する部分が `performUnitOfWork` に実装されている. 
- `render` はルートのノードを設定している. 

**Step V: Render and Commit Phases**
- Step IVまでの実装ではDOMツリーを毎回更新しているため, ユーザは完成途中のDOMを見ることになっていた. しかしそれは望ましくなくて、完成した最後のDOMツリーだけ見えるようにしたい.
- そこでDOMノードの構築とDOMツリーの構築は別々に行う. `performUnitOfWork` はDOMノードの構築のみ行う. DOMツリーの構築はすべてのDOMノードを構築し終わった後, すなわち `nextUnitOfWork` がnullになった時に行う. 

**Step VI: Reconciliation**
- Step VまででDOMツリーを構築することはできたが, これをupdateしたり, 消したりすることをこのステップでできるようにする.
- そのために各DOMノードに、直前に構築したDOMノードへの参照を持っておくようにする. これが新しく作ろうとしているDOMノードと一致する場合はレンダリングせず、一致しない場合のみ再レンダリングが走るようにする. 

Tips: javascript で `&&` はすべての値が真値であれば, 最後のオペランドの値が返される. そうでない場合, 最も最初の偽値のオペランドを返す.

**Step VII: Function Components**
- Function componentsを追加する. Function componentsは以下のような使い方ができるもの. 
```js
function App(props) {
    return <h1>Hi {props.name}</h1>
}
```
- Function componentはDOMノードを持たないfiberとして機能する. つまり, 構造を示しているだけで実際に描画される, あるDOMノードとの対応があるわけではない. 
- よってFunction componentかそうでないかによって処理を分ける必要がある. 
- またDOMノードを持っていないfiberがあるため, 子や親に行く処理があるときにDOMノードがある場合はスキップするなどの処理を行う必要がある. 

**Step VIII: Hooks**
- Hooksを追加する. 
- `useState(initial)` をここでは追加する. `useState(initial)` はまず昔のfiberに対応するhookがあるときはそのstateをコピーする. そうでない場合は新規にhookが作成されているので `initial` で初期化する. 
- また更新用の関数はhookがもつqueueに更新用の関数への引数をpushしておき, `wipRoot` を設定しておくことで行う. 

## References
- https://pomb.us/build-your-own-react/
- https://zenn.dev/akatsuki/articles/a2cbd26488fa151b828b