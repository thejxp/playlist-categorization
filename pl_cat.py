import keras
import tensorflow as tf
import numpy as np
import pandas as pd

from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM

from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

import pl_plot

def encode_data(df, encoder, columns):
   """Integer encodes the specified columns in df."""
   for col in columns:
      df[col] = encoder.fit_transform(df[col])

def inverse_data(df, encoder, columns):
   """Reverse integer encoding on the specified columns of df. """
   for col in columns:
      df[col] = encoder.inverse_transform(df[col])

# def get_accuracy(predictions, test_y):
def calc_error(a):
   if (a == 0):
      return a
   else:
      return 1

def get_rf_prediction(train_X, test_X, train_y, test_y, n):
   rf = RandomForestClassifier(n_estimators = n, random_state = 42)
   rf.fit(train_X, train_y)
   predictions = rf.predict(test_X)
   errors = list(predictions - test_y)
   errors = list(map(lambda x: 0 if x == 0 else 1, errors))
   percent_error=(errors.count(0))/len(errors)*100
   print ("Accuracy Rate: ", percent_error ,"%")
   return rf, percent_error

def run_randf(df):
   all_songs = df.copy()
   label_encoder = LabelEncoder()
   encode_data(all_songs, label_encoder, ["playlist", 'artist'])

   X = all_songs.drop(['id','playlist', 'name', 'release_date','type', 'uri'], axis=1)
   y = all_songs['playlist']
   X_list = list(X.columns)
   X = np.array(X)
   train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.1, random_state = 42)
   rf, percent_error = get_rf_prediction(train_X, test_X, train_y, test_y, 560)
   return rf, percent_error


def run_lstm(df):
   all_songs = df.copy()

   #encode data
   label_encoder = LabelEncoder()
   encode_data(all_songs, label_encoder, ["playlist", 'artist'])

   # preliminary plotting
   playlist_plot.plot(all_songs,  fields=['danceability','energy'], title="All Songs")

if __name__ == "__main__":
   all_songs = pd.read_csv('all songs.csv', na_values=["n/a", ""])

   rf, percent_error = run_randf(all_songs)


