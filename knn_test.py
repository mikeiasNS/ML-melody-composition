import numpy as np
import pandas as pd
import copy

# 0: semicolcheia, 1: colcheia, 2: seminima, 3: minima, 4: semibreve
actual_durations = [0.25, 0.5, 1, 2, 4]
beats_by_compass = 4
total_compasses = 16

# Importing the dataset
dataset = pd.read_csv('musics_mock.csv')
X = dataset.iloc[:, 0:2].values
y = dataset.iloc[:, 2].values

# categorical data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X = LabelEncoder()
X[:, 0] = labelencoder_X.fit_transform(X[:, 0])
onehotencoder = OneHotEncoder(categorical_features = [0])
X = onehotencoder.fit_transform(X).toarray()

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)

from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier()
classifier.fit(X, y)


result = np.array([[]])
test_seq = pd.read_csv('x_test.csv', header=None).iloc[:, :].values
X_test = copy.deepcopy(test_seq)
X_test[:, 0] = labelencoder_X.transform(X_test[:, 0])
X_test = onehotencoder.transform(X_test).toarray()
sc.fit(X_test)

i = 1
while(i <= 4): 
    compass_result = test_seq[test_seq[:, 1] == i, :]
    
    X_test = copy.deepcopy(compass_result)
    X_test[:, 0] = labelencoder_X.transform(X_test[:, 0])
    X_test = onehotencoder.transform(X_test).toarray()
    X_test = sc.transform(X_test)
    
    y_pred = classifier.predict(X_test)
    
    compass_result = np.concatenate((compass_result, np.array([y_pred]).T), axis=1)
    result = np.append(result, (compass_result))
    result = np.reshape(result, (int(len(result)/3), 3))
    
    if sum([actual_durations[x] for x in result[result[:, 1] == i, 2]]) == beats_by_compass: i += 1