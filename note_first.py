import numpy as np
import pandas as pd
import copy
import math
import random
from pre_processor import PreProcessor
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from markov import MarkovChain

# 0: semifusa, 1: fusa, 2: semicolcheia, 3: colcheia, 4: seminima, 5: minima, 6: semibreve
actual_durations = [0.0625, 0.125, 0.250, 0.500, 1, 2, 4]
beats_by_compass = 4
total_compasses = 16

# Importing the dataset
dataset = pd.read_csv('luiz_gonzaga_c.csv', header=None)

X_to_notes = dataset.iloc[:, 0:2].values
y_to_notes = dataset.iloc[:, 3].values

X_to_duration = dataset.iloc[:, [0,1,3]].values
y_to_duration = dataset.iloc[:, 2].values

notes_pre_proc = PreProcessor()
dur_pre_proc = PreProcessor()

X_to_notes = notes_pre_proc.call_method(X_to_notes, 'fit_transform', 
    scale=True, categorical=True, hot_encoder=True,
    categorical_data_index=(range(0, len(X_to_notes)), 0))

test_seq = pd.read_csv('x_test.csv', header=None).iloc[:, :].values
X_test = copy.deepcopy(test_seq)
X_test = notes_pre_proc.call_method(X_test, 'transform', categorical=True, 
    categorical_data_index=(range(0, len(X_test)), 0), hot_encoder=True)
notes_pre_proc.call_method(X_test, 'fit', scale=True)

X_to_duration = dur_pre_proc.call_method(X_to_duration, 'fit_transform',
    scale=True, categorical=True, hot_encoder=True,
    categorical_data_index=(range(0, len(X_to_duration)), 0))

markov_chain = MarkovChain(X_to_notes, y_to_notes)
markov_chain_dur = MarkovChain(X_to_duration, y_to_duration)
notes_y = np.array([])
durations_y = np.array([])
result = np.array([])

i = 1
while(i <= total_compasses):
    current_compass = test_seq[test_seq[:, 1] == i, :]
    
    # get note
    current_note_x = copy.deepcopy(current_compass)
    current_note_x = notes_pre_proc.call_method(current_note_x, 
        'transform', categorical=True,
        categorical_data_index=(range(0,1), 0),
        hot_encoder=True, scale=True)
    if len(notes_y) > 0: 
        note = markov_chain.predict(current_note_x, notes_y)
        notes_y = np.append(notes_y, note)
    else:
        classifier = GaussianNB()
        classifier.fit(X_to_notes, y_to_notes)
    
        note = classifier.predict(current_note_x)
        notes_y = np.append(notes_y, note)
    
    #get duration
    current_dur_x = np.append(current_compass, np.reshape([notes_y[-1]], (1,1)), axis=1)
    current_dur_x = dur_pre_proc.call_method(current_dur_x, 'transform', 
        categorical=True, hot_encoder=True, scale=True,
        categorical_data_index=(range(0,1), 0))
    
    if len(durations_y) > 0:
        duration = markov_chain_dur.predict(current_dur_x, durations_y[-10:])
        durations_y = np.append(durations_y, duration)
    else:
        classifier = GaussianNB()
        classifier.fit(X_to_duration, y_to_duration)
        
        duration = classifier.predict(current_dur_x)
        durations_y = np.append(durations_y, duration)
    
    result = np.append(result, current_compass)
    result = np.append(result, [duration, note])
    result = np.reshape(result, (int(len(result)/4), 4))
    
    total_in_compass = sum([actual_durations[int(x)] for x in durations_y[result[:, 1] == i]])
    
    if(total_in_compass > beats_by_compass):
        durations_y = durations_y[:-1]
        notes_y = notes_y[:-1]
        result = result[:-1, :]
        
    if(total_in_compass == beats_by_compass): i += 1
   
    
# creating MIDI
from mido import Message, MidiFile, MidiTrack, bpm2tempo, MetaMessage

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('set_tempo', tempo=bpm2tempo(120)))

delta = 0
for notes in result:
    if int(notes[3]) < 0: 
        delta += int(mid.ticks_per_beat * actual_durations[notes[2]])
        continue
    track.append(Message('note_on', note=int(notes[3]), time=delta, velocity=127))
    if delta != 0: delta = 0
    track.append(Message('note_off', note=int(notes[3]), 
        time=int(mid.ticks_per_beat * actual_durations[notes[2]])))

mid.save('note_first.mid')