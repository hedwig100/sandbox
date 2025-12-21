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
- `process.env` とか使うならnodeの型定義をインストールする必要がある
    - `npm install --save-dev @types/node`
- eslint, prettier:
    - `npm install -D eslint prettier`
    - `npm install -D @typescript-eslint/parser @typescript-eslint/eslint-plugin`
    - `npm install -D eslint-config-prettier eslint-plugin-prettier`
    - `npx eslint --init`: config生成
    - prettierは設定ファイル`.prettierrc`を手動で作成
- jest:
    - `npm install -D jest ts-jest @types/jest`
    - `npm init jest`
    - (`npm install -D ts-node`)