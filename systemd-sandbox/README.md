# Systemd sandbox

## メモ

- systemdをWSL上で使うには `/etc/wsl.conf` に何かを書く必要がある. [ここに書いてある.](https://qiita.com/curacao/items/fb9adaf1c097b1acd6a8)
- 起動

```
sudo systemctl daemon-reload
sudo systemctl start tiny_httpd.service
sudo systemctl status tiny_httpd.service
```

- asdfでインストールしたpythonのパスを指定すると実行できない.
- 理想的にはpoetryとかでインストールしたモジュールを利用したものも動かせるようにしたい.
- systemdのファイルたちは環境変数がない状態で実行されるため, 相対パスで実行ファイルを指定したいとき(e.g. poetry, pythonなど)はPath環境変数をEnvironmentalFileなどで与えてやる必要がある.
- 
