import {z} from 'zod';
import express from 'express';

const validate = <T>(schema: z.ZodType<T>) => {
  return (data: unknown): T => {
    const result = schema.safeParse(data);
    if (!result.success) {
      throw new Error(`Validation failed: ${result.error.message}`);
    }
    return result.data;
  };
};

export const validateMiddleware = <T>(schema: z.ZodType<T>) => {
  return (req: express.Request, res: express.Response, next: express.NextFunction) => {
    try {
      req.body = validate(schema)(req.body);
      next();
    } catch (error) {
      res.status(400).json({ error: (error as Error).message });
    }
  };
};