# Writing an OS in Rust

Reference: https://os.phil-opp.com/

## Build

```
cargo run
```

## Memo

### A Freestanding Rust Binary
- OSに依存する機能なしでコンパイルするための準備.

### Minimum Rust kernel

- VGAテキストバッファという特殊なメモリを利用することで画面に表示する
    - VGAテキストバッファは `0xb8000` という特殊なメモリにある. 
    - 文字列のasciiコードと色のコードを指定することで表示できる. 
- ブートローダーはbootloaderクレートを使う. ブートローダーと自分で実装したカーネルのリンクは
　bootimageというツールを使う. 
- カーネルを動かすために, QEMUのインストール
  ```
  sudo apt-get install qemu-system qemu-system-common qemu-utils
  ```
- qemuで動いた! QEMU上でより簡単に走らせるためにbootimage runnerコマンドを使うとできる. これをCargoのrunner設定を用いることで簡単にできる. つまりただ `cargo run` するだけでQEMUの起動までできる.