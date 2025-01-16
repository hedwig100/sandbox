# WebSocket Chat Application

## Usage
```
npm install
npm run server
```

VscodeのLiveServerという拡張機能でindex.htmlのサーバを立てる(これでアクセスしないとCORSエラーで多分動かない).
http://localhost:5500にアクセスする.

## メモ
- npmでプロジェクト作る. socket.ioとnodemonをインストール
- server.jsがサーバ, script.js, index.htmlがクライアント
- CORSエラーが出たので https://qiita.com/error484/items/c3047277fe9b4aa03f8d を参考に修正した
- あとは `.emit, .on. .broadcast` でいい感じにやれば大丈夫. 

疑問
- ずっとコネクションを繋いでいることは何か問題になることはないのか?
- ずっとコネクションを繋いでいるわけにはいかないと思うが, どのようなタイミングで切るべきなのか?(ライフサイクル)

## References
- https://medium.com/@bootcampmillionaire/what-i-learned-about-websockets-by-building-a-real-time-chat-application-using-socket-io-3d9e163e504
- https://www.youtube.com/watch?v=rxzOqP9YwmM
- https://github.com/WebDevSimplified/Realtime-Simple-Chat-App