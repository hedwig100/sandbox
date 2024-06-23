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
- これまでの関数の実装がすべてcopy-on-writeになっているのも重要な点だと思う。引数をupdateするのではなくてnewにcopyしてかつupdateしている。
- `BTree` 構造体がpageをディスク上に割り当てる関数を持つことで、これを入れ替えることでテストが容易にできるようにしている。

### 5. B+tree Deletion and Testing
- `Insert` の中で `treeInsert` したあとに `nodeSplit3` しているのは上の考察(呼び出し元が責任をもってsplitする)というものに合致している。
- そのあとの処理で高さが1高くなるようにできている。
- Delete処理のためにはInsertの場合はsplitを必要としたのと対照的にMerge処理を必要とする. 
- Mergeは持っているキーの数が0になった時ではなく、バイト数がある閾値より小さくなったら行うようにする。
- 基本的には再帰的に処理する、そのためleafの場合とinternalなノードの場合で処理を変更している。
- 実装がない `treeDelete` では `new` を作ってleafならleafDelete、そうでない場合は `nodeDelete` を行うというような処理になると思われる。
- `nodeDelete` ではupdateしてもし子がupdateされていたら自分もcopy-on-write方式でupdateするようにしている. 
- これもinsertの場合と同じだが `treeDelete` はcallerの責任でmergeしている. 
- page managementはすべてBTreeのcallbackを通じて行っているのでこれを利用するとテストが可能である。