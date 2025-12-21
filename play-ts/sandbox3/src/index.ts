import express from 'express';
import { type Chord, type BaseSound, ChordSchema } from './types/chord.js';
import { validateMiddleware } from './middleware/validate.js';
import { loggerMiddleware } from './middleware/logging.js';
import { ChordTones } from './services/chord.js';

const app: express.Application = express();
const PORT: number = 3000;

app.use(express.json());
app.use(loggerMiddleware);

app.get('/health', (req: express.Request, res: express.Response) => {
  res.status(200).send('OK');
});

app.post('/chord', validateMiddleware(ChordSchema), (req: express.Request, res: express.Response) => {
  const chord: Chord = req.body;
  const tones: BaseSound[] = ChordTones(chord);
  res.status(200).json(tones);
});

app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});