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

## References
- https://pomb.us/build-your-own-react/
- https://zenn.dev/akatsuki/articles/a2cbd26488fa151b828b