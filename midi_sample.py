#!/usr/bin/env python
"""
Open a MIDI file and print every message in every track.
Support for MIDI files is still experimental.
"""
import sys
from mido import MidiFile, bpm2tempo, tempo2bpm, merge_tracks
from notes import note
from graph.graph import Graph
from graph.vertex import Vertex

import pdb

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
  ticks_per_beat = midi_file.ticks_per_beat
  tempo = 0
  time_signature = ""
  graph = None

  track = merge_tracks(midi_file.tracks)

  for i, message in enumerate(track):
    msg_type = message.dict()["type"]

    if msg_type == 'set_tempo':
      tempo = message.dict()['tempo']
    if msg_type == "time_signature":
    	time_signature = str(message.dict()["numerator"]) + "/" + str(message.dict()['denominator'])

    if msg_type == "note_on":
      duration = 0
      if track[i + 1].dict()['type'] == 'note_off':
        duration = track[i + 1].dict()['time'] - message.dict()['time']
      elif track[i + 1].dict()['type'] == 'set_tempo':
        if track[i + 2].dict()['type'] == 'note_off':
          duration = track[i + 1].dict()['time'] - message.dict()['time']
        else:
          print '******ERROR******'
          break
      else:
        print '******ERROR******'
        break

      vertex = Vertex(message.dict()['note'], duration, tempo)

      if graph == None:
        graph = Graph(vertex, ticks_per_beat, time_signature)
      else:
        graph.keep_going_to(vertex)

  pdb.set_trace()