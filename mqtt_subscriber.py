import csv
import time
import datetime
import os
import glob
from threading import Timer
import paho.mqtt.client as mqtt
import requests

mqtt_broker = "192.168.137.1"
mqtt_topic = "emg_data"
flask_api_url = "http://localhost:5000/classify_emg"
upload_folder = 'uploads'

emg_signals = []

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)


def on_message(client, userdata, msg):
    try:
        emg_signal = int(msg.payload.decode())
        print("Received message:", emg_signal)

        # Append the signal to the last row if it's not full
        if len(emg_signals) > 0 and len(emg_signals[-1]) < 6:
            emg_signals[-1].append(emg_signal)
        else:
            emg_signals.append([emg_signal])

        # If the last row is full, save it to CSV and clear the list
        if len(emg_signals[-1]) == 6:
            save_to_csv(emg_signals)
            emg_signals.clear()
    except Exception as e:
        print(f"Error processing message: {e}")


def save_to_csv(emg_signals):
    # Generate a more precise timestamp including milliseconds
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    filename = os.path.join(upload_folder, f"emg_data_{current_time}.csv")

    # Open the file in write mode to create a new file with a unique name
    with open(filename, mode='a', newline='') as file:
        fieldnames = ['signal1', 'signal2', 'signal3', 'signal4', 'signal5', 'signal6']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header and the rows of data
        writer.writeheader()
        for row in emg_signals:
            writer.writerow({f'signal{i + 1}': val for i, val in enumerate(row)})


def send_to_flask_api():
    # Find the most recent CSV file in the upload folder
    list_of_files = glob.glob(os.path.join(upload_folder, '*.csv'))
    if not list_of_files:
        print("No CSV files found")
        return

    latest_file = max(list_of_files, key=os.path.getctime)

    try:
        with open(latest_file, 'rb') as f:
            files = {'file': (latest_file, f, 'text/csv')}
            response = requests.post(flask_api_url, files=files)
            print("Flask API response:", response.json())
    except Exception as e:
        print(f"Error sending data to Flask API: {e}")
    finally:
        os.remove(latest_file)  # Remove the file after sending


def save_and_send():
    save_to_csv(emg_signals)
    send_to_flask_api()
    emg_signals.clear()
    Timer(60.0, save_and_send).start()  # Restart the timer for the next minute


client = mqtt.Client()
client.on_message = on_message

try:
    client.connect(mqtt_broker, 1883, 60)
    client.subscribe(mqtt_topic)
    client.loop_start()
    Timer(60.0, save_and_send).start()  # Start the timer for periodic saving and sending
    while True:
        time.sleep(1)  # Keep the main thread alive
except Exception as e:
    print(f"Error: {e}")
finally:
    client.disconnect()
