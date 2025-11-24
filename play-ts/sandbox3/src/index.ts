import express from 'express';

const app: express.Application = express();
const PORT: number = 3000;

app.get('/health', (req: express.Request, res: express.Response) => {
  res.status(200).send('OK');
});

app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});