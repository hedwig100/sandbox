# README

https://chatgpt.com/c/691ed2dd-4970-8324-a448-b1da17b8cec6

```
tsc main.ts
node main.js
```

## TODO

- DONE: tsを普通に使ってみる(型付け、トランスパイル、パッケージ追加など) 
- ts + jestを試す
- ts + prettier + eslint を試す
- ts + express を試す
- ts + react + viteを試す
- tsでBE,FEをどっちも同じProjectで作る

## 勉強

### Javascriptの文法

- let, const, var
- async, await
- イベントループ
- (ES5 -> ES6はJavascriptの仕様で、現代ではS6が使われていると思ってよい)

### Typescriptの文法

- 型: number, boolean[]
- type宣言: type User = { name: string }
    - Union型
- interface:

### 実行環境

- ブラウザ
- Nodejs
- Typescriptの場合(トランスパイラ)
    - tsc
    - ts-node
    - ts-node-dev

### フォーマッタ、リンター

- prettier
- ESLint

### Module

- ESM: ブラウザにおける仕様 `import { a } from "./main.js"`
- CommonJS: Nodejsにおける仕様、Nodeはブラウザよりまえに実装していたので独自moduleシステムだったが、最近ESMにも対応した `const fs = requre('fs');` みたいなやつ

### tsconfig.json

- Typescriptのコンパイラの設定を行うファイル、たとえば出力するjavascriptのバージョンとか、anyを許すかとかmoduleシステムは何でトランスパイルするかとか

### トランスパイラ、バンドラ

歴史的経緯はあるが、Viteが今は強い

- Babel: 新しいjsを古いjsに変換するツール、webpack + babelでバンドルするのが昔は多かった
- Webpack: JS, CSS, 画像などすべてをバンドルするバンドラー、何でもバンドルできるがその分遅い
- esbuild: Goで書かれたトランスパイラでtypescriptを直接処理でき、Babelの100倍高速らしい
- Vite: 開発中はESM + esbuildで爆速、本番ビルドはRollupを使う、Typescriptのトランスパイルも行う

### その他ランタイム

- Bun
- Deno

### 主要ライブラリ

**UIフレームワーク**
- React:
- Vue:
- Svelte:
- SolidJS:

**UIコンポーネント**
- shadcn/ui
- Chakra UI
- MUI

**CSSスタイリング**
- Tailwind CSS

**フロントエンドの状態管理**
- Zustand
- Redux
- Recoil

**ルーティング**
- Next.js App Router

**データフェッチ**
- Tanstack Query
- SWR

**Web API**
- Express: API実装
- Fastify
- NestJS

**DB ORM**
- Prisma
- Drizzle ORM

**バリデーション、スキーマ**
- Zod: 型

**テスト**
- Vitest
- Jest
- Playwright

**フルスタックフレームワーク(SSRを実現する)**
- Next.js
- Remis
- Nuxt



