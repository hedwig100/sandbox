# Global Interpreter Lock

GILの効果を実感するためのプログラムたち. 

## GILとは
PythonにおいてはGlobal Intepreter Lockというものが存在する. これはPythonの
インタプリタ一つにつき, Pythonのバイトコードは一つしか実行できないという制約である. 
現状Pythonは実行しているプロセス一つにつき一つのインタプリタを持っているため, 
平たく言うと一つのプロセスにつき一つのスレッドしか実行できないと言ってもよい. 

これは並行実行の際に問題となる場合がある. たとえばCPUバウンドな処理を行う二つのスレッドが
あるとする. これをPython以外のGILが存在しない言語でマルチスレッドとして(マルチコア環境で)実行するとする. 二つのスレッドは並列に二つのコアで実行されうるため, 単純に一スレッドで実行する場合と比べ, オーバーヘッドなどを無視すると二倍高速化できることが期待できる.

しかしPythonではGILのため, マルチスレッドで実行しても同期的に実行するのと実行時間が変わらない. 実行時間を二倍にするにはマルチプロセスを用いなければならない. 

## 実験

PythonとC++で実行速度がシングルスレッド, マルチスレッド, マルチプロセスでどのように変化するか実験を行った. それぞれ `single.**, multithread.**, multiprocess.**` が実装である. 以下のスクリプトですべてをコンパイル、実行できる. 

```
./run.sh
```

以下のような実行結果が得られたと思う.

```
Python
Single thread version
Time: 0.39200544357299805sec

Multi thread version
Time: 0.40236806869506836sec

Multi process version
Time: 0.20753026008605957sec

C++
Single thread version
Finishes
Finishes
Time: 0.0707776sec

Multi thread version
Finishes
Finishes
Time: 0.0256312sec

Multi process version
Finishes
Finishes
Time: 0.0253211sec

```

PythonではGILにより`single`と`multithread`の実行時間が変わらない一方, C++では実行時間が減っていることがわかると思う. Pythonでもマルチプロセスを使うと実行時間が半分になっている. またC++で`multithred`と`multiprocess`の実行時間がそれほど変わらないことからスレッドが複数のコアで実行されていることがわかる.