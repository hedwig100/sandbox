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

モデルと右パネルは同じTripServiceを経由してSQLite上の旅行を更新します。各更新はversionで競合を検出します。旅行先と価格は説明用サンプルで、ライブの空席・料金情報ではありません。SQLiteの保存先は `TRIP_DB_PATH`（既定値 `data/trips.sqlite`）で変更できます。

## 検証

```bash
npm test
npm run typecheck
npm run lint
npm run build
```
