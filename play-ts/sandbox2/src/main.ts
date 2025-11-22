import { exportAdd } from '@/lib.js';
import { env } from '@/env';

const main = (): void => {
  console.log('This is sandbox2 main.ts');
  const result = exportAdd(5, 7);
  console.log(`5 + 7 = ${result}`);
  console.log(`Your database url from .env is: ${env.DATABASE_URL}`);
  console.log(`Your port from .env is: ${env.PORT}`);
  console.log(`Your node_env from .env is: ${env.NODE_ENV}`);
};

main();
