# Typescript Sandbox

## MEMO

2025/9/21

- 以下でpacakgeの準備

```
mkdir typescript-sandbox
cd typescript-sandbox
npm init
```

- Typescript、開発環境関連を追加

[jestの参考](https://typescriptbook.jp/tutorials/jest)

```
npm install typescript
npm install --save-dev prettier
npm install --save-dev jest
npm install --save-dev ts-jest
npm install --save-dev @types/jest
```

- testの設定

```
npx ts-jest config:init
```

- jest.config.jsの設定
```js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node'
};
```

- tsconfig.jsonを作る
```
npx tsc --init
```

- tsconfig.jsonの以下だけ変更
```
    "module": "commonjs",
    "target": "ES2019",
```

- package.jsonに以下を追加

```js
  "scripts": {
    "test": "jest",
    "format": "prettier --write **/*.{js,ts,tsx}"
  },
```

- index.tsを追加
- 以下をpackage.jsonに追加
```js
    "build": "npx tsc",
    "start": "node ./dist/index.js",
```


