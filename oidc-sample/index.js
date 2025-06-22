import 'dotenv/config';
import express from 'express';
import { Issuer } from 'openid-client';

const app = express();
const port = 3000;

(async () => {
  // GoogleのIssuer情報を取得
  const googleIssuer = await Issuer.discover('https://accounts.google.com');

  // クライアントの設定
  const client = new googleIssuer.Client({
    client_id: process.env.GOOGLE_CLIENT_ID,
    client_secret: process.env.GOOGLE_CLIENT_SECRET,
    redirect_uris: [process.env.REDIRECT_URI],
    response_types: ['code'],
  });

  // ログイン開始URL
  app.get('/login', (req, res) => {
    const url = client.authorizationUrl({
      scope: 'openid email profile',
      // PKCEはopenid-clientが自動対応
    });
    res.redirect(url);
  });

  // コールバック処理
  app.get('/callback', async (req, res) => {
    const params = client.callbackParams(req);
    try {
      const tokenSet = await client.callback(process.env.REDIRECT_URI, params);
      // IDトークンやアクセストークンを取得
      console.log('ID Token:', tokenSet.id_token);
      console.log('Access Token:', tokenSet.access_token);

      // ユーザー情報取得
      const userinfo = await client.userinfo(tokenSet.access_token);

      res.send(`
        <h1>ログイン成功！</h1>
        <pre>${JSON.stringify(userinfo, null, 2)}</pre>
      `);
    } catch (err) {
      res.status(500).send('認証エラー: ' + err.message);
    }
  });

  app.listen(port, () => {
    console.log(`http://localhost:${port}/login でログイン開始`);
  });
})();
