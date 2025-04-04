# Flex Bison

## メモ

### Flexのインストール

https://github.com/westes/flex/releases/tag/v2.6.4
http://honana.com/library/flex

```sh
wget -P /usr/local/src https://github.com/westes/flex/releases/download/v2.6.4/flex-2.6.4.tar.gz
cd /usr/lolca/src
tar xzf flex-2.6.4.tar.gz
cd flex-2.6.4
./configure --prefix=/usr/local/bin
make
make install
```
で`flex --version`が動けばok. バージョンは適宜変更すること.

### Flexコンパイル

```sh
flex -o lex.yy.c lex.l
gcc -o lex.o lex.yy.c
```
だとコンパイルできない。

lex.yの先頭に`%option noyywrap`するとエラーが消えて
```sh
flex lex.l
gcc -o lex.o lex.yy.c
./lex.o
```
で動いた。

- lex.lをfirst-lexディレクトリに移動。
- pascalディレクトリにpascalライクな言語の字句解析器のみ実装、Makeも使ってみた。

### Bisonインストール
```sh
sudo wget -P /usr/local/src https://ftp.gnu.org/gnu/bison/bison-3.8.2.tar.gz
cd /usr/local/src
sudo tar xzf bison-3.8.2.tar.gz
sudo ./configure --prefix=/usr/local/bin
sudo make
sudo make install
bison --version
```

Bisonとflexをつかってbasic-arithをつくる。
無理そうなのでまずはfirst-bisonで適当に触ってみる。

```
cd first-bison
bison rpcalc.y
gcc -o rpcalc.o rpcalc.tab.c -lm
```

###　Infix

- 演算子の優先順序は宣言の下の方にある方が優先。
- %left, %rightは演算が右結合か、左結合かということを意味する。つまり a + b + c が (a + b) + cなのか a + (b + c) なのかということ。
- %prec NEG でNEGと優先順序が同じであることを示す。

- `error` は予約されていて、エラーになったら発火する。

### Multi function calculator

- `api.value.type union` で union 型を YYSTYPE として使える(Semantic valueを持つ)。
- `%nterm` は non-terminal symbol を union の中の一つとして使える。

### Bison C++

- bisonをC++から使えるようにする。
```
cd cpp-bison
bison parser.yy -o parser.cc
g++ -std=c++14 parser.cc -o parser.o
```

### Bison and flex with C++

[Complex example](https://www.gnu.org/software/bison/manual/bison.html#A-Complete-C_002b_002b-Example)を完全にパクッて、
そこから望みの方向へ少しずつ、変更していくことにした。bisonをインストールしたディレクトリの`examples/c++/calc++`にある。

やりたいこと
- 外から使うクラスにはネームスペースをつける。
- できるだけわからないところをつぶす。
- C, C++の実装はできるだけlexer.l, parser.yyの外で行えるようにする。
- std::istreamを入力として、構文木を返却できるようにする。

## SQL example
C++で書くのはあきらめたのですべてをC言語で書く。

bison
- %tokenのはflexで定義された何か? それともbison側で定義している？
- 簡単に書いた
- 手順としては
    1. Bison側で%union, %tokenなどを使ってSemanticValueを持つ型を生成する。
    2. Lex側でどんなトークンを生成するかを決める。それはトークン定義とその値をsemanticValueとしてどのように持つかということ。
    3. Bison側で文法を定義する。
    4. ごちゃごちゃしたものを実装する
        - yylex, yyerrorの宣言
        - Bisonで文法のあとのアクションを実装する。
- だが%unionでせいせいしたSemanticValueの型にコンストラクタとかがないせいでC++でコンパイルすると使えない。デストラクタだけは定義できるけど、代入演算子とかが定義できない。それでコンパイルが通らない。
- なんかわからんが%unionの中のstd::stringを*std::stringにするとコンパイルが通った。

- あとflexをreentrantにしたいのと入力をcinではなくてFILE*として与えたい。
- reentrantはできた。
    - reentrantにして適当にやる。yyscanner_tを宣言したりするといい。
    - コードに書く位置が重要なのマジでやめてほしい。

## 参考

[FlexとBisonで実用的なパーサーを作る](https://zenn.dev/arark/articles/02e4764b851868)
[Flex公式レポジトリのサンプル](https://github.com/westes/flex/tree/master/examples)
[Flex公式ドキュメントのSimple Example](https://westes.github.io/flex/manual/Simple-Examples.html#Simple-Examples)
    - 説明が少なすぎる、どうやってコンパイルするとか書いてない。
[Bison公式ドキュメント](https://www.gnu.org/software/bison/manual/bison.html#Concepts)
    - ここからやってExampleくらいまでやるといい。