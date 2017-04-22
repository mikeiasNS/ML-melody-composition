#!/usr/bin/env python
"""
Open a MIDI file and print every message in every track.
Support for MIDI files is still experimental.
"""
import sys
from mido import MidiFile
from mido import bpm2tempo
from mido import merge_tracks
from notes import note
from tones import tone

file_names = [
  "midi_files/scales/c.mid", 
  "midi_files/scales/c#.mid",
  "midi_files/scales/d.mid", 
  "midi_files/scales/d#.mid",
  "midi_files/scales/e.mid", 
  "midi_files/scales/f.mid",
  "midi_files/scales/f#.mid", 
  "midi_files/scales/g.mid",
  "midi_files/scales/g#.mid",
  "midi_files/scales/a.mid",
  "midi_files/scales/a#.mid",
  "midi_files/scales/b.mid",
  "midi_files/scales/cm.mid", 
  "midi_files/scales/c#m.mid",
  "midi_files/scales/dm.mid", 
  "midi_files/scales/d#m.mid",
  "midi_files/scales/em.mid", 
  "midi_files/scales/fm.mid",
  "midi_files/scales/f#m.mid", 
  "midi_files/scales/gm.mid",
  "midi_files/scales/g#m.mid",
  "midi_files/scales/am.mid",
  "midi_files/scales/a#m.mid",
  "midi_files/scales/bm.mid"
  # 'midi_files/furelise.mid',
  # 'midi_files/asa-branca.mid',
  # 'midi_files/got.mid',
  # 'midi_files/imperial.mid',
  # 'midi_files/pegasus.mid'
]

for file_name in file_names:
  midi_file = MidiFile(file_name)

  track = merge_tracks(midi_file.tracks)
  # for i, track in enumerate(midi_file.tracks):
  track.sort(key=lambda message: message.time)
  print(file_name, tone(track))
  # for message in track:
  #   msg_type = message.dict()["type"]
    #if message.is_meta:
    # print(message.dict())
    # if msg_type == "time_signature":
    # 	print(message.dict())
    # if msg_type == "note_on":
    # 	print(note(message.dict()['note']), message.dict())