import z from 'zod';

export const BaseSoundSchema = z.enum(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]);
export  const BaseChordTypeSchema = z.enum(["M", "m", "dim",  "7", "m7", "M7"]);
export const ChordSchema = z.object({
  root: BaseSoundSchema,
  type: BaseChordTypeSchema,
});

export type BaseSound = z.infer<typeof BaseSoundSchema>;
export type BaseChordType = z.infer<typeof BaseChordTypeSchema>;
export type Chord = z.infer<typeof ChordSchema>;