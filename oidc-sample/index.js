import 'dotenv/config';
import express from 'express';
import { Issuer } from 'openid-client';
import cookieParser from 'cookie-parser';

const app = express();
const port = 3000;
app.use(cookieParser());

let client; // グローバルで使うOpenIDクライアント

(async () => {
  const googleIssuer = await Issuer.discover('https://accounts.google.com');
  client = new googleIssuer.Client({
    client_id: process.env.GOOGLE_CLIENT_ID,
    client_secret: process.env.GOOGLE_CLIENT_SECRET,
    redirect_uris: [process.env.REDIRECT_URI],
    response_types: ['code'],
  });

  // ログイン
  app.get('/login', (req, res) => {
    const url = client.authorizationUrl({
      scope: 'openid email profile',
      prompt: 'consent',
      access_type: 'offline',
    });
    res.redirect(url);
  });

  // コールバック
  app.get('/callback', async (req, res) => {
    const params = client.callbackParams(req);
    const tokenSet = await client.callback(process.env.REDIRECT_URI, params);
    console.log('トークンセット:', tokenSet);

    // Refresh Token を Cookie に保存（HttpOnly）
    res.cookie('refresh_token', tokenSet.refresh_token, {
      httpOnly: true,
      secure: false, // 本番では true にする（HTTPSのみ）
      sameSite: 'lax',
      maxAge: 30 * 24 * 60 * 60 * 1000, // 30日
    });

    res.send('<h1>ログイン成功</h1><a href="/protected">認証付きページへ</a>');
  });

  // 🔐 ミドルウェア（認証チェック）
  async function requireAuth(req, res, next) {
    const refreshToken = req.cookies.refresh_token;
    if (!refreshToken) return res.status(401).send('ログインが必要です');

    try {
      // Refresh Token から新しいトークンセットを取得
      const tokenSet = await client.refresh(refreshToken);

      // ユーザー情報を取得
      const userinfo = await client.userinfo(tokenSet.access_token);
      req.user = userinfo; // 次のミドルウェアで使えるように
      next();
    } catch (err) {
      console.error('Token refresh failed:', err);
      res.status(401).send('認証エラー');
    }
  }

  // 🔒 認証付きAPI
  app.get('/protected', requireAuth, (req, res) => {
    res.send(`<h1>ようこそ ${req.user.name} さん</h1>`);
  });

  // ログアウト
  app.get('/logout', async (req, res) => {
  const refreshToken = req.cookies.refresh_token;

  if (refreshToken) {
    try {
      await client.revoke(refreshToken, 'refresh_token');
      console.log('Refresh token revoked.');
    } catch (err) {
      console.error('Revoke failed:', err);
    }
  }

  // Cookie 削除
  res.clearCookie('refresh_token');

  res.send('<h1>ログアウトしました</h1><a href="/login">ログインへ戻る</a>');
});

  app.listen(port, () => {
    console.log(`http://localhost:${port}/login でログインを開始`);
  });
})();
