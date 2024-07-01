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

## References
- https://pomb.us/build-your-own-react/
- https://zenn.dev/akatsuki/articles/a2cbd26488fa151b828b