# Full-Stack Application

Node.js フルスタックプロジェクト with Express, React, TypeScript, Tailwind CSS, shadcn/ui, and TanStack Query

## セットアップ

### パッケージのインストール

```bash
npm install
```

必要な依存関係は全てpackage.jsonに含まれています。

## 開発

### サーバー起動

```bash
npm run dev:server
```

サーバーは http://localhost:3001 で起動します。

### クライアント起動

```bash
npm run dev:client
```

クライアントは http://localhost:3000 で起動します。

### テスト

```bash
npm test
```

### コードフォーマット

```bash
npm run format
```

## ビルド

```bash
npm run build
```

## shadcn/ui コンポーネントの追加

shadcn/uiのコンポーネントを追加するには、npx shadcn-ui@latestを使用します:

```bash
npx shadcn@latest add button
npx shadcn@latest add card
# など
```

## プロジェクト構造

```
├── src/
│   ├── client/          # React フロントエンド
│   │   ├── api/         # TanStack Query queries/mutations
│   │   ├── components/  # React コンポーネント
│   │   │   └── ui/      # shadcn/ui コンポーネント
│   │   ├── lib/         # ユーティリティ関数
│   │   ├── pages/       # ページコンポーネント
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   └── server/          # Express バックエンド
│       ├── __tests__/   # テスト
│       └── index.ts
├── dist/                # ビルド出力
├── package.json
├── tsconfig.json        # クライアント用TypeScript設定
├── tsconfig.server.json # サーバー用TypeScript設定
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
├── jest.config.js
└── components.json      # shadcn/ui 設定
```

## 技術スタック

### フロントエンド
- React 19
- TypeScript
- React Router
- TanStack Query
- Tailwind CSS
- shadcn/ui
- Vite

### バックエンド
- Node.js
- Express
- TypeScript
- tsx

### 開発ツール
- Jest
- ts-jest
- Prettier
