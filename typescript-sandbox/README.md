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

```
npm install typescript
npm install --save-dev prettier
npm install --save-dev jest
```

- testの設定

```
npx ts-jest config:init
```

- jest.config.jsの設定
```js
module.exports = {
  testEnvironment: 'node',
	testMatch: [
		'**/*.test.ts',
    '**/*.test.js',  
	],
	testPathIgnorePatterns: ['/node_modules/', '/src/'],
};
```

- package.jsonに以下を追加

```js
  "scripts": {
    "test": "jest",
    "format": "prettier --write ."
  },
```


