import numpy as np
import pandas as pd

# 0: semicolcheia, 1: tercina, 2: colcheia, 3: seminima, 4: minima, 5: semibreve
actual_durations = [0.25, 0.33, 0.5, 1, 2, 4]

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

X_test = pd.read_csv('x_test.csv', header=None).iloc[:, :].values
X_test[:, 0] = labelencoder_X.transform(X_test[:, 0])
X_test = onehotencoder.transform(X_test).toarray()
X_test = sc.fit_transform(X_test)

y_pred = classifier.predict(X_test)

result = pd.read_csv('x_test.csv', header=None).iloc[:, :].values
np.concatenate((result, np.array([y_pred]).T), axis=1)