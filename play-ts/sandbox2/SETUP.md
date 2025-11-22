# Typescript環境をつくる

```
npm init
npm install -D typescript
npx tsx --init
```


- tsconfig.jsonを適当にいじる
- package.jsonの `type: "module"` を設定してESMを使うようにする
- (任意ではあるが) package.json に `build, start` コマンドを追加

## コンパイル、実行

```
npm run build
npm run start
```

## 追加

- `@` つかってimportするなら `tsup` が必要（FEとかだとViteとかを使うのが普通かも）
- 