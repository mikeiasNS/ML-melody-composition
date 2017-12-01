from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import StandardScaler

class PreProcessor(object):
  def __init__(self):
    self.scaler = StandardScaler()
    self.label_encoder = LabelEncoder()
    self.one_hot_encoder = OneHotEncoder()

  def call_method(self,x, method, scale=False, categorical=False, categorical_data_index=0, hot_encoder=False):
    if categorical: x[categorical_data_index] = getattr(self.label_encoder, method)(x[categorical_data_index])
    if hot_encoder: 
        self.one_hot_encoder.categorical_features = [categorical_data_index[1]]
        x = getattr(self.one_hot_encoder, method)(x).toarray()
    if scale: x = getattr(self.scaler, method)(x)

    return x