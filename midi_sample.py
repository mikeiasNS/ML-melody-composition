#!/usr/bin/env python
"""
Open a MIDI file and print every message in every track.
Support for MIDI files is still experimental.
"""
from mido import MidiFile, tempo2bpm, merge_tracks
from tones import tone
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

file_names = [
  # 'midi_files/furelise.mid',
  # 'midi_files/asa-branca.mid',
  # 'midi_files/got.mid',
  # 'midi_files/imperial.mid',
  # 'midi_files/pegasus.mid',
   'midi_files/moondance.mid',
  # 'midi_files/phantom.mid',
  # 'midi_files/time_test.mid'
]

dataset_header = []
dataset = []

for file_name in file_names:
  midi_file = MidiFile(file_name)
  ticks_per_beat = midi_file.ticks_per_beat
  bpm = 0
  time_signature = ""

  track = merge_tracks(midi_file.tracks)
  print(file_name, tone(track))
  for i, message in enumerate(track):
    msg_type = message.dict()["type"]

    if msg_type == 'set_tempo':
      bpm = tempo2bpm(message.dict()['tempo'])
    if msg_type == "time_signature":
      time_signature = str(message.dict()["numerator"]) + "/" + str(message.dict()['denominator'])
    if msg_type == "note_on":
      duration = message.dict()['time'] / ticks_per_beat
      #if message.dict()['time'] > 0: dataset.append([-1, duration, i]) # -1 = pausa
    if msg_type == "note_off":
      duration = message.dict()['time'] / ticks_per_beat
      dataset.append([message.dict()['note'], duration, i])
      
# dataset = np.asarray(dataset)
# X = dataset[:, 1:2]
# wcss = []
# for i in range(1, 11):
#     kmeans = KMeans(n_clusters = i, init = 'k-means++')
#     kmeans.fit(X)
#     wcss.append(kmeans.inertia_)
# plt.plot(range(1, 11), wcss)
# plt.title('The Elbow Method')
# plt.xlabel('Number of clusters')
# plt.ylabel('WCSS')
# plt.show()

# k = 0

# for i in range(0, len(wcss)):
#     if wcss[i] / 2 > wcss[i+1]: 
#         k = i + 1
#     else:
#         break

# kmeans = KMeans(n_clusters = k)
# y_kmeans = kmeans.fit_predict(X)

# colors = ['blue', 'green', 'red', 'gray', 'black', 'white']
# for i in range(0, k):
#     #cluster = list(filter(lambda x: y_kmeans[dataset.index(x)] == i, dataset))
#     x = dataset[y_kmeans == i, 2]
#     y = dataset[y_kmeans == i, 1]
#     plt.scatter(x, y, s=10, c=colors[i]);

# plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 50, c = 'yellow')
# plt.title('Clusters of moondance')
# plt.xlabel('sequence')
# plt.ylabel('note')
# plt.legend()
# plt.show()