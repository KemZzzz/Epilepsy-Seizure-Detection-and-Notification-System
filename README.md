# Epilepsy Seizure Detection and Notification System

![5899983909112889982](https://github.com/user-attachments/assets/4b145c11-2c27-4e2d-90e7-fc4473e07c52)

## Overview
The Epilepsy Seizure Detection and Notification System is designed to detect convulsive seizures in patients using EMG sensors connected to an ESP32 device. The system notifies the patient's relatives and caregivers with the patient's current location and a history of seizures. The project integrates various technologies to ensure timely detection and notification, providing a comprehensive solution for managing epilepsy.

## System Architecture

### Components
- **EMG Sensors and ESP32**: Detects muscle activity and sends data to the ESP32 microcontroller.
- **Arduino Code**: Receives data from EMG sensors and transmits it via MQTT.
- **MQTT Broker**: Manages the data flow between the ESP32 and the server.
- **LSTM Model**: Processes the EMG data to detect seizures.
- **Flask API**: Handles data processing and communication with the Firebase backend.
- **Firebase**: Stores data and handles real-time updates.
- **Flutter App**: Notifies caregivers, stores history, and provides additional information and features.

## Workflow
1. **Detection**: EMG sensors detect muscle activity and send data to ESP32.
2. **Data Transmission**: ESP32 sends data to the MQTT broker.
3. **Processing**: MQTT broker forwards data to the server, where the LSTM model analyzes it.
4. **Notification**: If a seizure is detected, the Flask API sends the data to Firebase.
5. **Alert**: The Flutter app receives notifications from Firebase, alerting caregivers and providing the patient's current location and seizure history.

## Features

### Patient Management
- **Register and Login**: Patients and caregivers can create accounts and log in.
- **Caregiver Management**: Patients can add or remove caregivers.

### Seizure Detection
- **Real-time Monitoring**: Continuous monitoring of EMG data for seizure detection.
- **Notification System**: Immediate alerts sent to caregivers upon seizure detection.

### Additional Functionalities
- **Seizure History**: Stores and displays the history of seizures.
- **Location Tracking**: Provides the current location of the patient during a seizure.
- **Emergency Instructions**: Offers guidance on how to handle convulsive seizures and contact emergency services if needed.
- **Feedback System**: Allows users to provide feedback to help improve the model and the app.

## Setup and Installation

### Hardware Requirements
- EMG sensors
- ESP32 microcontroller

### Software Requirements
- Arduino IDE
- Python (for Flask API and LSTM model)
- Firebase account
- Flutter (for mobile app development)

### Installation Steps

#### Arduino Setup
1. Install the necessary libraries in the Arduino IDE.
2. Upload the Arduino code to the ESP32.

#### MQTT Broker
1. Set up an MQTT broker (e.g., Mosquitto).

#### Backend
1. Set up a virtual environment and install required Python packages.
2. Deploy the Flask API.
3. Configure the LSTM model and integrate it with the Flask API.

#### Firebase
1. Set up Firebase and configure the database and authentication.

#### Flutter App
1. Set up Flutter and install necessary dependencies.
2. Configure the app to connect with Firebase.

## Usage

### Start the system
1. Power on the EMG sensors and ESP32 device.
2. Ensure the MQTT broker, Flask API, and Firebase are running.

### Login and Register
1. Open the Flutter app.
2. Register or log in as a patient or caregiver.

### Real-time Monitoring
- The system will continuously monitor EMG data for seizure detection.
- Caregivers will receive notifications if a seizure is detected, along with the patient's location and seizure history.

### Emergency Handling
- Follow the app's instructions on how to deal with convulsive seizures.
- Use the app to contact emergency services if necessary.

### Feedback
- Provide feedback through the app to help improve the detection model and system.

## Contributing
We welcome contributions to enhance the system. Please fork the repository and submit pull requests with detailed descriptions of changes.



## Contact
For any inquiries or support, please contact us at karmezt123@gmail.com.

Thank you for using the Epilepsy Seizure Detection and Notification System. Your feedback and support are invaluable in improving our system and providing better care for those in need.
