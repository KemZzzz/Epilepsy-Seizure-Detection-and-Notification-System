import mne
import numpy as np
import pandas as pd
from imblearn.over_sampling import RandomOverSampler
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split


class EMGDataLoader:
    def __init__(self, path):
        self.path = path

    def load_emg_data(self, signals):
        data = mne.io.read_raw_edf(signals, preload=True, verbose=False, encoding='latin1')
        data.resample(1000)
        return data

    def load_emg_csv(self, path):
        data = pd.read_csv(path)
        data = data.loc[:, ~data.columns.str.startswith('Unnamed: 0')]
        data = data.to_numpy()
        data = data.reshape(6, -1)

        info = mne.create_info(6, 1024, ch_types='emg', verbose=None)
        emg = mne.io.RawArray(data, info, verbose=True)

        return emg

    def get_datalabels(self, non_data, seizure_data, insert_col):
        seizure_labels = [1] * len(seizure_data)
        non_labels = [0] * len(non_data)

        all_data = np.concatenate((non_data, seizure_data), axis=0)
        all_label = non_labels + seizure_labels

        data_label = np.insert(all_data, insert_col, all_label, axis=1)
        np.random.shuffle(data_label)

        data_label = pd.DataFrame(data_label)

        print(data_label)
        sig, label = data_label.iloc[:, :-1], data_label.iloc[:, -1]

        return sig, label

    def splitting_data(self, sig, label):
        oversampler = RandomOverSampler(
            sampling_strategy=1.0, random_state=0
        )
        data_input_balanced, data_output_balanced = oversampler.fit_resample(
            sig, label
        )

        X, X_test, y, y_test = train_test_split(
            data_input_balanced, data_output_balanced, test_size=0.20, random_state=42
        )

        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.25, random_state=42
        )

        return X_train, y_train, X_val, y_val, X_test, y_test

    def get_checkpoint_callback(self):
        return ModelCheckpoint(
            filepath='checkpoints/',
            save_weights_only=True,
            save_freq='epoch',  # Save weights every epoch
            monitor='val_loss',
            mode='min',
            save_best_only=True,
            verbose=1
        )


if __name__ == '__main__':
    data_loader = EMGDataLoader('C:/Users/karme/Downloads/new_data_encoded/')
    # Use data_loader methods to load, preprocess, and split data as needed
