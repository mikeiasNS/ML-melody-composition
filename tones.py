from notes import note
import operator
import pdb
TONES = {
  'C': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
  'C#': ['C#', 'D#', 'F', 'F#', 'G#', 'A#', 'C'],
  'D': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
  'D#': ['D#', 'F', 'G', 'G#', 'A#', 'C', 'D'],
  'E': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
  'F': ['F', 'G', 'A', 'A#', 'C', 'D', 'E'],
  'F#': ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'F'],
  'G': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
  'G#': ['G#', 'A#', 'C', 'C#', 'D#', 'F', 'G'],
  'A': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
  'A#': ['A#', 'C', 'D', 'D#', 'F', 'G', 'A'],
  'B': ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'],
  'Am': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
  'A#m': ['A#', 'C', 'C#', 'D#', 'F', 'F#', 'G#'],
  'Bm': ['B', 'C#', 'D', 'E', 'F#', 'G', 'A'],
  'Cm': ['C', 'D', 'D#', 'F', 'G', 'G#', 'A#'],
  'C#m': ['C#', 'D#', 'E', 'F#', 'G#', 'A', 'B'],
  'Dm': ['D', 'E', 'F', 'G', 'A', 'A#', 'C'],
  'D#m': ['D#', 'F', 'F#', 'G#', 'A#', 'B', 'C#'],
  'Em': ['E', 'F#', 'G', 'A', 'B', 'C', 'D'],
  'Fm': ['F', 'G', 'G#', 'A#', 'C', 'C#', 'D#', ],
  'F#m': ['F#', 'G#', 'A', 'B', 'C#', 'D', 'E'],
  'Gm': ['G', 'A', 'A#', 'C', 'D', 'D#', 'F'],
  'G#m': ['G#', 'A#', 'B', 'C#', 'D#', 'E', 'F#']
}

TONES_PER_NOTE = {
  'C': ['C', 'Am', 'C#', 'A#m', 'D#', 'Cm', 'F', 'Dm', 'G', 'Em', 'G#', 'Fm', 'A#', 'Gm'],
  'C#': ['C#', 'A#m', 'D', 'Bm', 'E', 'C#m', 'F#', 'D#m', 'G#', 'Fm', 'A', 'F#m', 'B', 'G#m'],
  'D': ['C', 'Am', 'D', 'Bm', 'D#', 'Cm', 'F', 'Dm', 'G', 'Em', 'A', 'F#m', 'A#', 'Gm'],
  'D#': ['C#', 'A#m', 'D#', 'Cm', 'E', 'C#m', 'F#', 'D#m', 'G#', 'Fm', 'A#', 'Gm', 'B', 'G#m'],
  'E': ['C', 'Am', 'D', 'Bm', 'E', 'C#m', 'F', 'Dm', 'G', 'Em', 'A', 'F#m', 'B', 'G#m'],
  'F': ['C', 'Am', 'C#', 'A#m', 'D#', 'Cm', 'F', 'Dm', 'F#', 'D#m', 'G#', 'Fm', 'A#', 'Gm'],
  'F#': ['C#', 'A#m', 'D', 'Bm', 'E', 'C#m', 'G', 'Em', 'A', 'F#m', 'F#', 'D#m', 'B', 'G#m'],
  'G': ['C', 'Am', 'D', 'Bm', 'D#', 'Cm', 'F', 'Dm', 'G', 'Em', 'G#', 'Fm', 'A#', 'Gm'],
  'G#': ['C#', 'A#m', 'D#', 'Cm', 'E', 'C#m', 'F#', 'D#m', 'G#', 'Fm', 'A', 'F#m', 'B', 'G#m'],
  'A': ['C', 'Am', 'D', 'Bm', 'E', 'C#m', 'F', 'Dm', 'G', 'Em', 'A', 'F#m', 'A#', 'Gm'],
  'A#': ['C#', 'A#m', 'D#', 'Cm', 'F', 'Dm', 'F#', 'D#m', 'G#', 'Fm', 'A#', 'Gm', 'B', 'G#m'],
  'B': ['C', 'Am', 'D', 'Bm', 'E', 'C#m', 'F#', 'D#m', 'G', 'Em', 'A', 'F#m', 'B', 'G#m']
}

def tone(track):
  qtt_in_tone = {
    'C': 0, 'C#': 0, 'D': 0, 'D#': 0, 'E': 0, 'F': 0, 
    'F#': 0, 'G': 0, 'G#': 0, 'A': 0, 'A#': 0, 'B': 0,
    'Cm': 0, 'C#m': 0, 'Dm': 0, 'D#m': 0, 'Em': 0, 'Fm': 0, 
    'F#m': 0, 'Gm': 0, 'G#m': 0, 'Am': 0, 'A#m': 0, 'Bm': 0
  }

  qtt_notes = {
    'C': 0, 'C#': 0, 'D': 0, 'D#': 0, 'E': 0, 'F': 0, 
    'F#': 0, 'G': 0, 'G#': 0, 'A': 0, 'A#': 0, 'B': 0
  }

  for message in track:
    if message.dict()["type"] == "note_on":
      current_note = note(message.dict()['note'], False)
      qtt_notes[current_note] += 1
      for possible_tone in TONES_PER_NOTE[current_note]:
        qtt_in_tone[possible_tone] += 1
  
  return major_or_minor(qtt_notes, qtt_in_tone)


def major_or_minor(qtt_notes, tone_prob):
  tone = max(tone_prob.iteritems(), key=operator.itemgetter(1))
  tones = [tone]
  del tone_prob[tone[0]]

  while True:
    tone = max(tone_prob.iteritems(), key=operator.itemgetter(1))
    if tone[1] == tones[-1][1]: 
      tones.append(tone)
      del tone_prob[tone[0]]
    else:
      break

  if len(tones) < 2:
    return tones[0]



  for i in range(len(tones) -1, -1, -1):
    current_tone = tones[i]
    tonic_note = current_tone[0]
    # third_note = TONES[tonic_note][2].replace('m', '')
    # sixth_note = TONES[tonic_note][5].replace('m', '')
    fifth_note = TONES[tonic_note][4].replace('m', '')
    fourth_note = TONES[tonic_note][3].replace('m', '')

    tones[i] += (qtt_notes[tonic_note.replace('m', '')] + qtt_notes[fourth_note] + qtt_notes[fifth_note],)

    # pdb.set_trace()

    if i < len(tones) - 1: 
      if tones[i][2] > tones[i+1][2]:
        del tones[i+1]
      elif tones[i][2] < tones[i+1][2]:
        del tones[i]

    # pdb.set_trace()

  return tones[0]