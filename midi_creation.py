from mido import Message, MidiFile, MidiTrack, bpm2tempo, MetaMessage

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('set_tempo', tempo=bpm2tempo(120)))
track.append(Message('note_on', note=64, time=0))
track.append(Message('note_off', note=64, time= int(mid.ticks_per_beat * 0.500)))
track.append(Message('note_on', note=64, time=0))
track.append(Message('note_off', note=64, time= int(mid.ticks_per_beat * 0.250)))
track.append(Message('note_on', note=64, time=0))
track.append(Message('note_off', note=64, time= int(mid.ticks_per_beat * 0.125)))
track.append(Message('note_on', note=64, time=0))
track.append(Message('note_off', note=64, time= int(mid.ticks_per_beat * 0.0625)))

mid.save('new_song.mid')