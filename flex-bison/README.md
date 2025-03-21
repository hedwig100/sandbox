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

## 参考

[FlexとBisonで実用的なパーサーを作る](https://zenn.dev/arark/articles/02e4764b851868)
[公式レポジトリのサンプル](https://github.com/westes/flex/tree/master/examples)
[公式ドキュメントのSimple Example](https://westes.github.io/flex/manual/Simple-Examples.html#Simple-Examples)
    - 説明が少なすぎる、どうやってコンパイルするとか書いてない。