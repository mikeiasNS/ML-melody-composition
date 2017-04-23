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
  # 'midi_files/furelise.mid',
  # 'midi_files/asa-branca.mid',
  # 'midi_files/got.mid',
  # 'midi_files/imperial.mid',
  # 'midi_files/pegasus.mid',
  # 'midi_files/moondance.mid',
  # 'midi_files/phantom.mid'
  'midi_files/time_test.mid'
]

for file_name in file_names:
  midi_file = MidiFile(file_name)
  print(midi_file.ticks_per_beat)

  track = merge_tracks(midi_file.tracks)
  # for i, track in enumerate(midi_file.tracks):
  # track.sort(key=lambda message: message.time)
  print(file_name, tone(track))
  for message in track:
    msg_type = message.dict()["type"]
    if msg_type == "time_signature" or message.is_meta:
    	print(message.dict())
    if msg_type == "note_on" or msg_type == "note_off":
    	print(note(message.dict()['note']), message.dict())