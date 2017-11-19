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

X = dataset.iloc[:, 0:2].values
y = dataset.iloc[:, 2].values

pre_processor = PreProcessor()

X = pre_processor.call_method(X, 'fit_transform', scale=True, categorical=True,
    categorical_data_index=(range(0, len(X)), 0), hot_encoder=True)

classifier = RandomForestClassifier()
classifier.fit(X, y)

durations_y = np.array([[]])
test_seq = pd.read_csv('x_test.csv', header=None).iloc[:, :].values
X_test = copy.deepcopy(test_seq)
X_test = pre_processor.call_method(X_test, 'transform', categorical=True, 
    categorical_data_index=(range(0, len(X_test)), 0), hot_encoder=True)
pre_processor.call_method(X_test, 'fit', scale=True)

i = 1
while(i <= total_compasses):
    compass_durations_X = test_seq[test_seq[:, 1] == i, :]
    
    X_test = copy.deepcopy(compass_durations_X)
    X_test = pre_processor.call_method(X_test, 'transform', hot_encoder=True, scale=True, 
        categorical=True, categorical_data_index=(range(0, len(X_test)), 0))
    
    classifier = RandomForestClassifier()
    classifier.fit(X, y)
    y_pred = classifier.predict(X_test)
    k = math.ceil(1 / actual_durations[y_pred[0]] - 1)
    if k > 0:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X, y)
        k_neighbors = knn.kneighbors(X_test, k, return_distance=False)
        y_pred = [y[k_neighbors[0][random.randrange(k)]]]
    
    compass_durations_X = np.concatenate((compass_durations_X, np.array([y_pred]).T), axis=1)
    durations_y = np.append(durations_y, compass_durations_X)
    durations_y = np.reshape(durations_y, (int(len(durations_y)/3), 3))
    
    total_in_current_compass = sum([actual_durations[x] for x in durations_y[durations_y[:, 1] == i, 2]])
    if total_in_current_compass > beats_by_compass:
        durations_y = durations_y[:-1, :]
        total_in_current_compass = sum([actual_durations[x] for x in durations_y[durations_y[:, 1] == i, 2]])
        
    if total_in_current_compass == beats_by_compass: i += 1

X = dataset.iloc[:, 0:3].values
y = dataset.iloc[:, 3].values

X = pre_processor.call_method(X, 'fit_transform', scale=True, categorical=True,
    categorical_data_index=(range(0, len(X)), 0), hot_encoder=True)

durations_X = copy.deepcopy(durations_y)
durations_X = pre_processor.call_method(durations_X, 'transform', categorical=True, 
    categorical_data_index=(range(0, len(durations_X)), 0), hot_encoder=True)
pre_processor.call_method(durations_X, 'fit', scale=True)

notes_y = np.array([])

markov_chain = MarkovChain(X, y)
order = 1

for i in range(0, len(durations_X)):
    current_note_x = durations_X[i]
    current_note_x = pre_processor.call_method([current_note_x], 'transform', scale=True)
    
    if i > 0: 
        y_pred = markov_chain.predict(current_note_x, notes_y)
        notes_y = np.append(notes_y, y_pred)
    else:
        classifier = GaussianNB()
        classifier.fit(X, y)
    
        y_pred = classifier.predict(current_note_x)
    
        notes_y = np.append(notes_y, y_pred)

melody = np.concatenate((durations_y, np.array([notes_y]).T), axis=1) 

# creating MIDI

from mido import Message, MidiFile, MidiTrack, bpm2tempo, MetaMessage

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('set_tempo', tempo=bpm2tempo(120)))

delta = 0
for notes in melody:
    if int(notes[3]) < 0: 
        delta += int(mid.ticks_per_beat * actual_durations[notes[2]])
        continue
    track.append(Message('note_on', note=int(notes[3]), time=delta, velocity=127))
    if delta != 0: delta = 0
    track.append(Message('note_off', note=int(notes[3]), 
        time=int(mid.ticks_per_beat * actual_durations[notes[2]])))

mid.save('new_song.mid')