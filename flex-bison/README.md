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

## 参考

[FlexとBisonで実用的なパーサーを作る](https://zenn.dev/arark/articles/02e4764b851868)
[公式レポジトリのサンプル](https://github.com/westes/flex/tree/master/examples)
[公式ドキュメントのSimple Example](https://westes.github.io/flex/manual/Simple-Examples.html#Simple-Examples)
    - 説明が少なすぎる、どうやってコンパイルするとか書いてない。