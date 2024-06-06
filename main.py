import mne
import werkzeug
from scipy.signal import butter, filtfilt
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, Bidirectional, Conv1D, MaxPooling1D, BatchNormalization
from keras.optimizers import Adam
from keras.regularizers import l2


def load_emg_csv(file_path):
    # Read the CSV file
    data = pd.read_csv(file_path)

    # Drop columns with "Unnamed" in their name and drop rows with NaN values
    data = data.loc[:, ~data.columns.str.contains('Unnamed')]
    data = data.dropna()

    # Replace infinite values with NaNs and then drop these rows
    data = data.replace([np.inf, -np.inf], np.nan).dropna()

    # Check if the resulting DataFrame is empty
    if data.empty:
        raise ValueError("The CSV file contains only NaN or infinite values.")

    # Convert the DataFrame to a NumPy array
    data = data.to_numpy()

    # Ensure the data shape is (samples, channels)
    if data.shape[1] != 6:
        raise ValueError("The CSV file must have exactly 6 columns corresponding to the EMG channels.")

    # Transpose the data to match the expected shape (channels, samples) for MNE
    data = data.T

    # Create MNE Info and RawArray
    info = mne.create_info(ch_names=['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6'], sfreq=1024, ch_types=['emg'] * 6)
    emg = mne.io.RawArray(data, info)

    return emg


def load_emg_data(signals):
    data = mne.io.read_raw_edf(signals, preload=True, verbose=False, encoding='latin1')
    data.resample(1000)
    return data


def emg_data_preprocessing(signals):
    # Convert to DataFrame and select relevant columns
    raw_data = signals.to_data_frame()
    raw_data = raw_data.loc[:, ~raw_data.columns.str.startswith('time')]
    raw_data = raw_data.iloc[:, -6:].to_numpy(dtype='float64')

    # Bandpass filter (10-450 Hz)
    low_band = 20 / 500
    high_band = 450 / 500
    a, b = butter(2, [low_band, high_band], btype='band')
    emg_filtered = filtfilt(a, b, raw_data, method='gust')

    # Rectify the signal
    emg_rectified = np.abs(emg_filtered)
    # Normalize the data
    emg_normalized = (emg_rectified - np.mean(emg_rectified, axis=0)) / np.std(emg_rectified, axis=0)

    return emg_normalized


class EMGClassifier:
    def __init__(self, model_path='saved-model/best-EMG'):
        self.model_path = model_path
        self.model = self.create_model()
        self.model.load_weights(self.model_path).expect_partial()

    def create_model(self, input_shape=(1, 6)):
        model = Sequential()
        # Bidirectional LSTM layers
        model.add(Bidirectional(LSTM(128, return_sequences=True), input_shape=input_shape))
        model.add(Dropout(0.2))
        model.add(Bidirectional(LSTM(128)))
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    def classify_emg(self, signal):
        if isinstance(signal, str):
            # Handle file paths
            signal_name = signal
            if signal_name.endswith(".edf"):
                EMG_signal = load_emg_data(signal)
            elif signal_name.endswith(".csv"):
                EMG_signal = load_emg_csv(signal)
            else:
                raise ValueError("Unsupported file format. Please provide a .edf or .csv file.")
        else:
            # Handle file-like objects

            signal_name = werkzeug.utils.secure_filename(signal.filename)

            if signal_name.endswith(".edf"):
                with open("EMG_file.edf", "wb") as save_file:
                    signal.save(save_file)
                EMG_signal = load_emg_data("EMG_file.edf")

            elif signal_name.endswith(".csv"):
                with open("EMG_file.csv", "wb") as save_file:
                    signal.save(save_file)
                EMG_signal = load_emg_csv("EMG_file.csv")
            else:
                raise ValueError("Unsupported file format. Please provide a .edf or .csv file.")

        preprocessed_emg = emg_data_preprocessing(EMG_signal)

        # Reshape data to fit the model input shape
        preprocessed_reshaped = preprocessed_emg.reshape((preprocessed_emg.shape[0], 1, preprocessed_emg.shape[1]))

        # Model prediction on entire sequence or fixed-size windows
        prediction = self.model.predict(preprocessed_reshaped)
        mean_prediction = np.mean(prediction)

        return mean_prediction

    @staticmethod
    def classification(y_pred):
        class_name = 'Seizure' if y_pred >= 0.70 else 'No Seizure'
        prob_Seizure = y_pred
        prob_no_Seizure = 1 - y_pred
        result = {
            'Probability of Seizure': (prob_Seizure * 100),
            'Probability of No Seizure': (prob_no_Seizure * 100),
            'Class Name': class_name
        }

        return result


if __name__ == '__main__':
    classifier = EMGClassifier()

    # For testing :
    file = 'D:\G-Project\data from sensors/emg_data_202405061542.csv'
    result = classifier.classify_emg(file)
    print(classifier.classification(result))
