# 旅 Canvas

OpenAI Responses APIのエージェントが旅行計画ツールを選び、会話に合わせて右側の旅行ボードを更新するNext.jsデモです。

## セットアップ

```bash
npm install
cp .env.example .env.local
```

`.env.local` の `OPENAI_API_KEY` を実際のキーへ置き換え、起動します。

```bash
npm run dev
```

ブラウザで `http://localhost:3000` を開いてください。モデルを変更するときは `.env.local` に `OPENAI_MODEL` を指定できます。

## ツール

- 旅行条件の更新
- サンプル旅行先の検索
- 候補地のフォーカス
- 日別旅程への追加
- 予算内訳の更新

モデルが直接UIを書き換えることはありません。各ツールが返す型付きイベントをクライアントのreducerが適用します。旅行先と価格は説明用サンプルで、ライブの空席・料金情報ではありません。

## 検証

```bash
npm test
npm run typecheck
npm run lint
npm run build
```
