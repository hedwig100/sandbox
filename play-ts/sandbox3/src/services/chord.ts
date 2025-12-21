import {type Chord, type BaseChordType, type BaseSound, ChordSchema} from '../types/chord.js';

export const ChordTones = (chord: Chord): BaseSound[] => {
  const {root, type} = chord;
  const semitoneMap: Record<BaseSound, number> = {
    "C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4,
    "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9,
    "A#": 10, "B": 11
  };
  const intervalsMap: Record<BaseChordType, number[]> = {
    "M": [0, 4, 7],
    "m": [0, 3, 7],
    "dim": [0, 3, 6],
    "7": [0, 4, 7, 10],
    "m7": [0, 3, 7, 10],
    "M7": [0, 4, 7, 11]
  };

  const rootSemitone: number = semitoneMap[root];
  const intervals: number[] = intervalsMap[type];

  const tones: BaseSound[] = [];
  for (const interval of intervals) {
    const toneSemitone = (rootSemitone + interval) % 12;
    const tone = Object.keys(semitoneMap).find(key => semitoneMap[key as BaseSound] === toneSemitone) as BaseSound;
    tones.push(tone);
  }
  return tones;
};