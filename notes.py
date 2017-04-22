NOTES = { 'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 
          'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11,  
          0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 
          6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}

def note_int(note, octave):
  return octave * 12 + NOTES[note.upper()]

def note(int_note, show_octave = True):
  note = NOTES[int_note % 12]
  octave = "" 
  if show_octave: octave = str(int_note / 12)
  return note + octave