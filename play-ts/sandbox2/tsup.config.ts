import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/main.ts', 'src/routes/a.ts'],
  format: ['esm'],
  dts: true,
  sourcemap: true,
  clean: true,
});