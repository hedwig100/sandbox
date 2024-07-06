# Build-your-own-react

```
export NODE_OPTIONS=--openssl-legacy-provider // To avoid error
npm start
```

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

## References
- https://pomb.us/build-your-own-react/
- https://zenn.dev/akatsuki/articles/a2cbd26488fa151b828b