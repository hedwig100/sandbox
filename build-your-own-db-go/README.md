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

### 6. Append-Only KV Store
この章で実装するKeyValueStoreはBtreeを使って実装する。この章ではdurabilityとatomicityに焦点を当てる。これはB+treeの`get, new, del`の三つのcallbackを通して理解される。

[fsyncについて](https://yasukata.hatenablog.com/entry/2020/06/24/072609)
- atomicityはroot nodeをatomicityに更新することで実現される.
- 新しいルートノードが先にディスクに書き込まれ、そのあとに更新後のノードがディスクに書き込まれた場合(これはキャッシュなどの問題によりあり得る), durabilityが保たれないので, 先に更新後のノードをfsyncし、そのあとにルートノードをfsyncする必要がある.
- copy-on-writeな方法をこの本ではとっているが、それと対比的な手法としてdouble-writeな方法もある. double-writeな方法はlogと同じような方法である. とりあえずupdateするのに必要な情報だけlogに書いておき、そのあとに実際のデータをインプレースに更新する. 

**Database on a file**
- ファイル上にpageを配置する. 
[mmapについて](https://ja.wikipedia.org/wiki/Mmap)
[mmapについて2](https://mkguytone.github.io/allocator-navigatable/ch73.html)
- mmapというシステムコールを使って, インメモリなバッファのファイルを読み書きする. mmapはファイルの一部を連続して仮想アドレス空間にマッピングする関数である. すなわちメモリ空間とファイルの対応付けを作る関数だと思えばよい. 
- mmapで確保したファイル(仮想アドレスを持つ)をpageごとに切り分けて使う. 

- 構造体 `mmap` はディスク上のデータを持っている. 
- `pageRead` の引数 `ptr` はこのDB内でのページのインデックスを意味すると思えばよい。0なら0番目のページを指していて、4なら4番目のページを指す.
- `extendMmap` は `chunk` (ページ)を増やしていくための関数. 

- 構造体 `page` はメモリ上のデータを持っている. 
- `pageAppend` ではメモリ上にとりあえず追加しているだけである. 
- `writePages` で `page.temp` のデータをディスクに書き込んでいる.

- meta pageはメタデータを持っている. 

**Error handling**
- fsyncやwriteでエラーが起こったらそのあとはどのような処理をするべきなのか?たとえば, write でエラーが起きて, Readが来たらどのような値を返すべきか?
- `fsync` でのエラーの後にどのような処理を行うかという問題があるが, 我々はcopy-on-writeな書き込みをしているのでただ単に前のデータに戻せばよい. 
- もう一つの方法として失敗したら二回書き込むという方法もある. 
- NOTE: クラッシュした後の復帰処理って書く必要があるのではないか?

### 7. Free List: Recycle & Reuse
- Chapter6の実装では一回使用して、消去したページが再利用されないようになっていたので, これを再利用するような実装をする. それはfree listというデータ構造で実現される. (NOTE: これ今まで知っていた用語でいうとbuffer poolということか?)
- アイデアは使用されていないページへのポインタを持つことである。
- free listはpageのlinked listとして実装される. 削除されたpageへのポインタがfree listには格納される. 
- free listのノードはインプレースに更新されるが, ページ内でnext以外は上書きされないので, nextが正しい限り, このアルゴリズムは正しく動く(NOTE: どういう意味?). 
- `tailSeq`, `headSeq` を動かすことでfree listへの使用されていないページへのポインタのappnedとdeleteを行う. これが `PopHead` と `PushTail`.

- `pageAlloc` はfree listに再利用可能なページがあればそれを利用する. もしなければファイルにページを追加してそれを返す. 
- `pageWrite` はページに書き込むのではなく, 書き込み可能なコピーを返している. 
- `pageRead` は前のチャプターのところから少し進化していて, `db.page.updates`というインメモリなバッファにあればそれを返し, そうでない場合は `db.pageReadFile` を返す. 