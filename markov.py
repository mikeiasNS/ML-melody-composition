import numpy as np
from sklearn.naive_bayes import GaussianNB

class MarkovChain(object):
    def __init__(self, dataset_x, dataset_y):
        self.dataset_x = dataset_x
        self.dataset_y = dataset_y
        self.classifier = GaussianNB()
        
    def predict(self, x, y):
        order = y.size
        
        final_x = []
        final_y = []
        i = 0
        
        while i < self.dataset_y.size - order:
            if self.dataset_y[i:i + order].all() == y.all():
                final_x.insert(len(final_x), self.dataset_x[i + order].tolist())
                final_y.insert(len(final_y), self.dataset_y[i + order].tolist())
            
            i += order
        
        self.classifier.fit(np.array(final_x), np.array(final_y))
        
        return self.classifier.predict(x)