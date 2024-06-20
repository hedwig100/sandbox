## Build your own databse in Go
[This page](https://build-your-own.org/database/) is referenced.

### 実装のアイデア

### 4. B+Tree Node and Insertion
- `BNode` をバイト列として実装することでディスク上への読み書きが後で簡単にできるようにしている. 
- `BNode` はoffsetを持つことで可変な長さを持ちうるkey-valueのペアを持ち, かつ二分探索で検索できるようにしている. 
- バイトフォーマットを初めから考慮してLittleEndianなどを用いている.
- `nodeReplaceKidN` の関数名がかなり謎, Nこのkidをreplaceしてoldからnewに変換するみたいな話に見える. 
- `nodeSplit2` というBNodeを一つ受け取って, それをleft,rightという二つのノードに分けて, 右側がPAGE_MAXを超えないようにする関数を作っておいて、それを利用して三つに分けられる`nodeSplit3`も実装する. 
- `treeInsert` のなかで　`leftUpdate` という関数があったが, これは実装されていない, まあ特定idxのものを(key, val)にするだけなので簡単だが。
- `nodeInsert` で `new` 自身はこの関数の呼び出し後にPAGE_MAXのサイズを超えている可能性はある. これが超えている場合はそれは呼び出し元の責任でsplitする. それは説明のところに書いてある通り. 
