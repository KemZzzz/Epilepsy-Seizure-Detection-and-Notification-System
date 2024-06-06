import numpy as np
import pandas as pd
import scipy as sp
from tqdm import tqdm
from Data_Loader import EMGDataLoader
from scipy.signal import find_peaks


class EMGDataProcessor:
    def __init__(self, start_end_file_path):
        self.start_end = pd.read_csv(start_end_file_path)
        self.start_end = self.start_end.loc[:, ~self.start_end.columns.str.startswith('Unnamed: 0')]
        self.path = 'C:/Users/karme/Downloads/new_data_encoded/'

    def emg_data_preprocessing(self, signals):
        raw_data = signals.to_data_frame()
        raw_data = raw_data.loc[:, ~raw_data.columns.str.startswith('time')]
        raw_data = raw_data.iloc[:, -6:]
        raw_data = raw_data.to_numpy(dtype='float64')
        low_band = 20 / 500
        high_band = 450 / 500
        a, b = sp.signal.butter(2, [low_band, high_band], btype='band')
        emg_filtered = sp.signal.filtfilt(a, b, raw_data, method='gust')
        emg_rectified = abs(emg_filtered)
        return emg_rectified

    def process_data(self):
        all_seizure_data = []
        all_non_data = []

        for i in tqdm(range(len(self.start_end.index))):
            temp = str(self.start_end.iloc[i, 0])
            file = EMGDataLoader.load_emg_data(self.path + temp)
            preprocessed = self.emg_data_preprocessing(file)

            Nonstart_time = (self.start_end.iloc[i, 1]) * 1024
            Nonend_time = (self.start_end.iloc[i, 2]) * 1024
            Seizurestart_time = (self.start_end.iloc[i, 3]) * 1024
            Seizureend_time = (self.start_end.iloc[i, 4]) * 1024

            non_data = preprocessed[:][Nonstart_time:Nonend_time]
            seizure_data = preprocessed[:][Seizurestart_time:Seizureend_time]

            all_seizure_data.append(pd.DataFrame(seizure_data))
            all_non_data.append(pd.DataFrame(non_data))

        all_seizure_data = pd.concat(all_seizure_data, ignore_index=True)
        all_non_data = pd.concat(all_non_data, ignore_index=True)

        sig, label = EMGDataLoader.get_datalabels(all_non_data, all_seizure_data, 6)
        X_train, y_train, X_val, y_val, X_test, y_test = EMGDataLoader.splitting_data(sig, label)

        return X_train, y_train, X_val, y_val, X_test, y_test


def data_reshape(X_train, y_train, X_val, y_val, X_test, y_test):
    X_train_array = X_train.to_numpy()
    X_val_array = X_val.to_numpy()
    X_test_array = X_test.to_numpy()

    # Reshape the input data
    X_train_reshaped = X_train_array.reshape((X_train_array.shape[0], 1, X_train_array.shape[1]))
    X_val_reshaped = X_val_array.reshape((X_val_array.shape[0], 1, X_val_array.shape[1]))
    X_test_reshaped = X_test_array.reshape((X_test_array.shape[0], 1, X_test_array.shape[1]))

    y_train_reshaped = np.expand_dims(y_train, axis=1)
    y_val_reshaped = np.expand_dims(y_val, axis=1)
    y_test_reshaped = np.expand_dims(y_test, axis=1)
    return X_train_reshaped, X_val_reshaped, X_test_reshaped, y_train_reshaped, y_val_reshaped, y_test_reshaped


if __name__ == '__main__':
    data_processor = EMGDataProcessor('Start_End.csv')
    X_train, y_train, X_val, y_val, X_test, y_test = data_processor.process_data()
    X_train_reshaped, X_val_reshaped, X_test_reshaped, y_train_reshaped, y_val_reshaped, y_test_reshaped = data_reshape(
        X_train, y_train, X_val, y_val, X_test, y_test)

