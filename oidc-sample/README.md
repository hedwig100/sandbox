# OIDC sample

```
npm install
node index.js
# http://localhost:3000/loginにアクセス
```

`access_type=offline, prompt=consent`を指定しないとrefresh tokenは返却されないことに注意する.